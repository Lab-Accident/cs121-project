-- CS 121 24wi: Password Management (A6 and Final Project)

-- (Provided) This function generates a specified number of characters for using as a
-- salt in passwords.
DELIMITER !
CREATE FUNCTION make_salt(num_chars INT)
RETURNS VARCHAR(20) NOT DETERMINISTIC
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

-- Provided (you may modify in your FP if you choose)
-- This table holds information for authenticating users based on
-- a password.  Passwords are not stored plaintext so that they
-- cannot be used by people that shouldn't have them.
-- You may extend that table to include an is_admin or role attribute if you
-- have admin or other roles for users in your application
-- (e.g. store managers, data managers, etc.)
CREATE TABLE user_info (
    -- Usernames are up to 20 characters.
    username VARCHAR(20) PRIMARY KEY,
    -- Salt will be 8 characters all the time, so we can make this 8.
    salt CHAR(8) NOT NULL,
    -- We use SHA-2 with 256-bit hashes.  MySQL returns the hash
    -- value as a hexadecimal string, which means that each byte is
    -- represented as 2 characters.  Thus, 256 / 8 * 2 = 64.
    -- We can use BINARY or CHAR here; BINARY simply has a different
    -- definition for comparison/sorting than CHAR.
    password_hash BINARY(64) NOT NULL
);

-- [Problem 1a]
-- Adds a new user to the user_info table, using the specified password (max
-- of 20 characters). Salts the password with a newly-generated salt value,
-- and then the salt and hash values are both stored in the table.
DELIMITER !
CREATE PROCEDURE sp_add_user(new_username VARCHAR(20), password VARCHAR(20))
BEGIN
    DECLARE salt CHAR(8);
    DECLARE hash BINARY(64);
    SET salt = make_salt(8);
    SET hash = SHA2(CONCAT(salt, password), 256);

    INSERT INTO user_info (username, salt, password_hash)
        VALUES (new_username, salt, hash);
END !
DELIMITER ;

-- [Problem 1b]
-- Authenticates the specified username and password against the data
-- in the user_info table.  Returns 1 if the user appears in the table, and the
-- specified password hashes to the value for the user. Otherwise returns 0.
DELIMITER !
CREATE FUNCTION authenticate(username VARCHAR(20), password VARCHAR(20))
RETURNS TINYINT DETERMINISTIC
BEGIN
    DECLARE salt CHAR(8);
    DECLARE stored_hash BINARY(64);
    DECLARE result TINYINT;

    SELECT salt, password_hash INTO salt, stored_hash
        FROM user_info
        WHERE username = username;

    IF stored_hash IS NOT NULL THEN
        IF SHA2(CONCAT(salt, password), 256) = stored_hash THEN
            SET result = 1;
        ELSE
            SET result = 0;
        END IF;
    ELSE
        SET result = 0;
    END IF;

    RETURN result;
END !
DELIMITER ;

-- [Problem 1c]
-- Add at least two users into your user_info table so that when we run this file,
-- we will have examples users in the database.
sp_add_user('user1', 'password1');
sp_add_user('user2', 'password2');

-- [Problem 1d]
-- Create a procedure sp_change_password to generate a new salt and change the given
-- user's password to the given password (after salting and hashing)
DELIMITER !
CREATE PROCEDURE sp_change_password(username VARCHAR(20), old_password VARCHAR(20), new_password VARCHAR(20))
BEGIN
    -- Set new password if the old password is correct
    IF authenticate(username, old_password) = 1 THEN
        DECLARE salt CHAR(8);
        DECLARE hash BINARY(64);
        SET salt = make_salt(8);
        SET hash = SHA2(CONCAT(salt, new_password), 256);

        UPDATE user_info
            SET salt = salt, password_hash = hash
            WHERE username = username;
    END IF;
END !
