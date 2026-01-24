<p align="center">
  <img src="https://img.shields.io/badge/🎯_Chill_Zone-SGCZ-00B4D8?style=for-the-badge" alt="Chill Zone Logo" />
</p>

<h1 align="center">🎯 Chill Zone - Sistema de Gestión de Zonas Recreativas</h1>

<p align="center">
  <strong>SGCZ (Sistema de Gestión Chill Zone)</strong><br/>
  Plataforma web integral para la administración de espacios recreativos, reservas y recursos institucionales.
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.11+-3776AB?style=flat-square&logo=python&logoColor=white" alt="Python" />
  <img src="https://img.shields.io/badge/Flask-3.0.3-000000?style=flat-square&logo=flask&logoColor=white" alt="Flask" />
  <img src="https://img.shields.io/badge/MySQL-8.0+-4479A1?style=flat-square&logo=mysql&logoColor=white" alt="MySQL" />
  <img src="https://img.shields.io/badge/AdminLTE-3.2.0-007bff?style=flat-square&logo=bootstrap&logoColor=white" alt="AdminLTE" />
  <img src="https://img.shields.io/badge/Docker-Ready-2496ED?style=flat-square&logo=docker&logoColor=white" alt="Docker" />
  <img src="https://img.shields.io/badge/License-MIT-green?style=flat-square" alt="License" />
  <img src="https://img.shields.io/badge/Status-Production%20Ready-brightgreen?style=flat-square" alt="Status" />
</p>

<p align="center">
  <a href="#-características-principales">Características</a> •
  <a href="#-tecnologías">Tecnologías</a> •
  <a href="#-instalación">Instalación</a> •
  <a href="#-estructura-del-proyecto">Estructura</a> •
  <a href="#-capturas-de-pantalla">Screenshots</a>
</p>

---

## 📖 Descripción

El **Sistema de Gestión Chill Zone (SGCZ)** es una aplicación web integral diseñada para la administración y reserva de espacios recreativos y de trabajo colaborativo (Coworking) dentro de una institución. El sistema permite a los usuarios consultar la disponibilidad de recursos (mesas de ping pong, futbolines, billar, salas de estudio), realizar reservas y reportar incidencias. Para los administradores, ofrece herramientas para gestionar el inventario de recursos, controlar el acceso de usuarios, aplicar sanciones por mal uso y configurar parámetros del sistema.

### 🎯 Objetivos Principales
- 📅 **Reservas inteligentes** con validación de conflictos en tiempo real
- 🛡️ **Sistema de sanciones** con duración automática según gravedad
- 📊 **Dashboard analítico** con métricas de uso y estadísticas
- 🔐 **Control de acceso** basado en roles (Usuario/Administrador)
- 📱 **Diseño responsivo** completamente funcional en móviles

---

## ✨ Características Principales

| Módulo | Descripción |
|--------|-------------|
| 🔐 **Autenticación y Roles** | Login seguro con bcrypt, roles USUARIO/ADMIN, recuperación de contraseña |
| 📅 **Sistema de Reservas** | Reservas en tiempo real, detección de conflictos, acompañantes grupales |
| 🏢 **Gestión de Zonas y Recursos** | CRUD completo, estados de mantenimiento, imágenes personalizadas |
| 🛠️ **Incidencias** | Reportes con evidencia (imágenes/PDF), asignación de responsables |
| ⚠️ **Sanciones** | Tipos LEVE/GRAVE/CRÍTICA, bloqueo automático, expiración automática |
| 📊 **Dashboard Administrativo** | AdminLTE 3.2, gráficos Chart.js, métricas en tiempo real |
| 📈 **Estadísticas y Reportes** | Análisis por zona/recurso/usuario, exportación CSV |
| ⚙️ **Configuración Dinámica** | Horarios, duración de reservas, anticipación máxima |

---

## 📁 Estructura del Proyecto

El proyecto se organiza en las siguientes carpetas principales:

```
Proyecto_final_chill_zone/
│
├── 📂 SGCZ-ChillZone/              # 🚀 Aplicación principal Flask
│   ├── 📜 app.py                   # Punto de entrada de la aplicación
│   ├── 📜 config.py                # Configuración centralizada
│   ├── 📜 requirements.txt         # Dependencias Python
│   │
│   ├── 📂 controllers/             # 🎮 Controladores (rutas HTTP)
│   │   ├── auth_controller.py      # Autenticación y sesiones
│   │   ├── admin_controller.py     # Panel de administración
│   │   ├── reservas_controller.py  # Gestión de reservas
│   │   ├── recursos_controller.py  # CRUD de recursos
│   │   ├── incidencias_controller.py
│   │   ├── sanciones_controller.py
│   │   ├── zonas_controller.py
│   │   ├── reportes_controller.py
│   │   └── estadisticas_controller.py
│   │
│   ├── 📂 services/                # 🧠 Lógica de negocio
│   │   ├── auth_service.py         # Autenticación y recuperación
│   │   ├── reservas_service.py     # Reglas de reservas
│   │   ├── recursos_service.py     # Gestión de recursos
│   │   ├── sanciones_service.py    # Sistema de sanciones
│   │   ├── incidencias_service.py  # Gestión de incidencias
│   │   ├── estadisticas_service.py # Métricas y estadísticas
│   │   ├── metrics_service.py      # Dashboard admin
│   │   └── reportes_service.py     # Generación de reportes
│   │
│   ├── 📂 repositories/            # 💾 Acceso a datos (SQL)
│   │   ├── user_repository.py
│   │   ├── reserva_repository.py
│   │   ├── recurso_repository.py
│   │   ├── incidencia_repository.py
│   │   ├── sancion_repository.py
│   │   ├── zona_repository.py
│   │   ├── config_repository.py
│   │   └── uso_repository.py
│   │
│   ├── 📂 models/                  # 📋 Modelos de datos (dataclasses)
│   │   ├── user.py, reserva.py, recurso.py, incidencia.py, uso.py
│   │
│   ├── 📂 utils/                   # 🔧 Utilidades
│   │   ├── db.py                   # Pool de conexiones MySQL
│   │   ├── security.py             # Hash, tokens, decoradores
│   │   ├── validators.py           # Validaciones de datos
│   │   ├── logger.py               # Logging centralizado
│   │   ├── audit.py                # Auditoría de acciones
│   │   └── file_uploader.py        # Subida de archivos
│   │
│   ├── 📂 templates/               # 🎨 Plantillas Jinja2
│   │   ├── layouts/, auth/, admin/, reservas/, recursos/
│   │   ├── incidencias/, sanciones/, zonas/, estadisticas/, reportes/
│   │
│   ├── 📂 static/                  # 📦 Archivos estáticos
│   │   ├── css/custom.css, js/main.js, img/resources/, uploads/
│   │
│   ├── 📂 tests/                   # 🧪 Tests unitarios (pytest)
│   │
│   └── 📂 docs/                    # 📚 Documentación técnica
│
├── 📂 AdminLTE-3.2.0/              # Framework de UI
├── 📜 chill_zone_db.sql            # Script de base de datos
├── 📜 docker-compose.yml           # Orquestación Docker
├── 📜 dockerfile                   # Imagen Docker
└── 📜 LICENSE                      # Licencia MIT
```

---

## 🛠️ Tecnologías

### Backend
| Tecnología | Versión | Propósito |
|------------|---------|-----------|
| **Python** | 3.11+ | Lenguaje principal |
| **Flask** | 3.0.3 | Framework web |
| **MySQL Connector** | 9.0.0 | Conexión a base de datos |
| **bcrypt** | 4.2.0 | Hash seguro de contraseñas |
| **Flask-WTF** | 1.2.1 | Validación de formularios y CSRF |
| **python-dotenv** | 1.0.1 | Variables de entorno |

### Frontend
| Tecnología | Versión | Propósito |
|------------|---------|-----------|
| **Jinja2** | 3.1.6 | Motor de plantillas |
| **AdminLTE** | 3.2.0 | Interfaz administrativa |
| **Bootstrap** | 4.x | Framework CSS |
| **Chart.js** | - | Gráficos interactivos |
| **DataTables** | - | Tablas dinámicas |

### DevOps
| Tecnología | Propósito |
|------------|-----------|
| **Docker** | Containerización |
| **Docker Compose** | Orquestación de servicios |
| **pytest** | Testing automatizado |

---

## 🚀 Instalación

### Prerrequisitos

- **Python** 3.11 o superior
- **MySQL** 8.0 o superior
- **Git**
- (Opcional) **Docker** y **Docker Compose**

### Opción 1: Con Docker 🐳 (Recomendado)

```bash
# Clonar el repositorio
git clone https://github.com/jeremyja28/Proyecto_final_chill_zone.git
cd Proyecto_final_chill_zone

# Levantar los servicios (Flask + MySQL)
docker-compose up --build
```

🌐 **Acceder a la aplicación**: http://localhost:4000

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

---

### Opción 2: Instalación Manual

#### 1️⃣ Clonar el repositorio

```bash
git clone https://github.com/jeremyja28/Proyecto_final_chill_zone.git
cd Proyecto_final_chill_zone/SGCZ-ChillZone
```

#### 2️⃣ Crear entorno virtual

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/macOS
python3 -m venv venv
source venv/bin/activate
```

#### 3️⃣ Instalar dependencias

```bash
pip install -r requirements.txt
```

#### 4️⃣ Configurar variables de entorno

```bash
# Copiar archivo de ejemplo
cp .env.example .env

# Editar con tus credenciales
```

**Contenido de `.env`:**
```env
FLASK_ENV=development
SECRET_KEY=tu-clave-secreta-super-segura-cambiar-en-produccion

DB_HOST=localhost
DB_PORT=3306
DB_NAME=chill_zone_db
DB_USER=root
DB_PASSWORD=tu_password_mysql
```

#### 5️⃣ Restaurar la base de datos

```bash
mysql -u root -p < ../chill_zone_db.sql
```

#### 6️⃣ Ejecutar la aplicación

```bash
python app.py
```

🌐 **Acceder a la aplicación**: http://localhost:5000

---

### 🔑 Credenciales de Acceso por Defecto

| Rol | Usuario | Contraseña |
|-----|---------|------------|
| 👑 Administrador | `admin` | `admin123` |
| 👤 Usuario | `est1@pucesa.edu.ec` | `12345678` |

> ⚠️ **Importante**: Cambiar las contraseñas predeterminadas en producción.

---

## 🖼️ Capturas de Pantalla

### 🏠 Landing Page
<!-- TODO: Agregar captura de pantalla -->
![Landing Page](docs/screenshots/landing.png)

### 🔐 Inicio de Sesión
<!-- TODO: Agregar captura de pantalla -->
![Login](docs/screenshots/login.png)

### 📊 Dashboard Administrativo
<!-- TODO: Agregar captura de pantalla -->
![Dashboard Admin](docs/screenshots/dashboard_admin.png)

### 📅 Sistema de Reservas
<!-- TODO: Agregar captura de pantalla -->
![Reservas](docs/screenshots/reservas.png)

### 🗓️ Disponibilidad de Recursos
<!-- TODO: Agregar captura de pantalla -->
![Disponibilidad](docs/screenshots/disponibilidad.png)

---

## 🧪 Tests

Ejecutar la suite de tests con pytest:

```bash
cd SGCZ-ChillZone
pytest tests/ -v
```

---

## 📋 Casos de Uso Implementados

| ID | Caso de Uso | Estado |
|----|-------------|--------|
| CU-01 | Autenticación de usuarios | ✅ |
| CU-02 | Gestión de reservas | ✅ |
| CU-03 | Consulta de disponibilidad | ✅ |
| CU-04 | Cancelación de reservas | ✅ |
| CU-05 | Gestión de recursos | ✅ |
| CU-06 | Reporte de incidencias | ✅ |
| CU-07 | Gestión de sanciones | ✅ |
| CU-08 | Dashboard administrativo | ✅ |
| CU-09 | Estadísticas y reportes | ✅ |
| CU-10 | Gestión de zonas | ✅ |
| CU-11 | Configuración del sistema | ✅ |
| CU-12 | Auditoría de acciones | ✅ |
| CU-13 | Gestión de usuarios (Admin) | ✅ |
| CU-14 | Protección de eliminación de recursos | ✅ |

---

## 🗄️ Base de Datos

### Tablas Principales
| Tabla | Descripción |
|-------|-------------|
| `usuarios` | Información de usuarios (nombre, correo, contraseña, rol, estado) |
| `recursos` | Catálogo de ítems reservables (mesas, salas, equipos) |
| `reservas` | Registro central de reservas (quién, qué, cuándo) |
| `incidencias` | Reportes de problemas asociados a recursos |
| `sanciones` | Registro de penalizaciones aplicadas |
| `zonas` | Áreas macro donde se ubican los recursos |
| `config_sistema` | Variables de configuración dinámica |

### Arquitectura

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

---

## 🔮 Mejoras Futuras

- [ ] Implementación de notificaciones por correo electrónico
- [ ] Sistema de chat en tiempo real para usuarios
- [ ] Integración con calendarios externos (Google Calendar, Outlook)
- [ ] Aplicación móvil nativa (Android/iOS)
- [ ] Sistema de QR para check-in/check-out automático
- [ ] API RESTful documentada con Swagger

---

## 👥 Créditos

### Desarrollado por:

<table>
  <tr>
    <td align="center">
      <a href="https://github.com/jeremyja28">
        <img src="https://github.com/jeremyja28.png" width="100px;" alt="Jeremy"/><br />
        <sub><b>Jeremy Jácome</b></sub>
      </a>
    </td>
  </tr>
</table>

### Agradecimientos
- **AdminLTE** - Framework de dashboard administrativo
- **Flask Community** - Framework web ligero y extensible
- **PUCESA** - Institución educativa

---

## 📄 Licencia

Este proyecto está bajo la licencia **MIT**. Consulta el archivo [LICENSE](LICENSE) para más detalles.

---

<p align="center">
  <sub>Hecho con ❤️ para la gestión eficiente de espacios recreativos</sub>
</p>

<p align="center">
  <a href="#-chill-zone---sistema-de-gestión-de-zonas-recreativas">⬆️ Volver al inicio</a>
</p>
