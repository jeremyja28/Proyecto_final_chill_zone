# Trazabilidad CU → Rutas → Servicios → Tablas

- CU-01 Login
  - Ruta: GET/POST /login
  - Servicio: auth_service.authenticate
  - Tablas: usuarios

- CU-05 Consultar disponibilidad
  - Ruta: GET/POST /reservas/disponibilidad
  - Servicio: reservas_service.consultar_disponibilidad
  - Tablas: reservas, recursos (vista v_disponibilidad opcional)

- CU-06 Crear reserva
  - Ruta: POST /reservas/crear
  - Servicio: reservas_service.crear_reserva
  - Tablas: reservas

- CU-09 Iniciar uso
  - Ruta: POST /uso/iniciar/<reserva_id>
  - Servicio: uso_service.iniciar_uso
  - Tablas: uso, reservas

- CU-10 Finalizar uso
  - Ruta: POST /uso/finalizar/<uso_id>
  - Servicio: uso_service.finalizar_uso
  - Tablas: uso, reservas

- CU-12 Gestión recursos
  - Ruta: /recursos/*
  - Servicio: recursos_service.*
  - Tablas: recursos

- CU-15 Reportes
  - Ruta: /reportes/*
  - Servicio: reportes_service.*
  - Tablas: reservas, uso, usuarios, recursos

- CU-18 Administración general
  - Ruta: /admin/*
  - Servicio: admin_service.*
  - Tablas: usuarios, config_sistema
