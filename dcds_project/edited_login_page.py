import streamlit as st
import mysql.connector as m
from mysql.connector import Error
import pandas as pd

# Database connection details
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'mysql2201',
    'database': 'project'
}

# Function to connect to the database with error handling
def connect_db():
    try:
        mc = m.connect(**db_config)
        if mc.is_connected():
            print("Connection Successful")
        return mc
    except Error as e:
        st.error(f"Error connecting to the database: {e}")
        return None

def view_employee_by_name(emp_name):
    conn = connect_db()
    if conn.is_connected():
        with conn.cursor() as cursor:
            query = """
                SELECT e.Employee_ID, e.Employee_Name, e.Age, e.Gender, e.Department_ID, e.Job_ID, s.Annual_Salary 
                FROM Employee e 
                JOIN Salaries s ON e.Employee_ID = s.Employee_ID 
                WHERE e.Employee_Name = %s
            """
            cursor.execute(query, (emp_name,))
            employee = cursor.fetchone()
            # Fetch all remaining rows to clear the cursor
            cursor.fetchall()

        conn.close()  # Close the connection once done

        if employee:
            return {
                'Employee_ID': employee[0],
                'Employee_Name': employee[1],
                'Age': employee[2],
                'Gender': employee[3],
                'Department_ID': employee[4],
                'Job_ID': employee[5],
                'Annual_Salary': employee[6]
            }
        else:
            return {'error': 'Employee not found'}
    else:
        return {'error': 'Database connection failed'}

def view_all_employees():
    conn = connect_db()
    if conn:
        try:
            with conn.cursor() as cursor:
                query = "SELECT * FROM Employee"
                cursor.execute(query)
                employees = cursor.fetchall()
            if employees:
                columns = ["Employee_ID", "Employee_Name", "Age", "Gender", "Department_ID", "Job_ID"]
                df = pd.DataFrame(employees, columns=columns)
                return df
            else:
                return None
        finally:
            conn.close()
    else:
        return None

def edit_employee_by_name(emp_name, field, new_value):
    # Validate the field to ensure it matches allowed columns
    valid_fields = ["Employee_Name", "Age", "Gender", "Department_ID", "Job_ID"]
    if field not in valid_fields:
        return False  # Return False if field is not valid

    conn = connect_db()
    if conn:
        with conn.cursor() as cursor:
            # Use the validated field and parameterize the new value and employee name
            query = f"UPDATE Employee SET {field} = %s WHERE Employee_Name = %s"
            cursor.execute(query, (new_value, emp_name))
            conn.commit()
            # Return True if any row was updated
            return cursor.rowcount > 0

        conn.close()
    return False


def add_employee(emp_id, name, age, gender, department_id, job_id):
    conn = connect_db()
    if conn and conn.is_connected():
        with conn.cursor() as cursor:
            query = """
                INSERT INTO Employee (Employee_ID, Employee_Name, Age, Gender, Department_ID, Job_ID)
                VALUES (%s, %s, %s, %s, %s, %s)
            """
            cursor.execute(query, (emp_id, name, age, gender, department_id, job_id))
            conn.commit()  # Commit the transaction to save changes in the database
            rowcount = cursor.rowcount  # Check if the row was inserted successfully
        conn.close()  # Close the connection
        return rowcount > 0  # Return True if row was added, otherwise False
    return False  # Return False if connection failed


def delete_employee(emp_id):
    conn = connect_db()
    if conn and conn.is_connected():
        with conn.cursor() as cursor:
            query = "DELETE FROM Employee WHERE Employee_ID = %s"
            cursor.execute(query, (emp_id,))
            conn.commit()  # Commit the transaction to save changes in the database
            rowcount = cursor.rowcount  # Check if a row was deleted
        conn.close()  # Close the connection
        return rowcount > 0  # Return True if row was deleted, otherwise False
    return False  # Return False if connection failed


# Login Page
def login():
    st.title("Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        if username == "admin" and password == "1234":
            st.session_state["logged_in"] = True
            st.success("Logged in successfully!")
        else:
            st.error("Invalid username or password")

# Main HR Management Interface
def main_app():
    st.title("HR Management System")

    # View Employee Section
    st.header("View Employee Details")
    view_emp_name = st.text_input("Enter Employee Name to View")
    if st.button("View Employee"):
        if view_emp_name:
            result = view_employee_by_name(view_emp_name)
            if 'error' in result:
                st.error(result['error'])
            else:
                st.json(result)
        else:
            st.warning("Please enter an Employee Name.")

    # View All Employees Section in Tabular Format
    if st.button("View All Employees"):
        employees_df = view_all_employees()
        if employees_df is not None:
            st.dataframe(employees_df)
        else:
            st.warning("No employees found.")

    # Edit Employee Section
    st.header("Edit Employee Details")
    edit_emp_name = st.text_input("Enter Employee Name to Edit")
    edit_field = st.selectbox("Select Field to Edit", ["Employee_Name", "Age", "Gender", "Department_ID", "Job_ID"])
    new_value = st.text_input(f"Enter new value for {edit_field}")
    if st.button("Edit Employee"):
        if edit_emp_name and new_value:
            success = edit_employee_by_name(edit_emp_name, edit_field, new_value)
            if success:
                st.success("Employee details updated successfully.")
            else:
                st.error("Update failed.")
        else:
            st.warning("Please provide both Employee Name and new value.")

    # Add Employee Section
    st.header("Add New Employee")
    new_emp_id = st.text_input("Employee ID")
    new_name = st.text_input("Employee Name")
    new_age = st.number_input("Age", min_value=18, max_value=100, step=1)
    new_gender = st.selectbox("Gender", ["M", "F"])
    new_department_id = st.number_input("Department ID", step=1)
    new_job_id = st.number_input("Job ID", step=1)

    if st.button("Add Employee"):
        if new_emp_id and new_name:
            success = add_employee(new_emp_id, new_name, new_age, new_gender, new_department_id, new_job_id)
            if success:
                st.success("Employee added successfully.")
            else:
                st.error("Failed to add employee.")
        else:
            st.warning("Please fill in all the details to add an employee.")

    # Delete Employee Section
    st.header("Delete Employee")
    delete_emp_id = st.text_input("Enter Employee ID to Delete")
    if st.button("Delete Employee"):
        if delete_emp_id:
            success = delete_employee(delete_emp_id)
            if success:
                st.success("Employee deleted successfully.")
            else:
                st.error("Failed to delete employee or Employee ID not found.")
        else:
            st.warning("Please enter an Employee ID.")

# Check if user is logged in
if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False

if st.session_state["logged_in"]:
    main_app()
else:
    login()
