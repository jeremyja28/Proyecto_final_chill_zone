-- phpMyAdmin SQL Dump
-- version 5.2.0
-- https://www.phpmyadmin.net/
--
-- Host: localhost:3307
-- Generation Time: Jan 24, 2026 at 06:51 PM
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
--

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
  `observacion` text COLLATE utf8mb4_unicode_ci,
  `creado_en` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `reservas`
--

INSERT INTO `reservas` (`id`, `usuario_id`, `recurso_id`, `fecha`, `hora_inicio`, `hora_fin`, `cantidad`, `estado`, `observacion`, `creado_en`) VALUES
(1, 2, 3, '2025-11-03', '10:00:00', '11:00:00', 1, 'FINALIZADA', NULL, '2025-11-04 02:42:05'),
(2, 2, 1, '2025-11-03', '09:00:00', '09:30:00', 1, 'FINALIZADA', NULL, '2025-11-04 02:42:05'),
(3, 2, 3, '2025-11-18', '14:00:00', '21:00:00', 1, 'CANCELADA', NULL, '2025-11-15 17:17:59'),
(4, 2, 1, '2025-11-15', '08:30:00', '09:00:00', 1, 'FINALIZADA', NULL, '2025-11-15 17:35:20'),
(5, 2, 1, '2025-11-17', '07:00:00', '07:15:00', 1, 'FINALIZADA', NULL, '2025-11-17 12:27:02'),
(6, 2, 3, '2025-11-17', '07:00:00', '07:45:00', 1, 'FINALIZADA', NULL, '2025-11-17 12:52:26'),
(7, 2, 2, '2025-11-17', '10:00:00', '11:15:00', 1, 'CANCELADA', NULL, '2025-11-17 12:54:52'),
(8, 2, 3, '2025-11-17', '10:00:00', '11:15:00', 1, 'FINALIZADA', NULL, '2025-11-17 12:55:25'),
(9, 1, 4, '2025-11-22', '19:00:00', '20:15:00', 1, 'CANCELADA', NULL, '2025-11-22 18:10:08'),
(10, 1, 4, '2025-11-22', '13:30:00', '13:45:00', 1, 'FINALIZADA', NULL, '2025-11-22 18:12:51'),
(11, 2, 4, '2025-11-22', '13:45:00', '14:00:00', 1, 'FINALIZADA', NULL, '2025-11-22 18:18:45'),
(12, 1, 8, '2025-11-24', '07:00:00', '07:30:00', 1, 'CANCELADA', NULL, '2025-11-23 22:21:44'),
(13, 2, 1, '2025-11-24', '08:00:00', '08:30:00', 1, 'FINALIZADA', NULL, '2025-11-23 22:27:21'),
(14, 2, 1, '2025-11-24', '08:30:00', '10:15:00', 1, 'CANCELADA', NULL, '2025-11-24 13:03:34'),
(15, 1, 1, '2025-12-08', '13:15:00', '14:30:00', 1, 'CANCELADA', NULL, '2025-12-07 17:10:56'),
(16, 2, 1, '2025-12-10', '10:00:00', '11:00:00', 1, 'CANCELADA', NULL, '2025-12-10 14:42:01'),
(17, 2, 1, '2025-12-10', '10:00:00', '11:00:00', 1, 'CANCELADA', NULL, '2025-12-10 14:44:18'),
(18, 2, 1, '2025-12-10', '11:00:00', '12:00:00', 1, 'CANCELADA_MANTENIMIENTO', NULL, '2025-12-10 15:32:30'),
(19, 2, 1, '2025-12-10', '13:00:00', '14:00:00', 1, 'FINALIZADA', NULL, '2025-12-10 15:36:17'),
(20, 2, 7, '2025-12-10', '14:00:00', '15:00:00', 1, 'FINALIZADA', NULL, '2025-12-10 15:37:10'),
(21, 3, 6, '2025-12-10', '12:30:00', '13:45:00', 1, 'FINALIZADA', NULL, '2025-12-10 15:39:04'),
(22, 3, 7, '2025-12-10', '15:00:00', '16:15:00', 1, 'FINALIZADA', NULL, '2025-12-10 15:39:24'),
(23, 4, 4, '2025-12-10', '21:15:00', '21:45:00', 1, 'CANCELADA', NULL, '2025-12-11 00:08:10'),
(24, 2, 9, '2026-01-24', '19:15:00', '21:00:00', 1, 'CANCELADA', NULL, '2026-01-24 18:04:43'),
(25, 2, 9, '2026-01-24', '15:30:00', '16:30:00', 1, 'CANCELADA', ' [Auto-Cancelación: Recurso marcado como \'Fuera de Servicio\' por avería técnica]', '2026-01-24 18:17:24'),
(26, 2, 10, '2026-01-24', '19:30:00', '20:30:00', 1, 'CANCELADA', ' [Auto-Cancelación: Reserva cancelada: La Zona \'Canchas\' ha sido inhabilitada temporalmente.]', '2026-01-24 18:31:26'),
(27, 2, 7, '2026-01-24', '19:30:00', '20:30:00', 1, 'CANCELADA_MANTENIMIENTO', NULL, '2026-01-24 18:39:27'),
(28, 2, 4, '2026-01-24', '20:15:00', '21:00:00', 1, 'CANCELADA', 'El recurso \'Mesa Juegos de Mesa\' fue desactivado.', '2026-01-24 18:41:37'),
(29, 2, 10, '2026-01-24', '18:45:00', '19:15:00', 1, 'PENDIENTE', NULL, '2026-01-24 18:44:02'),
(30, 2, 9, '2026-01-24', '19:45:00', '21:00:00', 1, 'PENDIENTE', NULL, '2026-01-24 18:45:29');

--
-- Indexes for dumped tables
--

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
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `reservas`
--
ALTER TABLE `reservas`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=31;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `reservas`
--
ALTER TABLE `reservas`
  ADD CONSTRAINT `fk_reserva_recurso` FOREIGN KEY (`recurso_id`) REFERENCES `recursos` (`id`),
  ADD CONSTRAINT `fk_reserva_usuario` FOREIGN KEY (`usuario_id`) REFERENCES `usuarios` (`id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
