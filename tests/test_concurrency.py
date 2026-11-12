import threading

from conftest import TUE, at
from tutorias.service import BookingError


def test_no_doble_reserva_concurrente(world):
    """RN1 bajo concurrencia: 10 hilos intentan el mismo horario, solo uno gana."""
    s = world["svc"]
    students = [s.create_student(f"E{i}", f"e{i}@utp.ac.pa")["id"] for i in range(10)]
    results = []

    def go(sid):
        try:
            s.create_booking(world["t1"], sid, at(TUE, "14:00"), 60)
            results.append("ok")
        except BookingError:
            results.append("fail")

    threads = [threading.Thread(target=go, args=(sid,)) for sid in students]
    [t.start() for t in threads]
    [t.join() for t in threads]
    assert results.count("ok") == 1
    assert len(s.list_bookings("tutor_id", world["t1"])) == 1
