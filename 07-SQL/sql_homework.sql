---------------------------------------------------------------------------
--create table for employees
---------------------------------------------------------------------------
CREATE TABLE employees (
    emp_no SERIAL PRIMARY KEY,
	birth_date DATE,
    first_name VARCHAR NOT NULL,
	last_name VARCHAR NOT NULL,
	gender VARCHAR NOT NULL,
	hire_date DATE
);

---------------------------------------------------------------------------
--create table for departments
--------------------------------------------------------------------------
CREATE TABLE departments (
    dept_no VARCHAR PRIMARY KEY,
	dept_name VARCHAR
);

---------------------------------------------------------------------------
--create table for salaries
---------------------------------------------------------------------------
CREATE TABLE salaries (
    emp_no INTEGER,
	FOREIGN KEY (emp_no) REFERENCES employees(emp_no),
	salary INTEGER,
	from_date DATE,
	to_date DATE
);
SELECT COUNT(*) FROM salaries;
---------------------------------------------------------------------------
--create table for titles
---------------------------------------------------------------------------
CREATE TABLE titles (
    emp_no INTEGER,
	FOREIGN KEY (emp_no) REFERENCES employees(emp_no),
	title VARCHAR,
	from_date DATE,
	to_date DATE
);

---------------------------------------------------------------------------
--create table for dept_manager
---------------------------------------------------------------------------
CREATE TABLE dept_manager (
    dept_no VARCHAR,
	FOREIGN KEY (dept_no) REFERENCES departments(dept_no),
	emp_no INTEGER,
	FOREIGN KEY (emp_no) REFERENCES employees(emp_no),
	from_date DATE,
	to_date DATE
);

---------------------------------------------------------------------------
--create table for dept_emp
---------------------------------------------------------------------------
CREATE TABLE dept_emp (
	emp_no INTEGER,
	FOREIGN KEY (emp_no) REFERENCES employees(emp_no),
	dept_no VARCHAR,
	FOREIGN KEY (dept_no) REFERENCES departments(dept_no),
	from_date DATE,
	to_date DATE
);

---------------------------------------------------------------------------
--read tables
---------------------------------------------------------------------------
SELECT * FROM employees;
SELECT COUNT(*) FROM employees;
SELECT * FROM departments;
SELECT * FROM dept_emp;
SELECT * FROM dept_manager;
SELECT * FROM salaries;
SELECT * FROM titles;

---------------------------------------------------------------------------
--Code for query 1 - List the following details of each employee: 
--employee number, last name, first name, gender, and salary.
---------------------------------------------------------------------------

SELECT e.emp_no, e.last_name, e.first_name, e.gender, s.salary
FROM employees AS e
JOIN salaries AS s 
ON e.emp_no = s.emp_no;


---------------------------------------------------------------------------
--Code for query 2 - List employees who were hired in 1986
--------------------------------------------------------------------------
SELECT *
FROM employees
WHERE EXTRACT(year FROM "hire_date") = 1986;

---------------------------------------------------------------------------
--Code for query 3 - List the manager of each department with the following 
--information: department number, department name, the manager's employee 
--number, last name, first name, and start and end employment dates.
--------------------------------------------------------------------------

SELECT dm.dept_no, d.dept_name, dm.emp_no, e.last_name, e.first_name, dm.from_date, dm.to_date
FROM departments d
    JOIN dept_manager dm
        ON d.dept_no = dm.dept_no
            JOIN employees e
                ON dm.emp_no = e.emp_no;
                            
---------------------------------------------------------------------------
--Code for query 4 - List the department of each employee with the following 
--information: employee number, last name, first name, and department name.
---------------------------------------------------------------------------

SELECT e.emp_no, e.last_name, e.first_name, de.dept_no, d.dept_name
FROM employees e
	JOIN dept_emp de
		ON e.emp_no = de.emp_no
			JOIN departments d
				ON de.dept_no = d.dept_no;

---------------------------------------------------------------------------
--Code for query 5 - List all employees whose first name is "Hercules" and 
--last names begin with "B."
---------------------------------------------------------------------------

SELECT emp_no, first_name, last_name
FROM employees
WHERE first_name = 'Hercules' AND last_name LIKE 'B%';


---------------------------------------------------------------------------
--Code for query 6 - List all employees in the Sales department, including 
--their employee number, last name, first name, and department name.
---------------------------------------------------------------------------

SELECT e.emp_no, e.last_name, e.first_name, de.dept_no, d.dept_name
FROM employees e
	JOIN dept_emp de
		ON e.emp_no = de.emp_no
			JOIN departments d
				ON de.dept_no = d.dept_no
WHERE dept_name = 'Sales';

---------------------------------------------------------------------------
--Code for query 7 - List all employees in the Sales and Development 
--departments, including their employee number, last name, first name, and 
--department name.
---------------------------------------------------------------------------

SELECT e.emp_no, e.last_name, e.first_name, de.dept_no, d.dept_name
FROM employees e
	JOIN dept_emp de
		ON e.emp_no = de.emp_no
			JOIN departments d
				ON de.dept_no = d.dept_no
WHERE dept_name = 'Sales' OR dept_name = 'Development';

---------------------------------------------------------------------------
--Code for query 8 - In descending order, list the frequency count of 
--employee last names, i.e., how many employees share each last name.
---------------------------------------------------------------------------

SELECT last_name,  COUNT(last_name) FROM employees
GROUP by last_name
ORDER by last_name DESC;

