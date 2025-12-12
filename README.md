# Proyecto Final Chill Zone (SGCZ)

![Python](https://img.shields.io/badge/Python-3.12-blue?style=flat-square&logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-3.0-green?style=flat-square&logo=flask&logoColor=white)
![MySQL](https://img.shields.io/badge/MySQL-8.0-orange?style=flat-square&logo=mysql&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-Ready-blue?style=flat-square&logo=docker&logoColor=white)
![AdminLTE](https://img.shields.io/badge/AdminLTE-3.2-purple?style=flat-square)

## Resumen Ejecutivo

El **Sistema de Gestión Chill Zone (SGCZ)** es una aplicación web integral diseñada para la administración y reserva de espacios recreativos y de trabajo colaborativo (Coworking) dentro de una institución (ej. universitaria). El sistema permite a los usuarios consultar la disponibilidad de recursos (como mesas de ping pong, futbolines, salas de estudio), realizar reservas, y reportar incidencias. Para los administradores, ofrece herramientas para gestionar el inventario de recursos, controlar el acceso de usuarios, aplicar sanciones por mal uso y configurar parámetros del sistema como horarios y límites de reserva. El objetivo principal es optimizar el uso de las instalaciones compartidas y mantener un control ordenado de las actividades. Además, gracias a su diseño responsivo basado en AdminLTE, el sistema es completamente funcional tanto en dispositivos de escritorio como en móviles, facilitando el acceso desde cualquier lugar.

## Estructura del Proyecto

El proyecto se organiza en las siguientes carpetas principales:

*   **`SGCZ-ChillZone/`**: Contiene el código fuente del backend de la aplicación (Python/Flask).
    *   **`controllers/`**: Manejadores de rutas (Blueprints) que procesan las peticiones HTTP.
    *   **`models/`**: Definiciones de clases que representan las entidades del negocio.
    *   **`repositories/`**: Capa de acceso a datos que ejecuta las consultas SQL.
    *   **`services/`**: Capa de lógica de negocio que orquesta las operaciones entre controladores y repositorios.
    *   **`static/`**: Archivos estáticos (CSS, JavaScript, imágenes, subidas de usuarios).
    *   **`templates/`**: Plantillas HTML (Jinja2) para la interfaz de usuario.
    *   **`utils/`**: Funciones de utilidad (seguridad, validaciones, base de datos, logs).
    *   **`tests/`**: Pruebas unitarias y de integración.
*   **`AdminLTE-3.2.0/`**: Contiene los recursos de la plantilla de diseño AdminLTE utilizada para el frontend.
*   **`chill_zone_db.sql`**: Script SQL para la creación y población inicial de la base de datos.
*   **`docker-compose.yml` & `dockerfile`**: Archivos de configuración para el despliegue en contenedores Docker.

## Módulos y Funciones Principales

El sistema está dividido en módulos funcionales, cada uno con responsabilidades específicas:

### 1. Autenticación (`auth`)
Gestiona el acceso de los usuarios al sistema.
*   **Funciones clave**: Iniciar sesión, cerrar sesión, protección de rutas por roles, gestión de contraseñas (hashing seguro con **Bcrypt** y verificación).
*   **Roles**: El sistema cuenta con dos roles claramente definidos:
    *   **ADMIN**: Acceso total a configuración, gestión de usuarios, recursos y reportes.
    *   **USUARIO**: Acceso limitado a consultar disponibilidad, gestionar sus propias reservas y reportar incidencias.

### 2. Reservas (`reservas`)
El núcleo del sistema para la gestión de turnos.
*   **Funciones clave**:
    *   `consultar_disponibilidad`: Verifica si un recurso está libre en un horario específico.
    *   `crear_reserva`: Registra una nueva reserva validando reglas de negocio estrictas (cuyos parámetros principales son configurables por el administrador desde el sistema), tales como:
        *   **Horario**: Definido en la configuración (por defecto 07:00 - 22:00).
        *   **Duración**: Rango configurable (por defecto 15 min - 2 horas).
        *   **Simultaneidad**: Un usuario no puede tener más de una reserva activa al mismo tiempo (ni como titular ni como acompañante).
        *   **Anticipación**: Límite de días configurable (por defecto 7 días).
        *   **Reglas por Zona**: La "Chill Zone" requiere mínimo 1 acompañante.
    *   `modificar_reserva`: Permite cambios en reservas existentes.
    *   `cancelar_reserva`: Anula una reserva y libera el recurso.
    *   `listar_reservas_usuario`: Muestra el historial y reservas futuras de un usuario.

### 3. Recursos (`recursos`)
Administración del inventario físico.
*   **Funciones clave**:
    *   `listar_recursos`: Obtiene el catálogo de recursos disponibles.
    *   `crear_recurso`: Añade nuevos ítems al inventario.
    *   `editar_recurso`: Modifica detalles como descripción o imagen.
    *   `cambiar_estado`: Pone recursos en mantenimiento o fuera de servicio.

### 4. Zonas (`zonas`)
Gestión de las áreas físicas (ej. Chill Zone, Coworking).
*   **Funciones clave**:
    *   `listar_zonas`: Muestra las áreas disponibles.
    *   `crear_zona` / `editar_zona`: Administración de la información de las zonas.

### 5. Incidencias (`incidencias`)
Sistema de reporte de daños o problemas.
*   **Funciones clave**:
    *   `crear_incidencia`: Permite a los usuarios reportar un problema (con evidencia fotográfica).
    *   `listar_incidencias`: Vista para administradores de los reportes pendientes.
    *   `atender_incidencia`: Marcar incidencias como revisadas o resueltas.

### 6. Sanciones (`sanciones`)
Control disciplinario de usuarios.
*   **Funciones clave**:
    *   `aplicar_sancion`: Registra una penalización a un usuario (ej. por no presentarse o dañar equipo).
    *   `listar_sanciones`: Historial de sanciones.
    *   `levantar_sancion`: Reactiva el acceso a un usuario sancionado.

### 7. Administración (`admin`)
Configuración global y gestión de usuarios.
*   **Funciones clave**:
    *   `listar_usuarios`: Ver todos los usuarios registrados.
    *   `bloquear_usuario`: Restringir acceso al sistema.
    *   `configurar_sistema`: Ajustar parámetros globales (horarios de apertura, tiempos máximos de reserva).

### 8. Reportes y Estadísticas (`reportes`, `estadisticas`)
Análisis de datos del sistema.
*   **Funciones clave**: Generación de reportes de uso, métricas de ocupación y estadísticas de incidencias.

## Requisitos Técnicos

Para desplegar y ejecutar este proyecto, se requiere el siguiente entorno:

*   **Lenguaje**: Python 3.12+
*   **Base de Datos**: MySQL 8.0
*   **Contenedores**: Docker y Docker Compose (opcional, pero recomendado para despliegue rápido).

## Instalación y Ejecución

### Opción 1: Con Docker (Recomendado)

#### Usando Docker Compose
```bash
# Clonar el repositorio
git clone https://github.com/jeremyja28/Proyecto_final_chill_zone.git
cd Proyecto_final_chill_zone

# Levantar los servicios (Flask + MySQL)
docker-compose up --build
```
**Acceder a la aplicación**: http://localhost:4000

#### Usando imagen Docker existente (con zona horaria Ecuador)
```bash
docker run -d -p 4000:4000 \
  --name practica \
  --add-host=host.docker.internal:host-gateway \
  -e DB_HOST=host.docker.internal \
  -e TZ=America/Guayaquil \
  -e DB_PORT=3306 \
  -e DB_USER=root \
  -e DB_PASSWORD= \
  jeremya28/practica:0.0.1.RELEASE
```

> **Nota**: Este comando configura automáticamente la zona horaria de Ecuador (America/Guayaquil) y conecta con MySQL en el host local.

### Opción 2: Instalación Local

#### 1. Clonar el repositorio
```bash
git clone https://github.com/jeremyja28/Proyecto_final_chill_zone.git
cd Proyecto_final_chill_zone/SGCZ-ChillZone
```

#### 2. Crear entorno virtual e instalar dependencias
```bash
# Crear entorno virtual
python -m venv venv

# Activar entorno virtual
# En Windows:
venv\Scripts\activate
# En Linux/Mac:
source venv/bin/activate

# Instalar dependencias
pip install -r requirements.txt
```

#### 3. Configurar Base de Datos MySQL

**Importar el esquema de la base de datos:**
```bash
mysql -u root -p < ../chill_zone_db.sql
```

**Crear archivo `.env` en la carpeta `SGCZ-ChillZone/`:**
```env
DB_HOST=localhost
DB_PORT=3306
DB_USER=root
DB_PASSWORD=tu_password
DB_NAME=chill_zone_db
TZ=America/Guayaquil
```

#### 4. Ejecutar la aplicación
```bash
python app.py
```
**Acceder a la aplicación**: http://localhost:4000

### Credenciales de Acceso por Defecto

Después de importar `chill_zone_db.sql`, puedes acceder con las credenciales predeterminadas:

| Rol          | Usuario                | Contraseña    |
|--------------|------------------------|---------------|
| Administrador | admin                 | admin123      |
| Usuario      | est1@pucesa.edu.ec     | 12345678      |

> **Importante**: Cambiar las contraseñas predeterminadas en producción.

## Sistema de Notificaciones

Actualmente, el sistema utiliza **notificaciones visuales en la aplicación** (Flash messages) para informar al usuario sobre el éxito o fallo de sus acciones (ej. "Reserva creada con éxito", "Conflicto de horario").

*   **Nota**: El envío de correos electrónicos (confirmaciones, recordatorios) no está implementado en esta versión y se considera una mejora futura.

## Base de Datos

El sistema utiliza una base de datos relacional (MySQL) con las siguientes tablas:

### Tablas Principales
*   **`usuarios`**: Almacena la información de los usuarios (nombre, correo, contraseña, rol, estado).
*   **`recursos`**: Catálogo de ítems reservables (mesas, salas, equipos).
*   **`reservas`**: Registro central de las transacciones de reserva (quién, qué, cuándo).
*   **`incidencias`**: Reportes de problemas asociados a recursos o reservas.
*   **`sanciones`**: Registro de penalizaciones aplicadas a usuarios.

### Tablas Auxiliares y de Configuración
*   **`zonas`**: Define las áreas macro donde se ubican los recursos.
*   **`config_sistema`**: Almacena variables de configuración dinámica (ej. `horario_inicio`, `reserva_duracion_max_min`).
*   **`uso`**: Registro detallado del tiempo real de uso de los recursos.
*   **`reserva_acompanantes`**: Relación de usuarios adicionales que participan en una reserva.
*   **`incidencia_responsables`**: Relación de usuarios implicados en una incidencia reportada.

## Tecnologías Utilizadas

*   **Backend**: Flask 3.0.3
*   **Base de Datos**: MySQL 8.0 (via mysql-connector-python 9.0.0)
*   **Seguridad**: Bcrypt 4.2.0 para hashing de contraseñas
*   **Formularios**: Flask-WTF 1.2.1 + WTForms 3.1.2
*   **Frontend**: AdminLTE 3.2.0, Bootstrap, jQuery
*   **Testing**: pytest 8.3.2
*   **Contenedores**: Docker + Docker Compose
*   **Variables de Entorno**: python-dotenv 1.0.1

## Estructura de la Arquitectura

```
┌──────────────────┐
│   Templates      │  ← Jinja2 (HTML)
│   (Frontend)     │
└────────┬─────────┘
         │
┌────────▼─────────┐
│   Controllers    │  ← Blueprints (Rutas HTTP)
└────────┬─────────┘
         │
┌────────▼─────────┐
│    Services      │  ← Lógica de Negocio
└────────┬─────────┘
         │
┌────────▼─────────┐
│  Repositories    │  ← Acceso a Datos (SQL)
└────────┬─────────┘
         │
┌────────▼─────────┐
│   MySQL DB       │  ← Base de Datos
└──────────────────┘
```

## Contribución

Este es un proyecto académico desarrollado para la materia de Ingeniería de Software. Las contribuciones son bienvenidas:

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add: nueva funcionalidad'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## Licencia

Este proyecto está bajo la Licencia MIT. Ver el archivo [LICENSE](LICENSE) para más detalles.

## Autores

*   **Equipo de Desarrollo** - *Proyecto Final* - [jeremyja28](https://github.com/jeremyja28)

## Mejoras Futuras

*   [ ] Implementación de notificaciones por correo electrónico
*   [ ] Sistema de chat en tiempo real para usuarios
*   [ ] Integración con calendarios externos (Google Calendar, Outlook)
*   [ ] Aplicación móvil nativa (Android/iOS)
*   [ ] Sistema de QR para check-in/check-out automático
*   [ ] Panel de analítica avanzada con gráficos interactivos
*   [ ] API RESTful documentada con Swagger
*   [ ] Sistema de pagos para reservas premium

---

**Desarrollado con ❤️ para la comunidad universitaria**
