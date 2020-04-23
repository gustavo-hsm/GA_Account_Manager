CREATE DATABASE GA_Account_Summary;

USE GA_Account_Summary;

CREATE TABLE Account(
    id INT AUTO_INCREMENT PRIMARY KEY,
    id_analytics INT UNIQUE NOT NULL,
    txt_account_name VARCHAR(255)
);

CREATE TABLE Property(
    id INT AUTO_INCREMENT PRIMARY KEY,
    id_analytics VARCHAR(100) UNIQUE NOT NULL,
    id_account INT NOT NULL,
    txt_property_name VARCHAR(255),
    FOREIGN KEY (id_account)
        REFERENCES Account(id)
        ON UPDATE CASCADE ON DELETE CASCADE
);

CREATE TABLE View(
    id INT AUTO_INCREMENT PRIMARY KEY,
    id_analytics INT UNIQUE NOT NULL,
    id_property INT NOT NULL,
    txt_view_name VARCHAR(255),
    FOREIGN KEY (id_property)
        REFERENCES Property(id)
        ON UPDATE CASCADE ON DELETE CASCADE
);

CREATE TABLE User(
    id INT AUTO_INCREMENT PRIMARY KEY,
    id_analytics INT NOT NULL,
    id_account INT NOT NULL,
    txt_user_email VARCHAR(255),
    txt_user_local_permission VARCHAR(255),
    txt_user_global_permission VARCHAR(255),
    FOREIGN KEY (id_account)
        REFERENCES Account(id)
        ON UPDATE CASCADE ON DELETE CASCADE
);