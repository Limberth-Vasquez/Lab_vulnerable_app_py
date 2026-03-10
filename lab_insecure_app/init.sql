CREATE DATABASE vulnerable_db;
GO

USE vulnerable_db;
GO

CREATE TABLE users (
    id INT PRIMARY KEY IDENTITY(1,1),
    username NVARCHAR(50),
    password NVARCHAR(50)
);
GO

INSERT INTO users (username, password) VALUES
('admin','admin123'),
('limberth','1234'),
('test','test123');
GO
