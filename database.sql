-- Create the database
CREATE DATABASE IF NOT EXISTS churn_prediction;
USE churn_prediction;

-- Create the main customers table
CREATE TABLE IF NOT EXISTS customers (
    customer_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    age INT NOT NULL,
    payments_made INT NOT NULL,
    purchases INT NOT NULL,
    is_active TINYINT(1) NOT NULL
);

-- Create the churned_customers table
CREATE TABLE IF NOT EXISTS churned_customers (
    customer_id INT NOT NULL,
    name VARCHAR(255) NOT NULL,
    payments_made INT NOT NULL,
    is_active TINYINT(1) NOT NULL,
    PRIMARY KEY (customer_id)
);
