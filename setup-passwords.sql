-- CS 121 24wi: Password Management (A6 and Final Project)
DROP FUNCTION IF EXISTS make_salt;
DROP FUNCTION IF EXISTS authenticate;
DROP PROCEDURE IF EXISTS sp_add_user;
DROP PROCEDURE IF EXISTS sp_change_password;

-- (Provided) This function generates a specified number of characters for using as a
-- salt in passwords.
DELIMITER !
CREATE FUNCTION make_salt(num_chars INT)
RETURNS VARCHAR(20) DETERMINISTIC
BEGIN
    DECLARE salt VARCHAR(20) DEFAULT '';

    -- Don't want to generate more than 20 characters of salt.
    SET num_chars = LEAST(20, num_chars);

    -- Generate the salt!  Characters used are ASCII code 32 (space)
    -- through 126 ('z').
    WHILE num_chars > 0 DO
        SET salt = CONCAT(salt, CHAR(32 + FLOOR(RAND() * 95)));
        SET num_chars = num_chars - 1;
    END WHILE;

    RETURN salt;
END !
DELIMITER ;


-- Our user_info table is create in setup.sql, so we don't need to create it here.

-- [Problem 1a]
-- Adds a new user to the user_info table, using the specified password (max
-- of 20 characters). Salts the password with a newly-generated salt value,
-- and then the salt and hash values are both stored in the table.
-- For our applicaiton, the username will be an email address.
-- We also need a first name and optional last name.
DELIMITER !
CREATE PROCEDURE sp_add_user(
    in_email VARCHAR(320),
    in_password VARCHAR(20),
    in_first_name VARCHAR(30),
    in_last_name VARCHAR(30),
    in_is_admin BOOLEAN)
BEGIN
    DECLARE salt VARCHAR(20);
    DECLARE hash BINARY(64);
    DECLARE new_user_id INT;

    -- Generate salt using the make_salt function
    SET salt = make_salt(8);

    -- Hash the password
    SET hash = SHA2(CONCAT(salt, in_password), 256);

    -- Insert user into the table
    INSERT INTO
        user_info (first_name, last_name, email, salt, password_hash, is_admin)
        VALUES (in_first_name, in_last_name, in_email, salt, hash, in_is_admin);

    SELECT LAST_INSERT_ID() INTO new_user_id;

    -- Create default shelves for the user
    INSERT INTO shelf (user_id, shelf_name, is_private)
        VALUES (new_user_id, 'Favorites', 1);
    INSERT INTO shelf (user_id, shelf_name, is_private)
        VALUES (new_user_id, 'Has Read', 1);
    INSERT INTO shelf (user_id, shelf_name, is_private)
        VALUES (new_user_id, 'Currently Reading', 1);
    INSERT INTO shelf (user_id, shelf_name, is_private)
        VALUES (new_user_id, 'Wants to Read', 1);
END !
DELIMITER ;

-- [Problem 1b]
-- Authenticates the specified username and password against the data
-- in the user_info table.  Returns 1 if the user appears in the table, and the
-- specified password hashes to the value for the user. Otherwise returns 0.
DELIMITER !
CREATE FUNCTION authenticate(email VARCHAR(320), password VARCHAR(20))
RETURNS TINYINT DETERMINISTIC
BEGIN
    DECLARE pwd_salt CHAR(8);
    DECLARE stored_hash BINARY(64);
    DECLARE result TINYINT DEFAULT 0;

    SELECT salt, password_hash INTO pwd_salt, stored_hash
        FROM user_info
        WHERE user_info.email = email;

    IF stored_hash IS NOT NULL THEN
        IF SHA2(CONCAT(pwd_salt, password), 256) = stored_hash THEN
            SET result = 1;
        END IF;
    END IF;

    RETURN result;
END !
DELIMITER ;

-- [Problem 1c]
-- Add at least two users into your user_info table so that when we run this file,
-- we will have examples users in the database.
-- These users are very simple; we'll have more complex users in the project.
CALL sp_add_user('maddie@caltech.edu', 'password1', 'Maddie', 'Ramos', 1);
CALL sp_add_user('arolfnes@caltech.edu', 'password2', 'Alex', 'Rolfness', 0);

-- [Problem 1d]
-- Create a procedure sp_change_password to generate a new salt and change the given
-- user's password to the given password (after salting and hashing)
DELIMITER !
CREATE PROCEDURE sp_change_password(email VARCHAR(320), new_password VARCHAR(20))
BEGIN
    DECLARE salt CHAR(8);
    DECLARE hash BINARY(64);
    SET salt = make_salt(8);
    SET hash = SHA2(CONCAT(salt, new_password), 256);

    UPDATE user_info
    SET salt = salt, password_hash = hash
    WHERE user_info.email = email;
END !
DELIMITER ;
