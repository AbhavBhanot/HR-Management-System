import mysql.connector as m

def connect_to_database():
    mc = m.connect(host='localhost', user='root', password='mysql2201', database='project')
    if mc.is_connected():
        print("Connection Successful")
    return mc

def view_employee(cursor):
    emp_name = input("Enter Employee Name: ")
    command = """
        SELECT e.Employee_ID, e.Employee_Name, e.Age, e.Gender, e.Department_ID, e.Job_ID, s.Annual_Salary
        FROM Employee e
        JOIN Salaries s ON e.Employee_ID = s.Employee_ID
        WHERE e.Employee_Name = %s
    """
    cursor.execute(command, (emp_name,))
    employee_details = cursor.fetchone()
    if employee_details:
        print("Employee Details:")
        print(f"ID: {employee_details[0]}, Name: {employee_details[1]}, Age: {employee_details[2]}, Gender: {employee_details[3]}, "
              f"Department ID: {employee_details[4]}, Job ID: {employee_details[5]}, Salary: {employee_details[6]}")
    else:
        print("Employee not found.")

def view_all_employees(cursor):
    print("Viewing all employees in the Employee table:")
    cursor.execute("SELECT * FROM Employee")
    employees = cursor.fetchall()
    for emp in employees:
        print(emp)
    
    print("\nViewing all employees in the Salaries table:")
    cursor.execute("SELECT * FROM Salaries")
    salaries = cursor.fetchall()
    for salary in salaries:
        print(salary)

def edit_employee(cursor, connection):
    emp_name = input("Enter Employee Name to edit: ")
    cursor.execute("SELECT * FROM Employee WHERE Employee_Name = %s", (emp_name,))
    employee = cursor.fetchone()
    if not employee:
        print("Employee not found.")
        return

    print("1. Edit Name\n2. Edit Age\n3. Edit Gender\n4. Edit Department ID\n5. Edit Job ID\n6. Edit Salary")
    edit_choice = int(input("Choose the detail you want to edit: "))

    if edit_choice == 1:
        new_name = input("Enter new name: ")
        cursor.execute("UPDATE Employee SET Employee_Name = %s WHERE Employee_Name = %s", (new_name, emp_name))
    elif edit_choice == 2:
        new_age = int(input("Enter new age: "))
        cursor.execute("UPDATE Employee SET Age = %s WHERE Employee_Name = %s", (new_age, emp_name))
    elif edit_choice == 3:
        new_gender = input("Enter new gender (M/F): ")
        cursor.execute("UPDATE Employee SET Gender = %s WHERE Employee_Name = %s", (new_gender, emp_name))
    elif edit_choice == 4:
        new_department_id = int(input("Enter new Department ID: "))
        cursor.execute("UPDATE Employee SET Department_ID = %s WHERE Employee_Name = %s", (new_department_id, emp_name))
    elif edit_choice == 5:
        new_job_id = int(input("Enter new Job ID: "))
        cursor.execute("UPDATE Employee SET Job_ID = %s WHERE Employee_Name = %s", (new_job_id, emp_name))
    elif edit_choice == 6:
        new_salary = float(input("Enter new salary: "))
        cursor.execute("UPDATE Salaries SET Annual_Salary = %s WHERE Employee_ID = %s", (new_salary, employee[0]))
    else:
        print("Invalid choice.")
        return

    connection.commit()
    print("Employee details updated successfully.")

def add_employee(cursor, connection):
    emp_id = int(input("Enter Employee ID: "))
    emp_name = input("Enter employee name: ")
    emp_age = int(input("Enter employee age: "))
    emp_gender = input("Enter gender (M/F): ")
    dept_id = int(input("Enter Department ID: "))
    job_id = int(input("Enter Job ID: "))

    command_emp = """INSERT INTO Employee (Employee_ID, Employee_Name, Age, Gender, Department_ID, Job_ID)
        VALUES (%s, %s, %s, %s, %s, %s)"""
    cursor.execute(command_emp, (emp_id, emp_name, emp_age, emp_gender, dept_id, job_id))
    connection.commit()
    print("New employee added successfully.")

def delete_employee(cursor, connection):
    emp_name = input("Enter Employee Name to delete: ")
    cursor.execute("SELECT * FROM Employee WHERE Employee_Name = %s", (emp_name,))
    employee = cursor.fetchone()
    if not employee:
        print("Employee not found.")
        return

    confirm = input("Are you sure you want to delete this employee? (yes/no): ").lower()
    if confirm == 'yes':
        cursor.execute("DELETE FROM Employee WHERE Employee_Name = %s", (emp_name,))
        cursor.execute("DELETE FROM Salaries WHERE Employee_ID = %s", (employee[0],))
        connection.commit()
        print("Employee deleted successfully.")
    else:
        print("Deletion canceled.")

def main():
    connection = connect_to_database()
    if not connection:
        return

    cursor = connection.cursor()

    while True:
        print("\nHR Management System")
        print("1. View employee details by name")
        print("2. View all employees in tables")
        print("3. Edit employee details by name")
        print("4. Add new employee")
        print("5. Delete employee by name")
        print("6. Exit")

        try:
            choice = int(input("Enter your choice: "))
        except ValueError:
            print("Invalid input. Please enter a number.")
            continue

        if choice == 1:
            view_employee(cursor)
        elif choice == 2:
            view_all_employees(cursor)
        elif choice == 3:
            edit_employee(cursor, connection)
        elif choice == 4:
            add_employee(cursor, connection)
        elif choice == 5:
            delete_employee(cursor, connection)
        elif choice == 6:
            print("Exiting the HR Management System.")
            break
        else:
            print("Invalid choice. Please select an option between 1-6.")

    cursor.close()
    connection.close()

if __name__ == "__main__":
    main()
