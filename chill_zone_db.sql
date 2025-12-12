-- phpMyAdmin SQL Dump
-- version 5.2.0
-- https://www.phpmyadmin.net/
--
-- Host: localhost:3307
-- Generation Time: Dec 11, 2025 at 02:44 AM
-- Server version: 8.0.30
-- PHP Version: 8.1.10

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `chill_zone_db`
CREATE DATABASE IF NOT EXISTS `chill_zone_db` DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE `chill_zone_db`;

-- --------------------------------------------------------
--

-- --------------------------------------------------------

--
-- Table structure for table `config_sistema`
--

CREATE TABLE `config_sistema` (
  `id` int NOT NULL,
  `nombre` varchar(80) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `valor` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `actualizado_en` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `config_sistema`
--

INSERT INTO `config_sistema` (`id`, `nombre`, `valor`, `actualizado_en`) VALUES
(1, 'csrf_token', 'IjlkMzBlYTUwMDhlYzIzMzE0YzcwYmNlY2Y0Mzc0YzM4ZjZlOGNkYmIi.aTmMfg.fVRpvTPzWQGzvtJ6k4zD605X34w', '2025-12-10 15:12:24'),
(2, 'horario_inicio', '07:00', '2025-12-10 15:12:24'),
(3, 'horario_fin', '22:00', '2025-12-10 15:12:24'),
(4, 'reserva_anticipacion_max_dias', '6', '2025-12-10 15:12:24'),
(5, 'reserva_duracion_min_min', '15', '2025-12-10 15:12:24'),
(6, 'reserva_duracion_max_min', '120', '2025-12-10 15:12:24');

-- --------------------------------------------------------

--
-- Table structure for table `incidencias`
--

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

--
-- Dumping data for table `incidencias`
--

INSERT INTO `incidencias` (`id`, `recurso_id`, `usuario_id`, `reserva_id`, `descripcion`, `evidencia_url`, `estado`, `creado_en`) VALUES
(1, 3, 1, NULL, 'Raqueta rota', NULL, 'REVISADA', '2025-11-22 16:44:38'),
(2, 4, 2, NULL, 'esta rota la mesa', NULL, 'REVISADA', '2025-11-22 18:19:11'),
(3, 1, 2, NULL, 'hola mundo.txt', '/static/uploads/incidencias/20251124_080551_rayo.png', 'REVISADA', '2025-11-24 13:05:51'),
(4, 3, 2, NULL, 'esta rota la mesa', NULL, 'REVISADA', '2025-11-24 13:48:29'),
(5, 1, 1, 13, 'prueba xdddddd', NULL, 'REVISADA', '2025-12-07 17:01:35'),
(6, 1, 1, 13, 'asdfghjklñ', NULL, 'REVISADA', '2025-12-10 14:46:11'),
(7, 1, 1, 13, 'asdfghjklñ', '/static/uploads/incidencias/20251210_094632_rayo.jpg', 'REVISADA', '2025-12-10 14:46:32');

-- --------------------------------------------------------

--
-- Table structure for table `incidencia_responsables`
--

CREATE TABLE `incidencia_responsables` (
  `id` int NOT NULL,
  `incidencia_id` int NOT NULL,
  `usuario_id` int NOT NULL,
  `creado_en` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `incidencia_responsables`
--

INSERT INTO `incidencia_responsables` (`id`, `incidencia_id`, `usuario_id`, `creado_en`) VALUES
(1, 3, 4, '2025-11-24 13:05:51'),
(2, 4, 2, '2025-11-24 13:48:29'),
(3, 5, 3, '2025-12-07 17:01:35'),
(4, 5, 4, '2025-12-07 17:01:35'),
(5, 5, 2, '2025-12-07 17:01:35'),
(6, 6, 3, '2025-12-10 14:46:11'),
(7, 7, 4, '2025-12-10 14:46:32');

-- --------------------------------------------------------

--
-- Table structure for table `recursos`
--

CREATE TABLE `recursos` (
  `id` int NOT NULL,
  `zona_id` int NOT NULL,
  `nombre` varchar(150) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `tipo` enum('SALA','MESA','JUEGO','EQUIPO','OTRO') CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT 'OTRO',
  `descripcion` text CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci,
  `ubicacion` varchar(150) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `imagen_url` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `cantidad_total` int NOT NULL DEFAULT '1',
  `estado` enum('DISPONIBLE','EN_MANTENIMIENTO','FUERA_DE_SERVICIO') CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT 'DISPONIBLE',
  `eliminado` tinyint(1) NOT NULL DEFAULT '0',
  `mantenimiento_inicio` datetime DEFAULT NULL COMMENT 'Inicio del periodo de mantenimiento',
  `mantenimiento_fin` datetime DEFAULT NULL COMMENT 'Fin del periodo de mantenimiento',
  `creado_en` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `recursos`
--

INSERT INTO `recursos` (`id`, `zona_id`, `nombre`, `tipo`, `descripcion`, `ubicacion`, `imagen_url`, `cantidad_total`, `estado`, `eliminado`, `mantenimiento_inicio`, `mantenimiento_fin`, `creado_en`) VALUES
(1, 1, 'Futbolín A', 'JUEGO', 'Mesa de futbolín', 'Chill Zone', '/static/img/resources/Chill_zone_futbolin_A.jpg', 1, 'DISPONIBLE', 0, NULL, NULL, '2025-11-04 02:42:05'),
(2, 1, 'Futbolín B', 'JUEGO', 'Mesa de futbolín', 'Chill Zone', '/static/img/resources/Chill_zone_futbolin_B.jpg', 1, 'DISPONIBLE', 0, NULL, NULL, '2025-11-04 02:42:05'),
(3, 1, 'Mesa de Ping Pong', 'MESA', 'Mesa oficial de ping pong', 'Chill Zone', '/static/img/resources/Chill_zone_ping_pong.jpg', 1, 'DISPONIBLE', 0, NULL, NULL, '2025-11-04 02:42:05'),
(4, 1, 'Mesa Juegos de Mesa', 'MESA', 'Mesa con juegos de mesa', 'Chill Zone', '/static/img/resources/Coworking_B.jpg', 1, 'DISPONIBLE', 0, NULL, NULL, '2025-11-04 02:42:05'),
(5, 2, 'Coworking Sala 1', 'SALA', 'Sala para 4 personas', 'Coworking', '/static/img/resources/Coworking_A.jpg', 1, 'DISPONIBLE', 0, NULL, NULL, '2025-11-04 02:42:05'),
(6, 2, 'Coworking Sala 2', 'SALA', 'Sala para 4 personas', 'Coworking', '/static/img/resources/Coworking_B.jpg', 1, 'DISPONIBLE', 0, NULL, NULL, '2025-11-04 02:42:05'),
(7, 2, 'Coworking Sala 3', 'SALA', 'Sala para 6 personas', 'Coworking', '/static/img/resources/Coworking_C.jpg', 1, 'DISPONIBLE', 0, NULL, NULL, '2025-11-04 02:42:05'),
(8, 2, 'Coworking Sala 4', 'SALA', 'Sala para 6 personas', 'Coworking', '/static/img/resources/Coworking_D.jpg', 1, 'DISPONIBLE', 0, NULL, NULL, '2025-11-04 02:42:05');

-- --------------------------------------------------------

--
-- Table structure for table `reservas`
--

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

--
-- Dumping data for table `reservas`
--

INSERT INTO `reservas` (`id`, `usuario_id`, `recurso_id`, `fecha`, `hora_inicio`, `hora_fin`, `cantidad`, `estado`, `creado_en`) VALUES
(1, 2, 3, '2025-11-03', '10:00:00', '11:00:00', 1, 'FINALIZADA', '2025-11-04 02:42:05'),
(2, 2, 1, '2025-11-03', '09:00:00', '09:30:00', 1, 'FINALIZADA', '2025-11-04 02:42:05'),
(3, 2, 3, '2025-11-18', '14:00:00', '21:00:00', 1, 'CANCELADA', '2025-11-15 17:17:59'),
(4, 2, 1, '2025-11-15', '08:30:00', '09:00:00', 1, 'FINALIZADA', '2025-11-15 17:35:20'),
(5, 2, 1, '2025-11-17', '07:00:00', '07:15:00', 1, 'FINALIZADA', '2025-11-17 12:27:02'),
(6, 2, 3, '2025-11-17', '07:00:00', '07:45:00', 1, 'FINALIZADA', '2025-11-17 12:52:26'),
(7, 2, 2, '2025-11-17', '10:00:00', '11:15:00', 1, 'CANCELADA', '2025-11-17 12:54:52'),
(8, 2, 3, '2025-11-17', '10:00:00', '11:15:00', 1, 'FINALIZADA', '2025-11-17 12:55:25'),
(9, 1, 4, '2025-11-22', '19:00:00', '20:15:00', 1, 'CANCELADA', '2025-11-22 18:10:08'),
(10, 1, 4, '2025-11-22', '13:30:00', '13:45:00', 1, 'FINALIZADA', '2025-11-22 18:12:51'),
(11, 2, 4, '2025-11-22', '13:45:00', '14:00:00', 1, 'FINALIZADA', '2025-11-22 18:18:45'),
(12, 1, 8, '2025-11-24', '07:00:00', '07:30:00', 1, 'CANCELADA', '2025-11-23 22:21:44'),
(13, 2, 1, '2025-11-24', '08:00:00', '08:30:00', 1, 'FINALIZADA', '2025-11-23 22:27:21'),
(14, 2, 1, '2025-11-24', '08:30:00', '10:15:00', 1, 'CANCELADA', '2025-11-24 13:03:34'),
(15, 1, 1, '2025-12-08', '13:15:00', '14:30:00', 1, 'CANCELADA', '2025-12-07 17:10:56'),
(16, 2, 1, '2025-12-10', '10:00:00', '11:00:00', 1, 'CANCELADA', '2025-12-10 14:42:01'),
(17, 2, 1, '2025-12-10', '10:00:00', '11:00:00', 1, 'CANCELADA', '2025-12-10 14:44:18'),
(18, 2, 1, '2025-12-10', '11:00:00', '12:00:00', 1, 'CANCELADA_MANTENIMIENTO', '2025-12-10 15:32:30'),
(19, 2, 1, '2025-12-10', '13:00:00', '14:00:00', 1, 'FINALIZADA', '2025-12-10 15:36:17'),
(20, 2, 7, '2025-12-10', '14:00:00', '15:00:00', 1, 'FINALIZADA', '2025-12-10 15:37:10'),
(21, 3, 6, '2025-12-10', '12:30:00', '13:45:00', 1, 'FINALIZADA', '2025-12-10 15:39:04'),
(22, 3, 7, '2025-12-10', '15:00:00', '16:15:00', 1, 'FINALIZADA', '2025-12-10 15:39:24'),
(23, 4, 4, '2025-12-10', '21:15:00', '21:45:00', 1, 'CANCELADA', '2025-12-11 00:08:10');

-- --------------------------------------------------------

--
-- Table structure for table `reserva_acompanantes`
--

CREATE TABLE `reserva_acompanantes` (
  `id` int NOT NULL,
  `reserva_id` int NOT NULL,
  `usuario_id` int NOT NULL,
  `creado_en` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `reserva_acompanantes`
--

INSERT INTO `reserva_acompanantes` (`id`, `reserva_id`, `usuario_id`, `creado_en`) VALUES
(1, 12, 4, '2025-11-23 22:21:44'),
(2, 12, 3, '2025-11-23 22:21:44'),
(3, 13, 3, '2025-11-23 22:27:21'),
(4, 13, 4, '2025-11-23 22:27:21'),
(5, 14, 3, '2025-11-24 13:03:34'),
(6, 15, 4, '2025-12-07 17:10:56'),
(7, 16, 5, '2025-12-10 14:42:01'),
(8, 17, 4, '2025-12-10 14:44:18'),
(9, 18, 4, '2025-12-10 15:32:30'),
(10, 19, 4, '2025-12-10 15:36:17'),
(11, 20, 3, '2025-12-10 15:37:10'),
(12, 23, 5, '2025-12-11 00:08:10');

-- --------------------------------------------------------

--
-- Table structure for table `sanciones`
--

CREATE TABLE `sanciones` (
  `id` int NOT NULL,
  `usuario_id` int NOT NULL,
  `creado_por` int NOT NULL,
  `incidencia_id` int DEFAULT NULL,
  `motivo` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `tipo` enum('LEVE','GRAVE','CRITICA') CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT 'LEVE',
  `puntos` int NOT NULL DEFAULT '1',
  `estado` enum('ACTIVA','LEVANTADA') CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT 'ACTIVA',
  `levantada_en` timestamp NULL DEFAULT NULL,
  `creado_en` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `sanciones`
--

INSERT INTO `sanciones` (`id`, `usuario_id`, `creado_por`, `incidencia_id`, `motivo`, `tipo`, `puntos`, `estado`, `levantada_en`, `creado_en`) VALUES
(1, 5, 1, NULL, 'Dejar demasiado sucio el area de coworking sala A', 'LEVE', 1, 'LEVANTADA', NULL, '2025-11-22 17:38:50'),
(2, 3, 1, NULL, 'SANCION', 'CRITICA', 1, 'LEVANTADA', NULL, '2025-11-24 13:09:04'),
(3, 6, 6, NULL, 'prueba', 'CRITICA', 1, 'LEVANTADA', NULL, '2025-11-24 13:30:43'),
(4, 5, 1, NULL, 'porque si', 'GRAVE', 1, 'LEVANTADA', NULL, '2025-11-24 13:47:27'),
(5, 3, 1, NULL, 'prueba xd', 'LEVE', 1, 'LEVANTADA', NULL, '2025-12-07 17:13:45'),
(6, 3, 1, NULL, 'SANCION', 'LEVE', 1, 'LEVANTADA', '2025-12-10 14:47:08', '2025-12-07 17:14:04');

-- --------------------------------------------------------

--
-- Table structure for table `uso`
--

CREATE TABLE `uso` (
  `id` int NOT NULL,
  `reserva_id` int NOT NULL,
  `hora_inicio` datetime NOT NULL,
  `hora_fin` datetime DEFAULT NULL,
  `duracion_min` int DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `uso`
--

INSERT INTO `uso` (`id`, `reserva_id`, `hora_inicio`, `hora_fin`, `duracion_min`) VALUES
(1, 2, '2025-11-03 09:00:00', '2025-11-03 09:25:00', 25);

-- --------------------------------------------------------

--
-- Table structure for table `usuarios`
--

CREATE TABLE `usuarios` (
  `id` int NOT NULL,
  `nombre` varchar(60) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `apellido` varchar(60) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `correo` varchar(120) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `hash_password` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `rol` enum('USUARIO','ADMIN') CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT 'USUARIO',
  `estado` enum('ACTIVO','BLOQUEADO') CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT 'ACTIVO',
  `creado_en` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `imagen_url` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `usuarios`
--

INSERT INTO `usuarios` (`id`, `nombre`, `apellido`, `correo`, `hash_password`, `rol`, `estado`, `creado_en`, `imagen_url`) VALUES
(1, 'Administrador', 'Sistema', 'admin', '$2b$12$w.t3qpR4XV11YTN55kqkbOQfeSfPFBnAhqPZfh/mH5n6RncF4mvnu', 'ADMIN', 'ACTIVO', '2025-11-04 02:42:05', '/static/uploads/perfiles/user_1_rayo.jpg'),
(2, 'Estudiante', 'Uno', 'estu1@pucesa.edu.ec', '$2b$12$x30Zpu95kBQ0ec0l9oj.AOvOUvAcjseOHyNYJEQHlVu2JfIq5B4jq', 'USUARIO', 'ACTIVO', '2025-11-04 02:42:05', '/static/uploads/perfiles/user_2_rayo.jpg'),
(3, 'Carlos', 'Parreño', 'carlos@pucesa.edu.ec', '$2b$12$1dKm.lqsUrZXE0y24G2Q8.DZV1TICPQ3ynGngahTgOiWQ6gIuB/0O', 'USUARIO', 'ACTIVO', '2025-11-22 16:42:08', NULL),
(4, 'Alberto', 'Falconi', 'beto@pucesa.edu.ec', '$2b$12$SbM0s2KgBKW/Uppilt3AqOqIfoAJUPbwxbKOHRYOf0f5Nya4xwxBO', 'USUARIO', 'ACTIVO', '2025-11-22 17:37:24', NULL),
(5, 'Estudiante', 'prueba2', 'estu2@pucesa.edu.ec', '$2b$12$Fuz6US.mWXLs3V7uuMaP4uCYrA6y.vVJV8VNba1..gJy8f2xVxlT6', 'USUARIO', 'ACTIVO', '2025-11-22 17:38:18', '/static/uploads/perfiles/user_5_rayo.jpg'),
(6, 'admin2', 'User', 'admin2@gmail.com', '$2b$12$VMHDnKUECejuWQ/W9eXz1uqdTri2ftzRcQiA5RsZQu5z5yJgmKHqq', 'USUARIO', 'ACTIVO', '2025-11-24 13:30:16', NULL);

-- --------------------------------------------------------

--
-- Stand-in structure for view `v_disponibilidad`
-- (See below for the actual view)
--
CREATE TABLE `v_disponibilidad` (
`cantidad_reservada` decimal(32,0)
,`cantidad_total` int
,`fecha` date
,`franjas_ocupadas` text
,`recurso_id` int
,`recurso_nombre` varchar(150)
,`zona_id` int
);

-- --------------------------------------------------------

--
-- Table structure for table `zonas`
--

CREATE TABLE `zonas` (
  `id` int NOT NULL,
  `nombre` varchar(120) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `descripcion` text CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci,
  `imagen_url` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `creado_en` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `zonas`
--

INSERT INTO `zonas` (`id`, `nombre`, `descripcion`, `imagen_url`, `creado_en`) VALUES
(1, 'Chill Zone', 'Espacio de recreación y descanso', '/static/img/resources/Chill_Zone.jpg', '2025-11-04 02:42:05'),
(2, 'Coworking', 'Espacio de estudio y trabajo colaborativo', '/static/img/resources/CoWorkZone.jpg', '2025-11-04 02:42:05');

-- --------------------------------------------------------

--
-- Structure for view `v_disponibilidad`
--
DROP TABLE IF EXISTS `v_disponibilidad`;

CREATE ALGORITHM=UNDEFINED DEFINER=`root`@`localhost` SQL SECURITY DEFINER VIEW `v_disponibilidad`  AS SELECT `r`.`id` AS `recurso_id`, `r`.`nombre` AS `recurso_nombre`, `r`.`zona_id` AS `zona_id`, `d`.`fecha` AS `fecha`, `r`.`cantidad_total` AS `cantidad_total`, ifnull(sum((case when (`res`.`estado` in ('PENDIENTE','ACTIVA')) then `res`.`cantidad` else 0 end)),0) AS `cantidad_reservada`, group_concat(distinct concat(`res`.`hora_inicio`,'-',`res`.`hora_fin`) order by `res`.`hora_inicio` ASC separator ',') AS `franjas_ocupadas` FROM (((select curdate() AS `fecha` union all select (curdate() + interval 1 day) AS `DATE_ADD(CURDATE(), INTERVAL 1 DAY)` union all select (curdate() + interval 2 day) AS `DATE_ADD(CURDATE(), INTERVAL 2 DAY)`) `d` join `recursos` `r`) left join `reservas` `res` on(((`res`.`recurso_id` = `r`.`id`) and (`res`.`fecha` = `d`.`fecha`) and (`res`.`estado` in ('PENDIENTE','ACTIVA'))))) GROUP BY `r`.`id`, `d`.`fecha``fecha`  ;

--
-- Indexes for dumped tables
--

--
-- Indexes for table `config_sistema`
--
ALTER TABLE `config_sistema`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `nombre` (`nombre`);

--
-- Indexes for table `incidencias`
--
ALTER TABLE `incidencias`
  ADD PRIMARY KEY (`id`),
  ADD KEY `fk_incidencia_recurso` (`recurso_id`),
  ADD KEY `fk_incidencia_usuario` (`usuario_id`),
  ADD KEY `fk_incidencia_reserva` (`reserva_id`);

--
-- Indexes for table `incidencia_responsables`
--
ALTER TABLE `incidencia_responsables`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `unique_incidencia_usuario` (`incidencia_id`,`usuario_id`),
  ADD KEY `idx_incidencia_responsables_usuario` (`usuario_id`);

--
-- Indexes for table `recursos`
--
ALTER TABLE `recursos`
  ADD PRIMARY KEY (`id`),
  ADD KEY `idx_recursos_zona` (`zona_id`),
  ADD KEY `idx_recursos_estado` (`estado`),
  ADD KEY `idx_recursos_eliminado` (`eliminado`),
  ADD KEY `idx_recursos_zona_tipo` (`zona_id`,`tipo`),
  ADD KEY `idx_recursos_mant_periodo` (`mantenimiento_inicio`,`mantenimiento_fin`);

--
-- Indexes for table `reservas`
--
ALTER TABLE `reservas`
  ADD PRIMARY KEY (`id`),
  ADD KEY `idx_reservas_recurso_fecha` (`recurso_id`,`fecha`),
  ADD KEY `idx_reservas_usuario_fecha` (`usuario_id`,`fecha`),
  ADD KEY `idx_reservas_estado` (`estado`),
  ADD KEY `idx_reservas_fecha_hora` (`fecha`,`hora_inicio`,`hora_fin`);

--
-- Indexes for table `reserva_acompanantes`
--
ALTER TABLE `reserva_acompanantes`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `unique_reserva_usuario` (`reserva_id`,`usuario_id`),
  ADD KEY `idx_reserva_acompanantes_usuario` (`usuario_id`);

--
-- Indexes for table `sanciones`
--
ALTER TABLE `sanciones`
  ADD PRIMARY KEY (`id`),
  ADD KEY `fk_sancion_admin` (`creado_por`),
  ADD KEY `idx_sanciones_usuario` (`usuario_id`),
  ADD KEY `idx_sanciones_estado` (`estado`),
  ADD KEY `fk_sancion_incidencia` (`incidencia_id`);

--
-- Indexes for table `uso`
--
ALTER TABLE `uso`
  ADD PRIMARY KEY (`id`),
  ADD KEY `fk_uso_reserva` (`reserva_id`),
  ADD KEY `idx_uso_inicio` (`hora_inicio`);

--
-- Indexes for table `usuarios`
--
ALTER TABLE `usuarios`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `correo` (`correo`);

--
-- Indexes for table `zonas`
--
ALTER TABLE `zonas`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `nombre` (`nombre`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `config_sistema`
--
ALTER TABLE `config_sistema`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;

--
-- AUTO_INCREMENT for table `incidencias`
--
ALTER TABLE `incidencias`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=8;

--
-- AUTO_INCREMENT for table `incidencia_responsables`
--
ALTER TABLE `incidencia_responsables`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=8;

--
-- AUTO_INCREMENT for table `recursos`
--
ALTER TABLE `recursos`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=9;

--
-- AUTO_INCREMENT for table `reservas`
--
ALTER TABLE `reservas`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=24;

--
-- AUTO_INCREMENT for table `reserva_acompanantes`
--
ALTER TABLE `reserva_acompanantes`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=13;

--
-- AUTO_INCREMENT for table `sanciones`
--
ALTER TABLE `sanciones`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;

--
-- AUTO_INCREMENT for table `uso`
--
ALTER TABLE `uso`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT for table `usuarios`
--
ALTER TABLE `usuarios`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;

--
-- AUTO_INCREMENT for table `zonas`
--
ALTER TABLE `zonas`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `incidencias`
--
ALTER TABLE `incidencias`
  ADD CONSTRAINT `fk_incidencia_recurso` FOREIGN KEY (`recurso_id`) REFERENCES `recursos` (`id`),
  ADD CONSTRAINT `fk_incidencia_reserva` FOREIGN KEY (`reserva_id`) REFERENCES `reservas` (`id`),
  ADD CONSTRAINT `fk_incidencia_usuario` FOREIGN KEY (`usuario_id`) REFERENCES `usuarios` (`id`);

--
-- Constraints for table `incidencia_responsables`
--
ALTER TABLE `incidencia_responsables`
  ADD CONSTRAINT `fk_responsable_incidencia` FOREIGN KEY (`incidencia_id`) REFERENCES `incidencias` (`id`) ON DELETE CASCADE,
  ADD CONSTRAINT `fk_responsable_usuario` FOREIGN KEY (`usuario_id`) REFERENCES `usuarios` (`id`) ON DELETE CASCADE;

--
-- Constraints for table `recursos`
--
ALTER TABLE `recursos`
  ADD CONSTRAINT `fk_recurso_zona` FOREIGN KEY (`zona_id`) REFERENCES `zonas` (`id`) ON DELETE RESTRICT;

--
-- Constraints for table `reservas`
--
ALTER TABLE `reservas`
  ADD CONSTRAINT `fk_reserva_recurso` FOREIGN KEY (`recurso_id`) REFERENCES `recursos` (`id`),
  ADD CONSTRAINT `fk_reserva_usuario` FOREIGN KEY (`usuario_id`) REFERENCES `usuarios` (`id`);

--
-- Constraints for table `reserva_acompanantes`
--
ALTER TABLE `reserva_acompanantes`
  ADD CONSTRAINT `fk_acompanante_reserva` FOREIGN KEY (`reserva_id`) REFERENCES `reservas` (`id`) ON DELETE CASCADE,
  ADD CONSTRAINT `fk_acompanante_usuario` FOREIGN KEY (`usuario_id`) REFERENCES `usuarios` (`id`) ON DELETE CASCADE;

--
-- Constraints for table `sanciones`
--
ALTER TABLE `sanciones`
  ADD CONSTRAINT `fk_sancion_admin` FOREIGN KEY (`creado_por`) REFERENCES `usuarios` (`id`),
  ADD CONSTRAINT `fk_sancion_incidencia` FOREIGN KEY (`incidencia_id`) REFERENCES `incidencias` (`id`) ON DELETE SET NULL,
  ADD CONSTRAINT `fk_sancion_usuario` FOREIGN KEY (`usuario_id`) REFERENCES `usuarios` (`id`);

--
-- Constraints for table `uso`
--
ALTER TABLE `uso`
  ADD CONSTRAINT `fk_uso_reserva` FOREIGN KEY (`reserva_id`) REFERENCES `reservas` (`id`) ON DELETE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
