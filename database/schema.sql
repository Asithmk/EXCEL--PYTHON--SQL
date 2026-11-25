CREATE DATABASE IF NOT EXISTS student_analytics;

USE student_analytics;

CREATE TABLE IF NOT EXISTS students (
    student_id INT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    average_grade DECIMAL(4,2),
    nationality VARCHAR(50),
    age DECIMAL(5,2),
    rent DECIMAL(10,2),
    food_cost DECIMAL(10,2),
    iq DECIMAL(5,2),
    ambition VARCHAR(20),
    total_living_cost DECIMAL(10,2),
    ambition_score TINYINT
);