from datetime import date, datetime
from pathlib import Path

from fastapi import FastAPI, Request
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field, field_validator

from .db import connect
from .service import BookingError, TutoringService


WEB_DIR = Path(__file__).parent / "web"


class TutorIn(BaseModel):
    name: str
    subjects: str = ""
    photo: int = Field(default=0, ge=0, le=5)


class TutorPatch(BaseModel):
    name: str | None = None
    subjects: str | None = None
    photo: int | None = Field(default=None, ge=0, le=5)


class StudentIn(BaseModel):
    name: str
    email: str


class BookingIn(BaseModel):
    tutor_id: int
    student_id: int
    start: datetime
    duration_minutes: int

    @field_validator("start")
    @classmethod
    def _hora_local(cls, v: datetime) -> datetime:
        if v.tzinfo is not None:
            raise ValueError("Use hora local sin zona horaria (p. ej. 2030-01-08T10:00:00)")
        return v


class CancelIn(BaseModel):
    student_id: int


def create_app(service: TutoringService | None = None) -> FastAPI:
    svc = service or TutoringService(connect("tutorias.db"))
    app = FastAPI(title="Reservas de Tutorías")
    app.mount("/img", StaticFiles(directory=WEB_DIR / "img"), name="img")
    app.mount("/css", StaticFiles(directory=WEB_DIR / "css"), name="css")

    @app.exception_handler(BookingError)
    async def _handle(_: Request, exc: BookingError):
        return JSONResponse(status_code=exc.status, content={"detail": str(exc)})

    @app.get("/", include_in_schema=False)
    def home():
        return FileResponse(WEB_DIR / "index.html")

    @app.get("/admin", include_in_schema=False)
    def admin_panel():
        return FileResponse(WEB_DIR / "admin.html")

    @app.get("/tutors")
    def list_tutors():
        return svc.list_tutors()

    @app.patch("/tutors/{tutor_id}")
    def update_tutor(tutor_id: int, body: TutorPatch):
        return svc.update_tutor(tutor_id, body.name, body.subjects, body.photo)

    @app.delete("/tutors/{tutor_id}")
    def delete_tutor(tutor_id: int):
        return svc.delete_tutor(tutor_id)

    @app.get("/students/by-email")
    def student_by_email(email: str):
        return svc.find_student_by_email(email)

    @app.post("/tutors", status_code=201)
    def create_tutor(body: TutorIn):
        return svc.create_tutor(body.name, body.subjects, body.photo)

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
