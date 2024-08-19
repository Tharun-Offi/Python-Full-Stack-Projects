CREATE DATABASE iphone_waitlist;
USE iphone_waitlist;

CREATE TABLE customers (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255),
    email VARCHAR(255) UNIQUE,
    phone VARCHAR(255),
    position INT,
    referrals INT DEFAULT 0,
    referral_code VARCHAR(255)
);