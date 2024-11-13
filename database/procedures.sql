
CREATE OR REPLACE PROCEDURE REPLACE_IF_EXISTS_ELSE_ADD_USER (user_identifier INTEGER, user_name TEXT)
BEGIN
    SET @user_name := (SELECT `name` FROM `users` WHERE `identifier` = user_identifier LIMIT 1);

    IF (@user_name IS NULL)
    THEN
        INSERT INTO `users` (`identifier`, `name`) VALUES (user_identifier, user_name);
    ELSE
        IF (@user_name != user_name)
        THEN
            UPDATE `users` SET `name` = user_name, `changed_at` = CURRENT_TIMESTAMP() WHERE `identifier` = user_identifier;
        END IF;
    END IF;
END;
