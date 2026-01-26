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
  <a href="#-base-de-datos">Base de Datos</a>
</p>

---

## 📖 Descripción

El **Sistema de Gestión Chill Zone (SGCZ)** es una aplicación web integral diseñada para la administración y reserva de espacios recreativos y de trabajo colaborativo (Coworking) dentro de una institución. El sistema permite a los usuarios consultar la disponibilidad de recursos, realizar reservas y reportar incidencias. Para los administradores, ofrece herramientas para gestionar el inventario, controlar accesos, aplicar sanciones y configurar parámetros del sistema con altos estándares de seguridad.

### 🎯 Objetivos Principales
- 📅 **Reservas inteligentes** con validación de conflictos en tiempo real.
- 🛡️ **Seguridad Avanzada** con control de concurrencia (Optimistic Locking) y headers de seguridad.
- 📊 **Dashboard analítico** con métricas de uso y estadísticas.
- 🔐 **Control de acceso** basado en roles (Usuario/Administrador).
- 📱 **Diseño responsivo** completamente funcional en móviles.

---

## ✨ Características Principales

| Módulo | Descripción |
|--------|-------------|
| 🔐 **Seguridad y Auditoría** | Autenticación robusta, RBAC estricto, **Bloqueo Optimista** para prevenir conflictos de edición, auditoría de acciones, protección CSRF y headers de seguridad (HSTS, X-Frame-Options). |
| 📅 **Sistema de Reservas** | Reservas en tiempo real, detección automática de conflictos, gestión de acompañantes, cancelación automática por mantenimiento o sanciones. |
| 🏢 **Gestión de Zonas y Recursos** | CRUD completo con validación de integridad, estados de mantenimiento programado, inhabilitación en cascada (Zona -> Recursos -> Reservas). |
| 🛠️ **Incidencias** | Reportes detallados con evidencia multimedia, asignación de responsables y seguimiento de estado. |
| ⚠️ **Sanciones** | Sistema de penalización con puntos, tipos (LEVE/GRAVE/CRÍTICA) y bloqueo automático de reservas. |
| 📊 **Dashboard Administrativo** | AdminLTE 3.2, gráficos Chart.js, métricas en tiempo real de ocupación y uso. |
| 📈 **Reportes y Estadísticas** | Análisis detallado por recurso/zona, historial de uso, tiempos de ocupación, exportación de datos. |
| ⚙️ **Configuración Dinámica** | Ajuste en caliente de horarios, duración de reservas y ventanas de anticipación. |

---

## 📁 Estructura del Proyecto

El proyecto se organiza en las siguientes carpetas principales:

```
Proyecto_final_chill_zone/
│
├── 📂 SGCZ-ChillZone/              # 🚀 Aplicación principal Flask
│   ├── 📜 app.py                   # Punto de entrada de la aplicación
│   ├── 📜 config.py                # Configuración centralizada y seguridad
│   ├── 📜 requirements.txt         # Dependencias Python
│   │
│   ├── 📂 controllers/             # 🎮 Controladores (Blueprints)
│   │   ├── auth_controller.py      # Autenticación
│   │   ├── admin_controller.py     # Panel Admin
│   │   ├── reservas_controller.py  # Lógica de reservas
│   │   ├── recursos_controller.py  # Gestión de recursos
│   │   ├── zonas_controller.py     # Gestión de zonas
│   │   └── ... (otros controladores)
│   │
│   ├── 📂 services/                # 🧠 Lógica de Negocio
│   │   ├── reservas_service.py     # Reglas complejas de reserva
│   │   ├── recursos_service.py     # Gestión de recursos con checksum
│   │   ├── zonas_service.py        # Gestión de zonas con checksum
│   │   └── ... (otros servicios)
│   │
│   ├── 📂 repositories/            # 💾 Capa de Datos (SQL)
│   │   ├── user_repository.py
│   │   ├── reserva_repository.py
│   │   ├── recurso_repository.py
│   │   └── ... (otros repositorios)
│   │
│   ├── 📂 models/                  # 📋 Definición de Modelos
│   │
│   ├── 📂 utils/                   # 🔧 Utilidades Transversales
│   │   ├── security_utils.py       # Hashing y control de concurrencia
│   │   ├── db.py                   # Pool MySQL
│   │   ├── security.py             # Decoradores RBAC
│   │   └── ...
│   │
│   ├── 📂 templates/               # 🎨 Vistas (Jinja2 + AdminLTE)
│   ├── 📂 static/                  # 📦 Assets (CSS, JS, Imágenes)
│   │
│   └── 📂 docs/                    # 📚 Documentación
│
├── 📂 AdminLTE-3.2.0/              # Framework UI Base
├── 📜 chill_zone_db.sql            # Script DDL/DML Base de Datos
├── 📜 docker-compose.yml           # Despliegue Docker
└── 📜 LICENSE                      # Licencia
```

---

## 🛠️ Tecnologías

### Backend
| Tecnología | Versión | Propósito |
|------------|---------|-----------|
| **Python** | 3.11+ | Lenguaje principal |
| **Flask** | 3.0.3 | Framework web |
| **MySQL Connector** | 9.0.0 | Driver de base de datos |
| **bcrypt** | 4.2.0 | Hashing de contraseñas |
| **Flask-WTF** | 1.2.1 | Formularios y protección CSRF |

### Frontend
| Tecnología | Versión | Propósito |
|------------|---------|-----------|
| **Jinja2** | 3.1.6 | Renderizado de motor |
| **AdminLTE** | 3.2.0 | Interfaz de usuario responsiva |
| **Bootstrap** | 4.6 | Sistema de grillas y componentes |
| **jQuery** | 3.x | Manipulación DOM y AJAX |

---

## 🚀 Instalación

### Prerrequisitos
- **Python** 3.11+
- **MySQL** 8.0+
- **Git**

### Instalación Manual

1.  **Clonar el repositorio**
    ```bash
    git clone https://github.com/jeremyja28/Proyecto_final_chill_zone.git
    cd Proyecto_final_chill_zone/SGCZ-ChillZone
    ```

2.  **Configurar entorno virtual**
    ```bash
    python -m venv venv
    # Windows:
    venv\Scripts\activate
    # Linux/Mac:
    source venv/bin/activate
    ```

3.  **Instalar dependencias**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Configurar Base de Datos**
    - Importar el script `chill_zone_db.sql` en MySQL.
    - Configurar variables de entorno en `.env`:
    ```env
    DB_HOST=localhost
    DB_USER=root
    DB_PASSWORD=tu_password
    DB_NAME=chill_zone_db
    SECRET_KEY=clave_segura
    ```

5.  **Ejecutar**
    ```bash
    python app.py
    ```

Acceder en `http://localhost:5000`

---

## 📋 Casos de Uso Implementados

| ID | Caso de Uso | Estado |
|----|-------------|--------|
| CU-01 | Autenticación y Autorización | ✅ |
| CU-02 | Gestión de Perfil de Usuario | ✅ |
| CU-03 | Visualización de Disponibilidad | ✅ |
| CU-04 | Crear Reserva (Individual/Grupal) | ✅ |
| CU-05 | Cancelar Reserva | ✅ |
| CU-06 | Gestión de Recursos (Admin) | ✅ |
| CU-07 | Gestión de Zonas (Admin) | ✅ |
| CU-08 | Reporte y Gestión de Incidencias | ✅ |
| CU-09 | Aplicación de Sanciones | ✅ |
| CU-10 | Panel de Estadísticas | ✅ |
| CU-11 | Auditoría de Seguridad | ✅ |
| CU-12 | Configuración del Sistema | ✅ |

---

## 🗄️ Base de Datos

El sistema utiliza una base de datos relacional MySQL con la siguiente estructura normalizada:

### Tablas Principales

| Tabla | Descripción |
|-------|-------------|
| **usuarios** | Almacena credenciales, roles y estado de los usuarios. |
| **zonas** | Áreas físicas (ej. Chill Zone, Coworking) que agrupan recursos. |
| **recursos** | Ítems reservables con control de estado, mantenimiento y stock. |
| **reservas** | Registro transaccional de reservas. Estados: PENDIENTE, ACTIVA, FINALIZADA, CANCELADA. |
| **reserva_acompanantes** | Detalle de usuarios adicionales en una reserva grupal. |
| **incidencias** | Reportes de daños o problemas, con evidencia adjunta. |
| **incidencia_responsables** | Usuarios asignados o responsables de una incidencia. |
| **sanciones** | Historial de penalizaciones aplicadas por administradores. |
| **uso** | Registro de tiempos reales de ocupación de recursos. |
| **config_sistema** | Parámetros globales configurables (horarios, límites, timeouts). |

### Vistas
- **v_disponibilidad**: Vista optimizada para consultar disponibilidad de recursos en tiempo real y calcular franjas horarias ocupadas.

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
- **AdminLTE** - Framework UI
- **Flask Community**
- **PUCESA**

---

## 📄 Licencia

Este proyecto está bajo la licencia **MIT**. Consulta el archivo [LICENSE](LICENSE) para más detalles.

---

<p align="center">
  <sub>Hecho con ❤️ para la gestión eficiente de espacios recreativos</sub>
</p>
