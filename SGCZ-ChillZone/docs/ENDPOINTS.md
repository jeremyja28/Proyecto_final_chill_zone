# Endpoints

## Auth
- GET/POST /login -> auth/login.html
- GET /logout
- GET/POST /recuperar -> auth/recover.html
- GET/POST /restablecer -> auth/reset.html

## Reservas (/reservas)
- GET / -> reservas/index.html (mis reservas)
- GET/POST /disponibilidad -> reservas/disponibilidad.html
- POST /crear
- POST /modificar/<id>
- POST /cancelar/<id>

## Uso (/uso)
- GET / -> uso/index.html
- POST /iniciar/<reserva_id>
- POST /finalizar/<uso_id>

## Recursos (/recursos)
- GET / -> recursos/index.html
- POST /crear [ADMIN]
- POST /editar/<id> [ADMIN]
- POST /eliminar/<id> [ADMIN]
- POST /estado/<id> [ADMIN]

## Reportes (/reportes) [ADMIN]
- GET / -> reportes/index.html
- GET /exportar -> CSV

## Admin (/admin) [ADMIN]
- GET / -> admin/index.html
- POST /rol/<user_id>
- POST /bloquear/<user_id>
- POST /config
