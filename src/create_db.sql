-- Create table employers and vacancies

-- Create table employers

CREATE TABLE employers(
    employer_id int NOT NULL,
    name VARCHAR(50) NOT NULL,
    url VARCHAR(100)
);

-- Create table vacancies

CREATE TABLE vacancies(
    vacancy_id int NOT NULL,
    employer_id int REFERENCES employers(employer_id) NOT NULL,
    hh_vac_id int NOT NULL,
    alternate_url varchar(100) NOT NULL,
    area varchar(20),
    published_at date NOT NULL,
    employment varchar(100),
    experience varchar(100),
    name varchar(100) NOT NULL",
    salary_from int,
    salary_to int,
    requirement varchar,
    responsibility varchar
);

-- Constraint primary keys

ALTER TABLE employers
    ADD CONSTRAINT pk_employers PRIMARY KEY (employer_id);

ALTER TABLE vacancies
    ADD CONSTRAINT pk_vacancies PRIMARY KEY (vacancy_id);

-- Constraint foreign key

ALTER TABLE vacancies
    ADD CONSTRAINT fk_vacancies_employers
    FOREIGN KEY (employer_id) REFERENCES employers(employer_id);
