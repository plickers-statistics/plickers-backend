
CREATE OR REPLACE PROCEDURE REPLACE_IF_EXISTS_ELSE_ADD_CLASS_ROOM
(
    IN parameter_hash_code    CHAR(24),
    IN parameter_name         TEXT,
    IN parameter_teacher_name TEXT
)
BEGIN
    DECLARE CONTINUE HANDLER FOR SQLEXCEPTION
        ROLLBACK;

    START TRANSACTION;

    INSERT INTO `classes` (`hash_code`, `name`, `teacher_name`)
    VALUES (parameter_hash_code, parameter_name, parameter_teacher_name)
    ON DUPLICATE KEY UPDATE
        `name`         = parameter_name,
        `teacher_name` = parameter_teacher_name,
        `changed_at`   = IF(
            parameter_name = VALUES(`name`) AND parameter_teacher_name = VALUES(`teacher_name`),
            VALUES(`changed_at`),
            CURRENT_TIMESTAMP()
        );

    COMMIT;
END;

CREATE OR REPLACE PROCEDURE REPLACE_IF_EXISTS_ELSE_ADD_STUDENT
(
    IN parameter_hash_code            CHAR(24),
    IN parameter_first_name           TEXT,
    IN parameter_class_hash_code CHAR(24)
)
BEGIN
    DECLARE CONTINUE HANDLER FOR SQLEXCEPTION
        ROLLBACK;

    START TRANSACTION;

    INSERT INTO `students_in_classes` (`hash_code`, `first_name`, `class_hash_code`)
    VALUES (parameter_hash_code, parameter_first_name, parameter_class_hash_code)
    ON DUPLICATE KEY UPDATE
        `first_name` = parameter_first_name,
        `changed_at` = IF(
            parameter_first_name = VALUES(`first_name`),
            VALUES(`changed_at`),
            CURRENT_TIMESTAMP()
        );

    COMMIT;
END;
