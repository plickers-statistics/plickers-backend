
CREATE OR REPLACE PROCEDURE REPLACE_IF_EXISTS_ELSE_ADD_CLASS_ROOM
(
    IN parameter_identifier   VARCHAR(24),
    IN parameter_name         TEXT,
    IN parameter_teacher_name TEXT
)
BEGIN
    SELECT (@name := `name`), (@teacher_name := `teacher_name`) FROM `classes` WHERE `identifier` = parameter_identifier LIMIT 1;

    IF (@name IS NULL)
    THEN
        INSERT INTO `classes`
            (`identifier`, `name`, `teacher_name`)
        VALUES
            (parameter_identifier, parameter_name, parameter_teacher_name);
    ELSE
        IF (@name != parameter_name OR @teacher_name != parameter_teacher_name)
        THEN
            UPDATE `classes` SET
                `changed_at`   = CURRENT_TIMESTAMP(),
                `name`         = parameter_name,
                `teacher_name` = parameter_teacher_name
            WHERE `identifier` = parameter_identifier;
        END IF;
    END IF;

    COMMIT;
END;

CREATE OR REPLACE PROCEDURE REPLACE_IF_EXISTS_ELSE_ADD_STUDENT
(
    IN parameter_identifier       VARCHAR(24),
    IN parameter_first_name       TEXT,
    IN parameter_class_identifier VARCHAR(24)
)
BEGIN
    SET @first_name := (SELECT `first_name` FROM `students` WHERE `identifier` = parameter_identifier LIMIT 1);

    IF (@first_name IS NULL)
    THEN
        INSERT INTO `students`
            (`identifier`, `first_name`, `class_identifier`)
        VALUES
            (parameter_identifier, parameter_first_name, parameter_class_identifier);
    ELSE
        IF (@first_name != parameter_first_name)
        THEN
            UPDATE `students` SET
                `changed_at` = CURRENT_TIMESTAMP(),
                `first_name` = parameter_first_name
            WHERE `identifier` = parameter_identifier;
        END IF;
    END IF;

    COMMIT;
END;
