DROP DATABASE IF EXISTS todo_app;
CREATE DATABASE IF NOT EXISTS todo_app;
USE todo_app;

DROP TABLE IF EXISTS `priorities`;
CREATE TABLE IF NOT EXISTS `priorities` (
	`id` int NOT NULL AUTO_INCREMENT,
    `name` varchar(20) UNIQUE NOT NULL,
    PRIMARY KEY (`id`)
);

DROP TABLE IF EXISTS `categories`;
CREATE TABLE IF NOT EXISTS `categories` (
	`id` int NOT NULL AUTO_INCREMENT,
    `name` varchar(20) UNIQUE NOT NULL,
    PRIMARY KEY (`id`)
);

DROP TABLE IF EXISTS `task_states`;
CREATE TABLE IF NOT EXISTS `task_states` (
	`id` int NOT NULL AUTO_INCREMENT,
    `name` varchar(20) UNIQUE NOT NULL,
    PRIMARY KEY (`id`)
);

DROP TABLE IF EXISTS `users`;
CREATE TABLE IF NOT EXISTS `users` (
	`id` int NOT NULL AUTO_INCREMENT,
    `username` varchar(30) UNIQUE NOT NULL,
    `password` varchar(255),
    PRIMARY KEY (`id`)
);

DROP TABLE IF EXISTS `boards`;
CREATE TABLE IF NOT EXISTS `boards` (
	`id` int NOT NULL AUTO_INCREMENT,
    `title` varchar(255) NOT NULL,
    `description` text, 
    `user_id` int,
	`creation_date` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
	`edition_date` datetime DEFAULT NULL,
    `deletion_date` datetime DEFAULT NULL,
    PRIMARY KEY (`id`),
    FOREIGN KEY (`user_id`) REFERENCES `users`(`id`)
);

DROP TABLE IF EXISTS `board_participants`;
CREATE TABLE IF NOT EXISTS `board_participants` (
	`user_id` int NOT NULL,
    `board_id` int NOT NULL,
	PRIMARY KEY (`board_id`,`user_id`),
    FOREIGN KEY (`user_id`) REFERENCES `users` (`id`),
    FOREIGN KEY (`board_id`) REFERENCES `boards` (`id`)
);

DROP TABLE IF EXISTS `tasks`;
CREATE TABLE IF NOT EXISTS `tasks` (
	`id` int NOT NULL AUTO_INCREMENT,
    `title` varchar(255) NOT NULL,
    `description` varchar(255),
	`creation_date` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
	`edition_date` datetime DEFAULT NULL,
    `deletion_date` datetime DEFAULT NULL,
    `completion_date` datetime DEFAULT NULL,
    `id_board` int NOT NULL,
    `id_user` int,
    `id_priority` int,
    `id_task_state` int, 
    `id_category` int,
    PRIMARY KEY (`id`),
    FOREIGN KEY (`id_board`) REFERENCES `boards`(`id`) ON DELETE CASCADE,
    FOREIGN KEY (`id_user`) REFERENCES `users`(`id`),
    FOREIGN KEY (`id_priority`) REFERENCES `priorities`(`id`),
    FOREIGN KEY (`id_task_state`) REFERENCES `task_states`(`id`),
    FOREIGN KEY (`id_category`) REFERENCES `categories`(`id`)
);

DROP TABLE IF EXISTS `attached_files`;
CREATE TABLE IF NOT EXISTS `attached_files` (
	`id` int NOT NULL AUTO_INCREMENT, 
    `path` varchar(255) UNIQUE NOT NULL,
	`creation_date` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
    `task_id` int NOT NULL,
    `user_id` int,
    PRIMARY KEY (`id`),
    FOREIGN KEY (`task_id`) REFERENCES `tasks`(`id`) ON DELETE CASCADE,
    FOREIGN KEY (`user_id`) REFERENCES `users`(`id`)
);

DROP TABLE IF EXISTS `task_assigned_users`;
CREATE TABLE IF NOT EXISTS `task_assigned_users` (
	`task_id` int NOT NULL,
    `user_id` int NOT NULL,
    PRIMARY KEY (`task_id`, `user_id`),
    FOREIGN KEY (`task_id`) REFERENCES `tasks`(`id`) ON DELETE CASCADE,
    FOREIGN KEY (`user_id`) REFERENCES `users`(`id`) ON DELETE CASCADE
);

DROP TABLE IF EXISTS `comments`;
CREATE TABLE IF NOT EXISTS `comments` (
	`id` int NOT NULL AUTO_INCREMENT, 
    `content` TEXT NOT NULL,
	`creation_date` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
	`edition_date` datetime DEFAULT NULL,
    `deletion_date` datetime DEFAULT NULL,
    `id_task` int NOT NULL,
    `id_answered_comment` int DEFAULT NULL,
    `id_user` int,
    PRIMARY KEY (`id`),
    FOREIGN KEY (`id_task`) REFERENCES `tasks` (`id`) ON DELETE CASCADE,
    FOREIGN KEY (`id_user`) REFERENCES  `users` (`id`),
    FOREIGN KEY (`id_answered_comment`) REFERENCES `comments` (`id`) ON DELETE CASCADE
)
    