-- show databases;

create database OpenBank;
use OpenBank;

CREATE TABLE users (
    id INT PRIMARY KEY AUTO_INCREMENT,
    username VARCHAR(64) NOT NULL UNIQUE,
    FIO VARCHAR(64) NOT NULL,
    balance INT DEFAULT 0,
    isBanned BOOLEAN DEFAULT FALSE,
    isOrg BOOLEAN DEFAULT FALSE
);


CREATE TABLE transactions (
    id INT PRIMARY KEY AUTO_INCREMENT,
    `from` INT,
    `to` INT,
    `datetime` DATETIME NOT NULL,
    sum INT NOT NULL,
    FOREIGN KEY (`from`) REFERENCES users (id),
    FOREIGN KEY (`to`) REFERENCES users (id),
    INDEX (`from`),
    INDEX (`to`)
);

CREATE TABLE creditRequest (
    id INT PRIMARY KEY AUTO_INCREMENT,
    userId INT NOT NULL,
    purpose VARCHAR(128) NOT NULL,
    `status` INT NOT NULL,
    FOREIGN KEY (userId) REFERENCES users (id),
    INDEX (userId)
);

CREATE TABLE taxes (
    id INT PRIMARY KEY AUTO_INCREMENT,
    `name` VARCHAR(32) NOT NULL,
    `datetime` DATETIME NOT NULL,
    sum INT NOT NULL
);

CREATE TABLE taxesPayment (
    id INT PRIMARY KEY AUTO_INCREMENT,
    userId INT NOT NULL,
    taxId INT NOT NULL,
    FOREIGN KEY (userId) REFERENCES users (id),
    FOREIGN KEY (taxId) REFERENCES taxes (id),
    INDEX (userId),
    INDEX (taxId)
);


-- select * from users;
-- select * from creditrequest;
-- select * from taxes;
-- select * from taxespayment;
-- select * from transactions;
-- drop database openbank; 