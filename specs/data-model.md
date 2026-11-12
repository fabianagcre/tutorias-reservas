# Modelo de datos

**tutors**(id PK, name, subjects)
**students**(id PK, name, email UNIQUE)
**bookings**(id PK, tutor_id FK, student_id FK, start TEXT ISO, end TEXT ISO, status 'active'|'cancelled', created_at, cancelled_at)

Índices: `bookings(tutor_id, start)`, `bookings(student_id, start)`.

Solapamiento: dos reservas activas A y B se solapan si `A.start < B.end AND B.start < A.end` (RN9: contiguas no solapan).
