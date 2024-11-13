
DROP DATABASE IF EXISTS `__plickers`;
CREATE DATABASE `__plickers`;
USE `__plickers`;

-- пользователи
CREATE TABLE `users`
(
    `identifier` INTEGER NOT NULL PRIMARY KEY,

    `created_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP(),
    `changed_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP(),

    `name` TEXT NOT NULL
);

-- история подключений
CREATE TABLE `connection_history`
(
    `identifier` INTEGER NOT NULL PRIMARY KEY AUTO_INCREMENT,

    `connected_at`    TIMESTAMP NOT NULL,
    `disconnected_at` TIMESTAMP NOT NULL,

    `ip_address`      TEXT    NOT NULL,
    `user_identifier` INTEGER     NULL REFERENCES `users` (`identifier`)
);

-- вопросы
CREATE TABLE `questions`
(
    `identifier` INTEGER NOT NULL PRIMARY KEY,

    `created_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP(),
    `changed_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP(),

    `formulation_html` TEXT NOT NULL
);

-- варианты ответов
CREATE TABLE `options`
(
    `identifier` INTEGER NOT NULL PRIMARY KEY AUTO_INCREMENT,

    `created_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP(),
    `changed_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP(),

    `question_identifier` INTEGER NOT NULL REFERENCES `questions` (`identifier`),
    `option_identifier`   INTEGER NOT NULL,
    `formulation_html`    TEXT    NOT NULL
);

-- ответы пользователей
CREATE TABLE `answers`
(
    `identifier` INTEGER NOT NULL PRIMARY KEY AUTO_INCREMENT,

    `created_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP(),
    `changed_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP(),

    `user_identifier`     INTEGER NOT NULL REFERENCES `users`     (`identifier`),
    `question_identifier` INTEGER NOT NULL REFERENCES `questions` (`identifier`),
    `option_identifier`   INTEGER NOT NULL REFERENCES `options`   (`option_identifier`)
);
