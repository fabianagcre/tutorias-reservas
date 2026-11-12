import pytest
from conftest import MON, SAT, TUE, at
from tutorias.service import ConflictError, ForbiddenError, ValidationError


def test_ca1_reserva_valida(world):
    b = world["svc"].create_booking(world["t1"], world["s1"], at(TUE, "10:00"), 60)
    assert b["status"] == "active" and b["end"].endswith("11:00:00")


def test_ca2_no_doble_reserva_tutor(world):
    """RN1 — regla crítica: un tutor no puede tener dos reservas solapadas."""
    s = world["svc"]
    s.create_booking(world["t1"], world["s1"], at(TUE, "10:00"), 60)
    with pytest.raises(ConflictError):
        s.create_booking(world["t1"], world["s2"], at(TUE, "10:30"), 30)
    with pytest.raises(ConflictError):  # mismo horario exacto
        s.create_booking(world["t1"], world["s2"], at(TUE, "10:00"), 60)
    assert len(s.list_bookings("tutor_id", world["t1"])) == 1


def test_ca3_no_doble_reserva_estudiante(world):
    s = world["svc"]
    s.create_booking(world["t1"], world["s1"], at(TUE, "10:00"), 60)
    with pytest.raises(ConflictError):
        s.create_booking(world["t2"], world["s1"], at(TUE, "10:30"), 60)


def test_ca4_reservas_contiguas_permitidas(world):
    s = world["svc"]
    s.create_booking(world["t1"], world["s1"], at(TUE, "10:00"), 60)
    assert s.create_booking(world["t1"], world["s2"], at(TUE, "11:00"), 60)["status"] == "active"


@pytest.mark.parametrize("day,hhmm,dur", [(TUE, "07:30", 30), (TUE, "17:30", 60), (SAT, "10:00", 60)])
def test_ca5_horario_de_atencion(world, day, hhmm, dur):
    with pytest.raises(ValidationError):
        world["svc"].create_booking(world["t1"], world["s1"], at(day, hhmm), dur)


@pytest.mark.parametrize("hhmm,dur", [("10:00", 45), ("10:15", 60), ("10:00", 150)])
def test_ca6_duracion_e_inicio(world, hhmm, dur):
    with pytest.raises(ValidationError):
        world["svc"].create_booking(world["t1"], world["s1"], at(TUE, hhmm), dur)


def test_ca7_no_reservar_en_el_pasado(world):
    with pytest.raises(ValidationError):
        world["svc"].create_booking(world["t1"], world["s1"], at(MON, "06:00"), 60)


def test_ca8_maximo_dos_por_dia(world):
    s = world["svc"]
    s.create_booking(world["t1"], world["s1"], at(TUE, "08:00"), 30)
    s.create_booking(world["t1"], world["s1"], at(TUE, "09:00"), 30)
    with pytest.raises(ValidationError):
        s.create_booking(world["t1"], world["s1"], at(TUE, "10:00"), 30)


def test_ca9_cancelar_libera_el_espacio(world):
    s = world["svc"]
    b = s.create_booking(world["t1"], world["s1"], at(TUE, "10:00"), 60)
    assert "10:00" not in s.availability(world["t1"], at(TUE, "00:00").date())
    s.cancel_booking(b["id"], world["s1"])
    assert "10:00" in s.availability(world["t1"], at(TUE, "00:00").date())
    assert s.create_booking(world["t1"], world["s2"], at(TUE, "10:00"), 60)["status"] == "active"


def test_ca10_solo_el_dueno_cancela(world):
    s = world["svc"]
    b = s.create_booking(world["t1"], world["s1"], at(TUE, "10:00"), 60)
    with pytest.raises(ForbiddenError):
        s.cancel_booking(b["id"], world["s2"])


def test_cancelar_dos_veces_es_conflicto(world):
    s = world["svc"]
    b = s.create_booking(world["t1"], world["s1"], at(TUE, "10:00"), 60)
    s.cancel_booking(b["id"], world["s1"])
    with pytest.raises(ConflictError):
        s.cancel_booking(b["id"], world["s1"])


def test_ca11_disponibilidad_excluye_ocupadas(world):
    s = world["svc"]
    s.create_booking(world["t1"], world["s1"], at(TUE, "10:00"), 90)
    free = s.availability(world["t1"], at(TUE, "00:00").date())
    assert not {"10:00", "10:30", "11:00"} & set(free)
    assert "09:30" in free and "11:30" in free


def test_disponibilidad_fin_de_semana_vacia(world):
    assert world["svc"].availability(world["t1"], at(SAT, "00:00").date()) == []


def test_validaciones_de_usuario(svc):
    with pytest.raises(ValidationError):
        svc.create_student("", "x@y.com")
    with pytest.raises(ValidationError):
        svc.create_student("Ana", "sin-arroba")
    svc.create_student("Ana", "a@b.com")
    with pytest.raises(ConflictError):
        svc.create_student("Otra", "A@B.com")
