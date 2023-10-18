-- SQL script for create tables: employers and vacancies

-- Drop tables

DROP TABLE IF EXISTS vacancies;
DROP TABLE IF EXISTS employers;

-- Create table employers

CREATE TABLE employers(
    employer_id int PRIMARY KEY,
    name VARCHAR(50) NOT NULL,
    url VARCHAR(100)
);

-- Create table vacancies

CREATE TABLE vacancies(
    vacancy_id int PRIMARY KEY,
    employer_id int REFERENCES employers(employer_id) ON DELETE CASCADE NOT NULL,
    alternate_url varchar(100) NOT NULL,
    area varchar(20),
    published_date date NOT NULL,
    employment varchar(100),
    experience varchar(100),
    name varchar(100) NOT NULL,
    salary_from int,
    salary_to int,
    requirement varchar,
    responsibility varchar
);
