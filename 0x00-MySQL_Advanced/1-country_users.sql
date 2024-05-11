-- create table users with
-- country, enumeration of countries: US, CO and TN, never null (= default will be the first element of the enumeration, here US)
CREATE TABLE IF NOT EXISTS users (
    id INT NOT NULL AUTO_INCREMENT,
    email VARCHAR(255) NOT NULL,
    name VARCHAR(255),
    country ENUM('US', 'CO', 'TN') DEFAULT 'US',
    PRIMARY KEY (id),
    UNIQUE KEY email (email)
);
