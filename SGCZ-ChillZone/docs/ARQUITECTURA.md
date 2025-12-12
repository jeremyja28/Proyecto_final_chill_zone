# Arquitectura

Patrón MVC con separación en capas:
- Controllers (Flask Blueprints): validación básica y orquestación
- Services: reglas de negocio (SRP, OCP)
- Repositories: SQL parametrizado (DIP)
- Models: dataclasses para claridad
- Utils: DB pool, seguridad, validación, logging

Decisiones:
- MySQL Connector con pool centralizado
- Templating Jinja2 + Bootstrap 5 para UI consistente
- Decoradores de rol para protección por módulo
- Ventana de mantenimiento pre-solicitada

Diagrama (alto nivel):
Cliente -> Controllers -> Services -> Repositories -> MySQL
