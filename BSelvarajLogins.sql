
DROP DATABASE IF EXISTS BSelvarajLogins;
CREATE DATABASE BSelvarajLogins;
USE BSelvarajLogins;

-- =======================
-- Table: User
-- =======================
CREATE TABLE User (
    userId INT AUTO_INCREMENT PRIMARY KEY,
    firstName VARCHAR(50) NOT NULL,
    lastName VARCHAR(50) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    accessLevel ENUM('basic', 'admin') NOT NULL
);

-- =======================
-- Table: Login
-- =======================
CREATE TABLE Login (
    loginId INT AUTO_INCREMENT PRIMARY KEY,
    userId INT UNIQUE,
    username VARCHAR(50) NOT NULL UNIQUE,
    password VARBINARY(255) NOT NULL,
    FOREIGN KEY (userId) REFERENCES User(userId) ON DELETE CASCADE
);

-- =======================
-- Procedure: AddUser
-- =======================
DELIMITER //
CREATE PROCEDURE AddUser (
    IN fName VARCHAR(50), 
    IN lName VARCHAR(50), 
    IN emailAddr VARCHAR(100), 
    IN access ENUM('basic', 'admin')
)
BEGIN
    INSERT INTO User (firstName, lastName, email, accessLevel) 
    VALUES (fName, lName, emailAddr, access);
END;
//

-- =======================
-- Procedure: AddLogin
-- =======================
CREATE PROCEDURE AddLogin (
    IN uId INT,
    IN uname VARCHAR(50),
    IN pword VARBINARY(255)
)
BEGIN
    INSERT INTO Login (userId, username, password)
    VALUES (uId, uname, pword);
END;
//

-- =======================
-- Procedure: GetAllUsers
-- =======================
CREATE PROCEDURE GetAllUsers()
BEGIN
    SELECT * FROM User;
END;
//

-- =======================
-- Procedure: GetAllLogins
-- =======================
CREATE PROCEDURE GetAllLogins()
BEGIN
    SELECT loginId, userId, username FROM Login;
END;
//

-- =======================
-- Procedure: UpdateUserEmail
-- =======================
CREATE PROCEDURE UpdateUserEmail (
    IN uId INT,
    IN newEmail VARCHAR(100)
)
BEGIN
    UPDATE User SET email = newEmail WHERE userId = uId;
END;
//

-- =======================
-- Procedure: DeleteUser
-- =======================
CREATE PROCEDURE DeleteUser (
    IN uId INT
)
BEGIN
    DELETE FROM User WHERE userId = uId;
END;
//

-- =======================
-- Procedure: DeleteLogin
-- =======================
CREATE PROCEDURE DeleteLogin (
    IN lId INT
)
BEGIN
    DELETE FROM Login WHERE loginId = lId;
END;
//
DELIMITER ;
