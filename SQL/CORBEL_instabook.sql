DROP DATABASE IF EXISTS `instabook`;
CREATE DATABASE IF NOT EXISTS `instabook`;
USE `instabook`;

DROP TABLE IF EXISTS `users`;
CREATE TABLE IF NOT EXISTS `users` (
  `id` int NOT NULL AUTO_INCREMENT,
  `username` varchar(30) UNIQUE NOT NULL,
  `email` varchar(256) UNIQUE NOT NULL,
  `email_verified_at` DATETIME DEFAULT NULL,
  `password` varchar(255),
  `remember_token` varchar(255) DEFAULT NULL,
  `created_at` DATETIME DEFAULT current_timestamp,
  `updated_at` DATETIME DEFAULT NULL,
  PRIMARY KEY (`id`)
);

DROP TABLE IF EXISTS `groups`;
CREATE TABLE IF NOT EXISTS `groups` (
	`id` int NOT NULL AUTO_INCREMENT,
    `name` varchar(256) NOT NULL,
    `description` text,
    `created_at` datetime DEFAULT current_timestamp,
    `updated_at` datetime DEFAULT NULL,
    PRIMARY KEY (`id`)
);

DROP TABLE IF EXISTS `group_user`;
CREATE TABLE IF NOT EXISTS `group_user` (
	`id_group` int NOT NULL,
    `id_user` int NOT NULL,
    FOREIGN KEY (`id_group`) REFERENCES `groups`(`id`),
    FOREIGN KEY (`id_user`) REFERENCES `users`(`id`),
    PRIMARY KEY (`id_group`,`id_user`)
);

DROP TABLE IF EXISTS `photos`;
CREATE TABLE IF NOT EXISTS `photos` (
	`id` int NOT NULL AUTO_INCREMENT,
    `title` varchar(255) NOT NULL,
    `description` text,
    `file_path` varchar(255) UNIQUE NOT NULL,
    `photo_date` datetime, 
    `resolution` varchar(30),
    `width` int unsigned,
    `height` int unsigned, 
    `created_at` datetime DEFAULT current_timestamp,
    `updated_at` datetime DEFAULT NULL,
    `owner_id` int,
    `group_id` int NOT NULL,
    PRIMARY KEY (`id`),
    FOREIGN KEY (`owner_id`) REFERENCES `users`(`id`),
    FOREIGN KEY (`group_id`) REFERENCES `groups`(`id`) ON DELETE CASCADE
);

DROP TABLE IF EXISTS `tags`;
CREATE TABLE IF NOT EXISTS `tags`(
	`id` int NOT NULL AUTO_INCREMENT,
    `name` varchar(30) NOT NULL UNIQUE,
    `created_at` datetime DEFAULT current_timestamp,
    `updated_at` datetime DEFAULT NULL,
    PRIMARY KEY (`id`)
);

DROP TABLE IF EXISTS `photo_tag`;
CREATE TABLE IF NOT EXISTS `photo_tag`(
	`id_photo` int NOT NULL,
    `id_tag` int,
    FOREIGN KEY (`id_photo`) REFERENCES `photos`(`id`) ON DELETE CASCADE,
    FOREIGN KEY (`id_tag`) REFERENCES `tags`(`id`) ON DELETE CASCADE,
    PRIMARY KEY (`id_photo`, `id_tag`)
);

DROP TABLE IF EXISTS `comments`;
CREATE TABLE IF NOT EXISTS `comments` (
	`id` int NOT NULL AUTO_INCREMENT, 
    `content` TEXT NOT NULL,
	`created_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
	`edited_at` datetime DEFAULT NULL,
    `deletion_date` datetime DEFAULT NULL,
    `id_photo` int NOT NULL,
    `id_answered_comment` int DEFAULT NULL,
    `id_user` int,
    PRIMARY KEY (`id`),
    FOREIGN KEY (`id_photo`)REFERENCES `photos` (`id`) ON DELETE CASCADE,
    FOREIGN KEY (`id_user`) REFERENCES  `users` (`id`),
    FOREIGN KEY (`id_answered_comment`) REFERENCES `comments` (`id`) ON DELETE CASCADE
);

# ----------------------------------------------- #

# Contrainte de date courante
ALTER TABLE `photos` 
MODIFY `created_at` DATETIME DEFAULT current_timestamp NOT NULL;

# Contrainte de date de modification sur la table `photos`
ALTER TABLE `photos`
ADD CONSTRAINT CHK_PhotoUpdate CHECK (`updated_at` = NULL OR `updated_at` > `created_at`);

# Contrainte de type (entier positif)
ALTER TABLE `photos`
MODIFY `width` int unsigned NOT NULL;
# Contrainte de hauteur minimale
ALTER TABLE `photos`
ADD CONSTRAINT CHK_PhotoHeight CHECK (`height` >= 10);

# Contrainte d'historique des modifications
ALTER TABLE `comments`
DROP COLUMN `edited_at`;

DROP TABLE IF EXISTS `comment_edit`;
CREATE TABLE IF NOT EXISTS `comment_edit` (
	`id` int NOT NULL AUTO_INCREMENT,
    `user_id` int,
    `comment_id` int NOT NULL,
    `updated_at` DATETIME NOT NULL DEFAULT current_timestamp,
    PRIMARY KEY (`id`),
    FOREIGN KEY (`user_id`) REFERENCES `users`(`id`),
    FOREIGN KEY (`comment_id`) REFERENCES `comments`(`id`)
);

# Contrainte d'unicité de l'adresse mail
ALTER TABLE `users`
ADD CONSTRAINT UNIQUE (`email`);
