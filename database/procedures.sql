
CREATE OR REPLACE PROCEDURE REPLACE_IF_EXISTS_ELSE_ADD_CLASS_ROOM
(
    IN parameter_identifier   VARCHAR(24),
    IN parameter_name         TEXT,
    IN parameter_teacher_name TEXT
)
BEGIN
    DECLARE CONTINUE HANDLER FOR SQLEXCEPTION
        ROLLBACK;

    START TRANSACTION;

    INSERT INTO `classes` (`identifier`, `name`, `teacher_name`)
    VALUES (parameter_identifier, parameter_name, parameter_teacher_name)
    ON DUPLICATE KEY UPDATE
        `name`         = VALUES(`name`),
        `teacher_name` = VALUES(`teacher_name`),
        `changed_at`   = CURRENT_TIMESTAMP();

    COMMIT;
END;

CREATE OR REPLACE PROCEDURE REPLACE_IF_EXISTS_ELSE_ADD_STUDENT
(
    IN parameter_identifier       VARCHAR(24),
    IN parameter_first_name       TEXT,
    IN parameter_class_identifier VARCHAR(24)
)
BEGIN
    DECLARE CONTINUE HANDLER FOR SQLEXCEPTION
        ROLLBACK;

    START TRANSACTION;

    INSERT INTO `students_in_classes` (`identifier`, `first_name`, `class_identifier`)
    VALUES (parameter_identifier, parameter_first_name, parameter_class_identifier)
    ON DUPLICATE KEY UPDATE
        `first_name` = VALUES(`first_name`),
        `changed_at` = CURRENT_TIMESTAMP();

    COMMIT;
END;
