CREATE DATABASE project;
drop database project;
USE project;
show tables;

CREATE TABLE employee (
    Employee_ID INT PRIMARY KEY,
    Employee_Name VARCHAR(100) NOT NULL,
    Age INT,
    Gender VARCHAR(5),
    Department_ID INT,
    Job_ID INT,
    FOREIGN KEY (Department_ID) REFERENCES department(Department_ID) ,
    FOREIGN KEY (Job_ID) REFERENCES jobs(Job_ID)
);
select * from employee;

CREATE TABLE department (
    Department_ID INT PRIMARY KEY,
    Department_Name VARCHAR(100) NOT NULL,
    Location VARCHAR(100)
);
select * from department;

CREATE TABLE jobs (
    Job_ID INT PRIMARY KEY,
    Job_Title VARCHAR(100) NOT NULL,
    Min_Salary FLOAT,
    Max_Salary FLOAT
);
select * from jobs;

CREATE TABLE performance_reviews (
    Review_ID INT PRIMARY KEY,
    Employee_ID INT,
    Performance_Score INT,
    Review_Date DATE,
    FOREIGN KEY (Employee_ID) REFERENCES employee(Employee_ID) ON DELETE CASCADE
);
select * from performance_reviews;

CREATE TABLE salaries (
    Salary_ID INT PRIMARY KEY,
    Employee_ID INT,
    Annual_Salary FLOAT NOT NULL,
    Effective_Date DATE NOT NULL,
    FOREIGN KEY (Employee_ID) REFERENCES employee(Employee_ID) ON DELETE CASCADE
);
select * from salaries;

CREATE TABLE Training_Programs (
    Program_ID INT PRIMARY KEY,
    Program_Name VARCHAR(100),
    Employee_ID INT,
    Start_Date DATE,
    End_Date DATE,
    FOREIGN KEY (Employee_ID) REFERENCES Employee(Employee_ID)
);
select * from training_programs;

CREATE TABLE Employee_Leave (
    Leave_ID INT PRIMARY KEY,
    Employee_ID INT,
    Leave_Type VARCHAR(50),
    Start_Date DATE,
    End_Date DATE,
    Leave_Status VARCHAR(50),
    FOREIGN KEY (Employee_ID) REFERENCES Employee(Employee_ID)
);
select * from employee_leave;

CREATE TABLE employee_personal_details (
    Employee_ID INT PRIMARY KEY,
    Marital_Status VARCHAR(50),
    Nationality VARCHAR(50),
    City_of_Residence VARCHAR(100),
    Email VARCHAR(100),
    Address VARCHAR(255),
    FOREIGN KEY (Employee_ID) REFERENCES employee(Employee_ID)
);
select * from employee_personal_details;

CREATE TABLE projects (
    Salary_ID INT PRIMARY KEY,
    Employee_ID INT,
    Annual_Salary Decimal(10,2),
    Project_Name VARCHAR(100),
    Project_Difficulty_Level INT,
    FOREIGN KEY (Employee_ID) REFERENCES employee(Employee_ID)
);
select * from projects;

-- Basic Queries
-- 1. List all employees along with their departments
SELECT e.Employee_Name, d.Department_Name
FROM Employee e
JOIN Department d ON e.Department_ID = d.Department_ID;
-- 2.Find employees in the 'Sales' department:
SELECT Employee_Name, Age
FROM Employee e
JOIN Department d ON e.Department_ID = d.Department_ID
WHERE d.Department_Name = 'Sales';
-- 3. Get the average salary of all employees:
SELECT AVG(Annual_Salary) AS Average_Salary 
FROM Salaries;
-- 4. Order by City_of_Residence
SELECT * 
FROM employee_personal_details
ORDER BY City_of_Residence;	
-- 5. Fetch project details where difficulty level is greater than 3
SELECT Project_Name, Project_Difficulty_Level FROM projects
WHERE Project_Difficulty_Level > 3
Order by Project_Difficulty_Level;

-- Advanced Queries
-- 1. Find the top 5 highest-paid employees
SELECT e.Employee_Name, s.Annual_Salary
FROM Employee e
JOIN Salaries s ON e.Employee_ID = s.Employee_ID
ORDER BY s.Annual_Salary DESC
LIMIT 5;
-- 2. Analyze the average performance score by department
SELECT d.Department_Name, AVG(p.Performance_Score) AS Avg_Performance
FROM Employee e
JOIN Department d ON e.Department_ID = d.Department_ID
JOIN Performance_Reviews p ON e.Employee_ID = p.Employee_ID
GROUP BY d.Department_Name;
-- 3.Get the total salary expenditure per department
SELECT d.Department_Name, SUM(s.Annual_Salary) AS Total_Expenditure
FROM Employee e
JOIN Salaries s ON e.Employee_ID = s.Employee_ID
JOIN Department d ON e.Department_ID = d.Department_ID
GROUP BY d.Department_Name;
-- 4. Find employees who have a performance score above the department average:
SELECT e.Employee_Name, p.Performance_Score, d.Department_Name
FROM Employee e
JOIN Performance_Reviews p ON e.Employee_ID = p.Employee_ID
JOIN Department d ON e.Department_ID = d.Department_ID
WHERE p.Performance_Score > (
    SELECT AVG(p.Performance_Score)
    FROM Employee e
    JOIN Performance_Reviews p ON e.Employee_ID = p.Employee_ID
    WHERE e.Department_ID = e.Department_ID
)order by d.department_name;
-- 5.Find employees who have attended training programs and are currently on leave
SELECT e.Employee_Name, tp.Program_Name, el.Leave_Type
FROM employee e
JOIN Training_Programs tp ON e.Employee_ID = tp.Employee_ID
JOIN Employee_Leave el ON e.Employee_ID = el.Employee_ID
WHERE el.Leave_Status = 'Approved';

-- Functions
-- 1. Get the total number of employees in a department
SELECT TotalEmployeesInDept('Finance');
-- 2. Calculate the average salary in a department
SELECT AvgSalaryInDept('HR');
-- 3. Get the highest salary for a specific job
SELECT MaxSalaryForJob(1);
-- 4. Calculate total number of projects assigned to an employee
SELECT get_project_count(90);
-- 5. Get employee nationality by Employee_ID
SELECT get_employee_nationality(3);

-- Procedure
-- 1.Insert a new employee
CALL InsertEmployee(101,'ABCD', 43, 'Male', 3, 2);
select * from Employee;
-- 2.Update an employee's salary
CALL UpdateSalary(100,45000);
-- 3. Delete an employee by ID
CALL DeleteEmployee(101);
select * from Employee;
-- 4.Add a new training program for an employee
CALL add_training_program();
-- 5. Update employee performance score
CALL update_performance_score();

-- Views
-- 1. Views for Salary above 50,000
SELECT * FROM salarycheck;
-- 2.View for Count of Employees by Department
SELECT * FROM empcountbydept;
-- 3.  Employees with their last performance review score
SELECT * FROM employee_performance;
-- 4. Employees currently on leave
SELECT * FROM employees_on_leave;
-- 5. Salaries of employees who have attended training programs
SELECT * FROM employees_with_training_salaries;

-- Trigger: Automatically update the maximum salary for a job when a new salary is inserted

