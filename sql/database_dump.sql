CREATE DATABASE poc_jira_langchain_bedrock_rds;
USE poc_jira_langchain_bedrock_rds;
CREATE TABLE employees (
   id int NOT NULL,
   first_name varchar(255) NOT NULL,
   last_name varchar(255),
   email varchar(255),
   gender varchar(255),
   salary double
);
INSERT INTO employees (id, first_name, last_name, gender, email, salary) VALUES (1, 'Alice', 'Aaron', 'female', 'alice@company_a.com', 2000);
INSERT INTO employees (id, first_name, last_name, gender, email, salary) VALUES (2, 'Bob', 'Biron', 'male', 'bob@company_b.com', 1000);
INSERT INTO employees (id, first_name, last_name, gender, email, salary) VALUES (3, 'Caroline', 'Cameron', 'female', 'caroline@company_c.com', 3000);
INSERT INTO employees (id, first_name, last_name, gender, email, salary) VALUES (4, 'Doug', 'Duran', 'male', 'doug@company_d.com', 1500);