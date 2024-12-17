-- show databases;

CREATE DATABASE OpenBank_ver02;
USE OpenBank_ver02;

CREATE TABLE users (
    id INT PRIMARY KEY AUTO_INCREMENT,
    username VARCHAR(64) NOT NULL UNIQUE,
    FIO VARCHAR(64) NOT NULL,
    balance DECIMAL(10, 2) DEFAULT 0.00,
    is_banned BOOLEAN DEFAULT FALSE,
    is_org BOOLEAN DEFAULT FALSE
) COMMENT 'Таблица для хранения информации о пользователях';

CREATE TABLE transactions (
    id INT PRIMARY KEY AUTO_INCREMENT,
    sender_id INT,
    recipient_id INT,
    transaction_datetime DATETIME NOT NULL,
    amount DECIMAL(10, 2) NOT NULL,
    FOREIGN KEY (sender_id) REFERENCES users (id),
    FOREIGN KEY (recipient_id) REFERENCES users (id),
    INDEX (sender_id),
    INDEX (recipient_id)
) COMMENT 'Таблица для хранения транзакций между пользователями';

CREATE TABLE credit_requests (
    id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT NOT NULL,
    purpose VARCHAR(128),
    status INT NOT NULL DEFAULT 0,
    amount DECIMAL(10, 2) NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users (id),
    INDEX (user_id)
) COMMENT 'Таблица для хранения запросов на кредит';

CREATE TABLE taxes (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(32) NOT NULL,
    due_datetime DATETIME NOT NULL,
    amount DECIMAL(10, 2) NOT NULL
) COMMENT 'Таблица для хранения информации о налогах';

CREATE TABLE tax_payments (
    id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT NOT NULL,
    tax_id INT NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users (id),
    FOREIGN KEY (tax_id) REFERENCES taxes (id),
    INDEX (user_id),
    INDEX (tax_id)
) COMMENT 'Таблица для хранения платежей по налогам';

CREATE TABLE credit_payments (
    id INT PRIMARY KEY AUTO_INCREMENT,
    credit_request_id INT NOT NULL,
    user_id INT NOT NULL,
    amount DECIMAL(10, 2) NOT NULL,
    payment_datetime DATETIME NOT NULL,
    is_paid BOOLEAN DEFAULT FALSE,
    FOREIGN KEY (credit_request_id) REFERENCES credit_requests(id),
    FOREIGN KEY (user_id) REFERENCES users (id),
    INDEX (credit_request_id),
    INDEX (user_id)
) COMMENT 'Таблица для хранения платежей по кредитам';

-- select * from users; 
-- select * from credit_requests;
-- select * from taxes;
-- select * from tax_payments;
-- select * from transactions;
-- select * from credit_payments;
-- drop database openbank;