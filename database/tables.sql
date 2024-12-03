
DROP DATABASE IF EXISTS `__plickers`;
CREATE DATABASE `__plickers`;
USE `__plickers`;

/* ===== ===== ===== ===== ===== */

-- классы
CREATE TABLE `classes`
(
    `identifier` VARCHAR(24) PRIMARY KEY CHECK ( LENGTH(`identifier`) = 24 ),

    `created_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP(),
    `changed_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP(),

    `name`         TEXT NOT NULL,
    `teacher_name` TEXT NOT NULL
);

-- студенты в классах
CREATE TABLE `students_in_classes`
(
    `identifier` VARCHAR(24) PRIMARY KEY CHECK ( LENGTH(`identifier`) = 24 ),

    `created_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP(),
    `changed_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP(),

    `first_name`       TEXT        NOT NULL,
    `class_identifier` VARCHAR(24) NOT NULL REFERENCES `classes` (`identifier`)
);

-- история подключений студентов
CREATE TABLE `student_connection_history`
(
    `identifier` INTEGER PRIMARY KEY AUTO_INCREMENT,

    `connected_at`    TIMESTAMP NOT NULL,
    `disconnected_at` TIMESTAMP NOT NULL,

    `ip_address`         TEXT        NOT NULL,
    `student_identifier` VARCHAR(24)     NULL REFERENCES `students_in_classes` (`identifier`),
    `extension_version`  TEXT            NULL
);

/* ===== ===== ===== ===== ===== */

-- банк вопросов
CREATE TABLE `questions`
(
    `identifier` INTEGER PRIMARY KEY,

    `created_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP(),
    `changed_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP(),

    `formulation_html` TEXT NOT NULL
);

-- варианты ответов на вопрос
CREATE TABLE `question_options`
(
    `identifier` INTEGER PRIMARY KEY AUTO_INCREMENT,

    `created_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP(),
    `changed_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP(),

    `question_identifier` INTEGER NOT NULL REFERENCES `questions` (`identifier`),
    `option_identifier`   INTEGER NOT NULL,
    `formulation_html`    TEXT    NOT NULL
);

-- ответы студентов
CREATE TABLE `student_answers`
(
    `identifier` INTEGER PRIMARY KEY AUTO_INCREMENT,

    `created_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP(),
    `changed_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP(),

    `student_identifier`  VARCHAR(24) NOT NULL REFERENCES `students_in_classes` (`identifier`),
    `question_identifier` INTEGER     NOT NULL REFERENCES `questions` (`identifier`),
    `option_identifier`   INTEGER         NULL
);

/* ===== ===== ===== ===== ===== */
