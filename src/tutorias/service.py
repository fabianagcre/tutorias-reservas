"""Reglas de negocio del sistema de reservas de tutorías (ver specs/business-rules.md)."""
from __future__ import annotations

import sqlite3
import threading
from datetime import date, datetime, time, timedelta
from typing import Callable

OPEN = time(8, 0)
CLOSE = time(18, 0)
ALLOWED_DURATIONS = (30, 60, 90, 120)
MAX_PER_DAY = 2


class BookingError(Exception):
    status = 422


class ValidationError(BookingError):
    status = 422


class ConflictError(BookingError):
    status = 409


class NotFoundError(BookingError):
    status = 404


class ForbiddenError(BookingError):
    status = 403


class TutoringService:
    def __init__(self, conn: sqlite3.Connection, now: Callable[[], datetime] = datetime.now):
        self.conn = conn
        self.now = now
        self._lock = threading.Lock()

    # ---------- altas ----------
    def create_tutor(self, name: str, subjects: str = "") -> dict:
        if not name.strip():
            raise ValidationError("El nombre del tutor es obligatorio")
        cur = self.conn.execute("INSERT INTO tutors(name, subjects) VALUES (?, ?)", (name.strip(), subjects))
        return {"id": cur.lastrowid, "name": name.strip(), "subjects": subjects}

    def create_student(self, name: str, email: str) -> dict:
        if not name.strip() or "@" not in email:
            raise ValidationError("Nombre y correo válidos son obligatorios")
        try:
            cur = self.conn.execute("INSERT INTO students(name, email) VALUES (?, ?)", (name.strip(), email.lower()))
        except sqlite3.IntegrityError:
            raise ConflictError("Ya existe un estudiante con ese correo")
        return {"id": cur.lastrowid, "name": name.strip(), "email": email.lower()}

    def _require(self, table: str, id_: int) -> sqlite3.Row:
        row = self.conn.execute(f"SELECT * FROM {table} WHERE id = ?", (id_,)).fetchone()
        if not row:
            raise NotFoundError(f"{table[:-1]} {id_} no existe")
        return row

    # ---------- validaciones puras ----------
    def _validate_slot(self, start: datetime, duration: int) -> datetime:
        if duration not in ALLOWED_DURATIONS:
            raise ValidationError("La duración debe ser 30, 60, 90 o 120 minutos")  # RN4
        if start.minute not in (0, 30) or start.second or start.microsecond:
            raise ValidationError("La hora de inicio debe ser en :00 o :30")  # RN4
        if start <= self.now():
            raise ValidationError("No se puede reservar en el pasado")  # RN5
        end = start + timedelta(minutes=duration)
        if start.weekday() >= 5:
            raise ValidationError("Solo se atiende de lunes a viernes")  # RN3
        if start.time() < OPEN or end.date() != start.date() or end.time() > CLOSE:
            raise ValidationError("El horario de atención es 08:00–18:00")  # RN3
        return end

    # ---------- reservas ----------
    def _overlap_count(self, column: str, id_: int, start: datetime, end: datetime) -> int:
        row = self.conn.execute(
            f"SELECT COUNT(*) c FROM bookings WHERE {column} = ? AND status = 'active' "
            'AND start < ? AND "end" > ?',
            (id_, end.isoformat(), start.isoformat()),
        ).fetchone()
        return row["c"]

    def create_booking(self, tutor_id: int, student_id: int, start: datetime, duration_minutes: int) -> dict:
        with self._lock:  # serializa para evitar carreras (RN1); la conexión no es reentrante entre hilos
            self._require("tutors", tutor_id)
            self._require("students", student_id)
            end = self._validate_slot(start, duration_minutes)
            self.conn.execute("BEGIN IMMEDIATE")
            try:
                if self._overlap_count("tutor_id", tutor_id, start, end):
                    raise ConflictError("El tutor ya tiene una reserva en ese horario")  # RN1
                if self._overlap_count("student_id", student_id, start, end):
                    raise ConflictError("El estudiante ya tiene una reserva en ese horario")  # RN2
                day_start = datetime.combine(start.date(), time.min).isoformat()
                day_end = datetime.combine(start.date() + timedelta(days=1), time.min).isoformat()
                n = self.conn.execute(
                    "SELECT COUNT(*) c FROM bookings WHERE student_id = ? AND status='active' "
                    "AND start >= ? AND start < ?",
                    (student_id, day_start, day_end),
                ).fetchone()["c"]
                if n >= MAX_PER_DAY:
                    raise ValidationError("Máximo 2 reservas activas por día")  # RN6
                created = self.now().isoformat()
                cur = self.conn.execute(
                    'INSERT INTO bookings(tutor_id, student_id, start, "end", status, created_at) '
                    "VALUES (?, ?, ?, ?, 'active', ?)",
                    (tutor_id, student_id, start.isoformat(), end.isoformat(), created),
                )
                self.conn.execute("COMMIT")
            except Exception:
                self.conn.execute("ROLLBACK")
                raise
        return self.get_booking(cur.lastrowid)

    def get_booking(self, booking_id: int) -> dict:
        row = self._require("bookings", booking_id)
        return dict(row)

    def cancel_booking(self, booking_id: int, student_id: int) -> dict:
        b = self._require("bookings", booking_id)
        if b["student_id"] != student_id:
            raise ForbiddenError("Solo el estudiante dueño puede cancelar")  # RN8
        if b["status"] == "cancelled":
            raise ConflictError("La reserva ya estaba cancelada")
        self.conn.execute(
            "UPDATE bookings SET status='cancelled', cancelled_at=? WHERE id=?",
            (self.now().isoformat(), booking_id),
        )  # RN7
        return self.get_booking(booking_id)

    def list_bookings(self, column: str, id_: int) -> list[dict]:
        rows = self.conn.execute(
            f"SELECT * FROM bookings WHERE {column} = ? ORDER BY start", (id_,)
        ).fetchall()
        return [dict(r) for r in rows]

    def availability(self, tutor_id: int, day: date) -> list[str]:
        """Franjas libres de 30 min (inicio) para un tutor en una fecha."""
        self._require("tutors", tutor_id)
        if day.weekday() >= 5:
            return []
        slots, cursor = [], datetime.combine(day, OPEN)
        limit = datetime.combine(day, CLOSE)
        while cursor < limit:
            nxt = cursor + timedelta(minutes=30)
            if cursor > self.now() and not self._overlap_count("tutor_id", tutor_id, cursor, nxt):
                slots.append(cursor.strftime("%H:%M"))
            cursor = nxt
        return slots
