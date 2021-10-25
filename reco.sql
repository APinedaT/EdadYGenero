-- phpMyAdmin SQL Dump
-- version 5.0.4
-- https://www.phpmyadmin.net/
--
-- Servidor: 127.0.0.1
-- Tiempo de generación: 26-05-2021 a las 19:13:05
-- Versión del servidor: 10.4.17-MariaDB
-- Versión de PHP: 7.3.27

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de datos: `electronika`
--

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `reco`
--

CREATE TABLE `reco` (
  `ID` int(50) NOT NULL,
  `Hora` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  `Tiempo` int(50) NOT NULL,
  `Genero` varchar(50) NOT NULL,
  `Edad` varchar(50) NOT NULL,
  `Expresion` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Volcado de datos para la tabla `reco`
--

INSERT INTO `reco` (`ID`, `Hora`, `Tiempo`, `Genero`, `Edad`, `Expresion`) VALUES
(1, '0000-00-00 00:00:00', 0, '', '0', ''),
(2, '2021-02-22 04:24:27', 0, '', '0', ''),
(34, '2021-02-23 01:16:25', 2, '', '0', ''),
(35, '2021-02-23 01:18:02', 2, '', '0', ''),
(36, '2021-02-23 01:18:31', 4, '', '0', ''),
(37, '2021-05-12 12:26:06', 10, 'Male', '0', ''),
(38, '2021-05-12 12:27:18', 7, 'Male', '(15-20)', ''),
(39, '2021-05-12 15:45:31', 47, 'Male', '(25-32)', ''),
(40, '2021-05-12 15:46:39', 6, 'Male', '(8-12)', ''),
(41, '2021-05-12 15:47:40', 19, 'Male', '(25-32)', ''),
(42, '2021-05-12 15:47:40', 19, 'Male', '(25-32)', ''),
(43, '2021-05-14 14:15:44', 7, 'Male', '(25-32)', ''),
(44, '2021-05-14 14:15:45', 7, 'Male', '(25-32)', ''),
(45, '2021-05-14 14:15:45', 7, 'Male', '(25-32)', ''),
(46, '2021-05-14 14:19:01', 57, 'Male', '(25-32)', ''),
(47, '2021-05-14 14:27:27', 50, 'Male', '(25-32)', ''),
(48, '2021-05-14 14:27:27', 50, 'Male', '(25-32)', ''),
(49, '2021-05-26 03:35:22', 31, 'Male', '(8-12)', ''),
(50, '2021-05-26 03:35:23', 31, 'Male', '(8-12)', ''),
(51, '2021-05-26 14:08:45', 16, 'Male', '(25-32)', ''),
(52, '2021-05-26 14:10:07', 9, 'Male', '(8-12)', ''),
(53, '2021-05-26 14:10:07', 8, 'Male', '(8-12)', ''),
(54, '2021-05-26 14:14:14', 3, 'Male', '(25-32)', ''),
(55, '2021-05-26 14:14:47', 19, 'Male', '(25-32)', ''),
(56, '2021-05-26 14:14:47', 8, 'Female', '(25-32)', '');

--
-- Índices para tablas volcadas
--

--
-- Indices de la tabla `reco`
--
ALTER TABLE `reco`
  ADD PRIMARY KEY (`ID`);

--
-- AUTO_INCREMENT de las tablas volcadas
--

--
-- AUTO_INCREMENT de la tabla `reco`
--
ALTER TABLE `reco`
  MODIFY `ID` int(50) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=57;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
