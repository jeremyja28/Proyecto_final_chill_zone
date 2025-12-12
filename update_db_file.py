
content = r"""-- phpMyAdmin SQL Dump
-- version 5.2.0
-- https://www.phpmyadmin.net/
--
-- Host: localhost:3307
-- Generation Time: Dec 05, 2025 at 04:39 PM
-- Server version: 8.0.30
-- PHP Version: 8.1.10

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";
SET FOREIGN_KEY_CHECKS = 0;


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `chill_zone_db`
--
CREATE DATABASE IF NOT EXISTS `chill_zone_db` DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE `chill_zone_db`;

-- --------------------------------------------------------
-- Table structure for table `config_sistema`
-- --------------------------------------------------------
CREATE TABLE `config_sistema` (
  `id` int NOT NULL,
  `nombre` varchar(80) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `valor` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `actualizado_en` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------
-- Table structure for table `incidencias`
-- --------------------------------------------------------
CREATE TABLE `incidencias` (
  `id` int NOT NULL,
  `recurso_id` int NOT NULL,
  `usuario_id` int NOT NULL,
  `reserva_id` int DEFAULT NULL,
  `descripcion` text CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `evidencia_url` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `estado` enum('PENDIENTE','REVISADA') CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT 'PENDIENTE',
  `creado_en` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------
-- Table structure for table `incidencia_responsables`
-- --------------------------------------------------------
CREATE TABLE `incidencia_responsables` (
  `id` int NOT NULL,
  `incidencia_id` int NOT NULL,
  `usuario_id` int NOT NULL,
  `creado_en` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------
-- Table structure for table `recursos`
-- --------------------------------------------------------
CREATE TABLE `recursos` (
  `id` int NOT NULL,
  `zona_id` int NOT NULL,
  `nombre` varchar(150) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `tipo` enum('SALA','MESA','JUEGO','EQUIPO','OTRO') CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT 'OTRO',
  `descripcion` text CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci,
  `ubicacion` varchar(150) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `cantidad_total` int NOT NULL DEFAULT '1',
  `estado` enum('DISPONIBLE','EN_MANTENIMIENTO','FUERA_DE_SERVICIO') CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT 'DISPONIBLE',
  `eliminado` tinyint(1) NOT NULL DEFAULT '0',
  `mantenimiento_inicio` datetime DEFAULT NULL COMMENT 'Inicio del periodo de mantenimiento',
  `mantenimiento_fin` datetime DEFAULT NULL COMMENT 'Fin del periodo de mantenimiento',
  `creado_en` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------
-- Table structure for table `reservas`
-- --------------------------------------------------------
CREATE TABLE `reservas` (
  `id` int NOT NULL,
  `usuario_id` int NOT NULL,
  `recurso_id` int DEFAULT NULL,
  `fecha` date NOT NULL,
  `hora_inicio` time NOT NULL,
  `hora_fin` time NOT NULL,
  `cantidad` int NOT NULL DEFAULT '1',
  `estado` enum('PENDIENTE','ACTIVA','CANCELADA','FINALIZADA','CANCELADA_MANTENIMIENTO','CANCELADA_SANCION') CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT 'PENDIENTE',
  `creado_en` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------
-- Table structure for table `reserva_acompanantes`
-- --------------------------------------------------------
CREATE TABLE `reserva_acompanantes` (
  `id` int NOT NULL,
  `reserva_id` int NOT NULL,
  `usuario_id` int NOT NULL,
  `creado_en` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------
-- Table structure for table `sanciones`
-- --------------------------------------------------------
CREATE TABLE `sanciones` (
  `id` int NOT NULL,
  `usuario_id` int NOT NULL,
  `creado_por` int NOT NULL,
  `motivo` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `tipo` enum('LEVE','GRAVE','CRITICA') CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT 'LEVE',
  `puntos` int NOT NULL DEFAULT '1',
  `estado` enum('ACTIVA','LEVANTADA') CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT 'ACTIVA',
  `creado_en` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------
-- Table structure for table `uso`
-- --------------------------------------------------------
CREATE TABLE `uso` (
  `id` int NOT NULL,
  `reserva_id` int NOT NULL,
  `hora_inicio` datetime NOT NULL,
  `hora_fin` datetime DEFAULT NULL,
  `duracion_min` int DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------
-- Table structure for table `usuarios`
-- --------------------------------------------------------
CREATE TABLE `usuarios` (
  `id` int NOT NULL,
  `nombre` varchar(120) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `correo` varchar(120) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `hash_password` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `rol` enum('ESTUDIANTE','ADMIN') CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT 'ESTUDIANTE',
  `estado` enum('ACTIVO','BLOQUEADO') CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT 'ACTIVO',
  `creado_en` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------
-- Table structure for table `zonas`
-- --------------------------------------------------------
CREATE TABLE `zonas` (
  `id` int NOT NULL,
  `nombre` varchar(120) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `descripcion` text CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci,
  `creado_en` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `incidencias`
--

INSERT INTO `incidencias` (`id`, `recurso_id`, `usuario_id`, `descripcion`, `evidencia_url`, `estado`, `creado_en`) VALUES
(1, 3, 1, 'Raqueta rota', NULL, 'REVISADA', '2025-11-22 16:44:38'),
(2, 4, 2, 'esta rota la mesa', NULL, 'REVISADA', '2025-11-22 18:19:11'),
(3, 1, 2, 'hola mundo.txt', '/static/uploads/incidencias/20251124_080551_rayo.png', 'PENDIENTE', '2025-11-24 13:05:51'),
(4, 3, 2, 'esta rota la mesa', NULL, 'PENDIENTE', '2025-11-24 13:48:29'),
(5, 4, 1, 'asdfghj', '/static/uploads/incidencias/20251203_104312_rayo.png', 'PENDIENTE', '2025-12-03 15:43:12'),
(6, 1, 2, 'prueba xdddddd', NULL, 'PENDIENTE', '2025-12-05 16:34:48');

-- --------------------------------------------------------
-- Indexes and Primary Keys
-- --------------------------------------------------------

ALTER TABLE `config_sistema`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `nombre` (`nombre`);

ALTER TABLE `incidencias`
  ADD PRIMARY KEY (`id`),
  ADD KEY `fk_incidencia_recurso` (`recurso_id`),
  ADD KEY `fk_incidencia_usuario` (`usuario_id`),
  ADD KEY `fk_incidencia_reserva` (`reserva_id`);

ALTER TABLE `incidencia_responsables`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `unique_incidencia_usuario` (`incidencia_id`,`usuario_id`),
  ADD KEY `idx_incidencia_responsables_usuario` (`usuario_id`);

ALTER TABLE `recursos`
  ADD PRIMARY KEY (`id`),
  ADD KEY `idx_recursos_zona` (`zona_id`),
  ADD KEY `idx_recursos_estado` (`estado`),
  ADD KEY `idx_recursos_eliminado` (`eliminado`),
  ADD KEY `idx_recursos_zona_tipo` (`zona_id`,`tipo`),
  ADD KEY `idx_recursos_mant_periodo` (`mantenimiento_inicio`,`mantenimiento_fin`);

ALTER TABLE `reservas`
  ADD PRIMARY KEY (`id`),
  ADD KEY `idx_reservas_recurso_fecha` (`recurso_id`,`fecha`),
  ADD KEY `idx_reservas_usuario_fecha` (`usuario_id`,`fecha`),
  ADD KEY `idx_reservas_estado` (`estado`),
  ADD KEY `idx_reservas_fecha_hora` (`fecha`,`hora_inicio`,`hora_fin`);

ALTER TABLE `reserva_acompanantes`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `unique_reserva_usuario` (`reserva_id`,`usuario_id`),
  ADD KEY `idx_reserva_acompanantes_usuario` (`usuario_id`);

ALTER TABLE `sanciones`
  ADD PRIMARY KEY (`id`),
  ADD KEY `fk_sancion_admin` (`creado_por`),
  ADD KEY `idx_sanciones_usuario` (`usuario_id`),
  ADD KEY `idx_sanciones_estado` (`estado`);

ALTER TABLE `uso`
  ADD PRIMARY KEY (`id`),
  ADD KEY `fk_uso_reserva` (`reserva_id`),
  ADD KEY `idx_uso_inicio` (`hora_inicio`);

ALTER TABLE `usuarios`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `correo` (`correo`);

ALTER TABLE `zonas`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `nombre` (`nombre`);

-- --------------------------------------------------------
-- AUTO_INCREMENT
-- --------------------------------------------------------

ALTER TABLE `config_sistema` MODIFY `id` int NOT NULL AUTO_INCREMENT;
ALTER TABLE `incidencias` MODIFY `id` int NOT NULL AUTO_INCREMENT;
ALTER TABLE `incidencia_responsables` MODIFY `id` int NOT NULL AUTO_INCREMENT;
ALTER TABLE `recursos` MODIFY `id` int NOT NULL AUTO_INCREMENT;
ALTER TABLE `reservas` MODIFY `id` int NOT NULL AUTO_INCREMENT;
ALTER TABLE `reserva_acompanantes` MODIFY `id` int NOT NULL AUTO_INCREMENT;
ALTER TABLE `sanciones` MODIFY `id` int NOT NULL AUTO_INCREMENT;
ALTER TABLE `uso` MODIFY `id` int NOT NULL AUTO_INCREMENT;
ALTER TABLE `usuarios` MODIFY `id` int NOT NULL AUTO_INCREMENT;
ALTER TABLE `zonas` MODIFY `id` int NOT NULL AUTO_INCREMENT;

-- --------------------------------------------------------
-- Foreign Keys
-- --------------------------------------------------------

ALTER TABLE `incidencias`
  ADD CONSTRAINT `fk_incidencia_recurso` FOREIGN KEY (`recurso_id`) REFERENCES `recursos` (`id`),
  ADD CONSTRAINT `fk_incidencia_usuario` FOREIGN KEY (`usuario_id`) REFERENCES `usuarios` (`id`),
  ADD CONSTRAINT `fk_incidencia_reserva` FOREIGN KEY (`reserva_id`) REFERENCES `reservas` (`id`);

ALTER TABLE `incidencia_responsables`
  ADD CONSTRAINT `fk_responsable_incidencia` FOREIGN KEY (`incidencia_id`) REFERENCES `incidencias` (`id`) ON DELETE CASCADE,
  ADD CONSTRAINT `fk_responsable_usuario` FOREIGN KEY (`usuario_id`) REFERENCES `usuarios` (`id`) ON DELETE CASCADE;

ALTER TABLE `recursos`
  ADD CONSTRAINT `fk_recurso_zona` FOREIGN KEY (`zona_id`) REFERENCES `zonas` (`id`) ON DELETE RESTRICT;

ALTER TABLE `reservas`
  ADD CONSTRAINT `fk_reserva_recurso` FOREIGN KEY (`recurso_id`) REFERENCES `recursos` (`id`),
  ADD CONSTRAINT `fk_reserva_usuario` FOREIGN KEY (`usuario_id`) REFERENCES `usuarios` (`id`);

ALTER TABLE `reserva_acompanantes`
  ADD CONSTRAINT `fk_acompanante_reserva` FOREIGN KEY (`reserva_id`) REFERENCES `reservas` (`id`) ON DELETE CASCADE,
  ADD CONSTRAINT `fk_acompanante_usuario` FOREIGN KEY (`usuario_id`) REFERENCES `usuarios` (`id`) ON DELETE CASCADE;

ALTER TABLE `sanciones`
  ADD CONSTRAINT `fk_sancion_admin` FOREIGN KEY (`creado_por`) REFERENCES `usuarios` (`id`),
  ADD CONSTRAINT `fk_sancion_usuario` FOREIGN KEY (`usuario_id`) REFERENCES `usuarios` (`id`);

ALTER TABLE `uso`
  ADD CONSTRAINT `fk_uso_reserva` FOREIGN KEY (`reserva_id`) REFERENCES `reservas` (`id`) ON DELETE CASCADE;

SET FOREIGN_KEY_CHECKS = 1;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
"""

with open(r"c:\Users\chanc\OneDrive\Escritorio\Trabajos_U_quinto_semestre\Ingenieria_de_software\Proyecto_final_chill_zone\chill_zone_db.sql", "w", encoding="utf-8") as f:
    f.write(content)
