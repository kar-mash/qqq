-- phpMyAdmin SQL Dump
-- version 5.2.2
-- https://www.phpmyadmin.net/
--
-- Хост: MySQL-8.0
-- Время создания: Апр 25 2025 г., 05:33
-- Версия сервера: 8.0.41
-- Версия PHP: 8.0.30

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- База данных: `ex1`
--

-- --------------------------------------------------------

--
-- Структура таблицы `all_docs`
--

CREATE TABLE `all_docs` (
  `id` int NOT NULL,
  `name` text NOT NULL,
  `price` double NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Дамп данных таблицы `all_docs`
--

INSERT INTO `all_docs` (`id`, `name`, `price`) VALUES
(1, 'weqw', 2312343),
(2, 'ffff', 32434),
(3, 'eewqe', 222);

-- --------------------------------------------------------

--
-- Структура таблицы `status`
--

CREATE TABLE `status` (
  `id` int NOT NULL,
  `name` enum('paid','not_paid') CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Дамп данных таблицы `status`
--

INSERT INTO `status` (`id`, `name`) VALUES
(1, 'paid'),
(2, 'not_paid');

-- --------------------------------------------------------

--
-- Структура таблицы `users`
--

CREATE TABLE `users` (
  `id` int NOT NULL,
  `login` text NOT NULL,
  `password` text NOT NULL,
  `name` text NOT NULL,
  `surname` text NOT NULL,
  `role` varchar(50) NOT NULL DEFAULT 'client'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Дамп данных таблицы `users`
--

INSERT INTO `users` (`id`, `login`, `password`, `name`, `surname`, `role`) VALUES
(1, 'kkk', '000', 'kal', 'ff', 'client'),
(2, 'user', '123', 'kalkal', 'kal', 'client'),
(3, '44e', 'ewqe', 'www', 'w', 'client'),
(4, 'jjj', '123', 'Lo', 'La', 'client'),
(5, '22', '222', 'weq', '212', 'admin');

-- --------------------------------------------------------

--
-- Структура таблицы `user_docs`
--

CREATE TABLE `user_docs` (
  `id` int NOT NULL,
  `id_user` int NOT NULL,
  `id_docs` int NOT NULL,
  `date_start` date NOT NULL,
  `date_end` date NOT NULL,
  `id_status` int NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Дамп данных таблицы `user_docs`
--

INSERT INTO `user_docs` (`id`, `id_user`, `id_docs`, `date_start`, `date_end`, `id_status`) VALUES
(3, 1, 1, '2024-04-01', '2025-01-01', 1),
(4, 1, 2, '2023-08-12', '2024-09-15', 2),
(5, 4, 3, '2022-01-01', '2023-01-06', 2);

--
-- Индексы сохранённых таблиц
--

--
-- Индексы таблицы `all_docs`
--
ALTER TABLE `all_docs`
  ADD PRIMARY KEY (`id`);

--
-- Индексы таблицы `status`
--
ALTER TABLE `status`
  ADD PRIMARY KEY (`id`);

--
-- Индексы таблицы `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`id`);

--
-- Индексы таблицы `user_docs`
--
ALTER TABLE `user_docs`
  ADD PRIMARY KEY (`id`),
  ADD KEY `id_user` (`id_user`),
  ADD KEY `id_docs` (`id_docs`),
  ADD KEY `id_status` (`id_status`);

--
-- AUTO_INCREMENT для сохранённых таблиц
--

--
-- AUTO_INCREMENT для таблицы `all_docs`
--
ALTER TABLE `all_docs`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT для таблицы `status`
--
ALTER TABLE `status`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT для таблицы `users`
--
ALTER TABLE `users`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT для таблицы `user_docs`
--
ALTER TABLE `user_docs`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- Ограничения внешнего ключа сохраненных таблиц
--

--
-- Ограничения внешнего ключа таблицы `user_docs`
--
ALTER TABLE `user_docs`
  ADD CONSTRAINT `user_docs_ibfk_1` FOREIGN KEY (`id_user`) REFERENCES `users` (`id`),
  ADD CONSTRAINT `user_docs_ibfk_2` FOREIGN KEY (`id_docs`) REFERENCES `all_docs` (`id`),
  ADD CONSTRAINT `user_docs_ibfk_3` FOREIGN KEY (`id_status`) REFERENCES `status` (`id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
