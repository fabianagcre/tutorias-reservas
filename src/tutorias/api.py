from datetime import date, datetime

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel

from .db import connect
from .service import BookingError, TutoringService


class TutorIn(BaseModel):
    name: str
    subjects: str = ""


class StudentIn(BaseModel):
    name: str
    email: str


class BookingIn(BaseModel):
    tutor_id: int
    student_id: int
    start: datetime
    duration_minutes: int


class CancelIn(BaseModel):
    student_id: int


def create_app(service: TutoringService | None = None) -> FastAPI:
    svc = service or TutoringService(connect("tutorias.db"))
    app = FastAPI(title="Reservas de Tutorías")

    @app.exception_handler(BookingError)
    async def _handle(_: Request, exc: BookingError):
        return JSONResponse(status_code=exc.status, content={"detail": str(exc)})

    @app.post("/tutors", status_code=201)
    def create_tutor(body: TutorIn):
        return svc.create_tutor(body.name, body.subjects)

    @app.post("/students", status_code=201)
    def create_student(body: StudentIn):
        return svc.create_student(body.name, body.email)

    @app.get("/tutors/{tutor_id}/availability")
    def availability(tutor_id: int, date: date):
        return {"tutor_id": tutor_id, "date": date.isoformat(), "free_slots": svc.availability(tutor_id, date)}

    @app.post("/bookings", status_code=201)
    def create_booking(body: BookingIn):
        return svc.create_booking(body.tutor_id, body.student_id, body.start, body.duration_minutes)

    @app.post("/bookings/{booking_id}/cancel")
    def cancel(booking_id: int, body: CancelIn):
        return svc.cancel_booking(booking_id, body.student_id)

    @app.get("/students/{student_id}/bookings")
    def student_bookings(student_id: int):
        svc._require("students", student_id)
        return svc.list_bookings("student_id", student_id)

    @app.get("/tutors/{tutor_id}/bookings")
    def tutor_bookings(tutor_id: int):
        svc._require("tutors", tutor_id)
        return svc.list_bookings("tutor_id", tutor_id)

    return app
