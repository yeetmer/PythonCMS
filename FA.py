#General Function
import time
import datetime
import os           
def get_current_time():
    time1 = time.localtime() 
    time_string = time.strftime("%d/%m/%Y, %H:%M:%S", time1)

    return time_string

#Check Student Validation
def check_student_valid(studentid):
    with open('students.txt', 'r') as file:
        for line in file:
            data = line.strip().split(',')
            if studentid == data[0]:
                studentname = data[1]
                return studentname
    return 
def check_password(studentid):
    with open('students.txt', 'r') as file:
        for line in file:
            data = line.strip().split(',')
            if studentid == data[0]:
                attempts = 3
                password = data[4]
                while attempts > 0:
                    user_input = input("Enter the password: ")
                    if user_input == password:
                        print("Password correct. Access granted.")
                        return
                    else:
                        attempts -= 1
                        print(f"Incorrect password. {attempts} attempts left.")
                else:
                    print("Out of attempts. Access denied.")
                    exit()
def display_student_menu():
    print("[1] Mark Attendance")
    print("[2] Check Timetables")
    print("[3] Submit/Check Assignments")
    print("[4] Display")
    print("[5] Exit Program")
    print("")

#Student Attendance Function 
def check_password(studentid):
    with open('students.txt', 'r') as file:
        for line in file:
            data = line.strip().split(',')
            if studentid == data[0]:
                attempts = 3
                password = data[4]
                while attempts > 0:
                    user_input = input("Enter the password: ")
                    if user_input == password:
                        print("Password correct. Access granted.")
                        return
                    else:
                        attempts -= 1
                        print(f"Incorrect password. {attempts} attempts left.")
                else:
                    print("Out of attempts. Access denied.")
                    exit()
def display_student_menu():
    print("[1] Mark Attendance")
    print("[2] Check Timetables")
    print("[3] Submit/Check Assignments")
    print("[4] Display")
    print("[5] Exit Program")

#Student Attendance Function 
def mark_attendance(studentid):
    sid = studentid
    attendancestatus = "ATTENDED"
    input_course_code = input("Please enter the course code: ")
    input_week = input("Enter Current Week: ")
    course_found = False
    
    with open(f'timetables_{sid}.txt', 'r') as file:
        for line in file:
            data = line.strip().split(',')
            if input_course_code == data[0] and input_week == data[2]:
                course_found = True
                course_name = data[1]
                start_time = data[5]
                class_date = data[9]  
                current_time = datetime.datetime.now().strftime("%H:%M:%S")
                current_date = datetime.datetime.now().strftime("%d/%m/%Y")  # Format date as "dd/mm/Y, Y = 4 digits
                class_start_time = datetime.datetime.strptime(start_time, "%H:%M:%S")
                fifteen_minutes_after_start = class_start_time + datetime.timedelta(minutes=15)
                with open(f'attendance_{sid}.txt', 'r+') as attendance_file:
                    lines = attendance_file.readlines()
                    found = False
                    for i, line in enumerate(lines):
                        line_data = line.strip().split(',')
                        if input_course_code == line_data[0] and input_week == line_data[2]:
                            found = True
                            if line_data[3] == '-' and line_data[4] == '-':  # Check for gaps when overwritten
                                if datetime.datetime.strptime(current_time, "%H:%M:%S") <= fifteen_minutes_after_start and current_date == class_date:
                                    new_line = f"{input_course_code},{course_name},{input_week},{current_date},{current_time},{attendancestatus}\n"
                                    #New line to match the original line length
                                    lines[i] = new_line.ljust(len(line))
                                    attendance_file.seek(0)
                                    attendance_file.writelines(lines)
                                    attendance_file.truncate()
                                    print("Attendance marked successfully.")
                                else:
                                    print("Attendance cannot be marked after the first 15 minutes of the class or if the current date does not match the class date.")
                            else:
                                print("Attendance Already MARKED!")
                            break
                    if not found:
                        print("No matching entry found in attendance file.")
                break  
    
    if not course_found:
        print("Course code not found in timetables.")   
def calculate_attendance_percentage(studentid):
    sid = studentid
    total_classes = 0
    attended_classes = 0
    attendance_status = "ATTENDED"
    coursecode = input("Enter course code: ")
    with open(f'attendance_{sid}.txt', 'r') as file:
        for line in file:
            data = line.strip().split(',')
            coursename = data[1]
            if coursecode == data[0]:
                total_classes += 1
            if data[5] == attendance_status:
                attended_classes += 1
                
    if total_classes > 0:
        print (f'Percentage of attendance for course: {str((attended_classes / total_classes) * 100)}')
    
    else:
        print("Course code not found.")
        return 0
def display_multiple_attendance(studentid):
        with open(f'attendance_{studentid}.txt', 'r') as file:
            for line in file:
                data = line.strip().split(',')
                print(f"Course Code: {data[0]}")
                print(f"Course Name: {data[1]}")
                print(f"Checkin Day: {data[2]}")
                print(f"Checkin Time: {data[3]}")
                print(f"Attendance Status: {data[4]}")
                print() 
        print()  

#Student Timetable Function
def create_timetables(studentid):
    sid = studentid
    course_code = input("Enter course code: ")
    course_name = input("Enter course name: ")  
    week = input("Enter week: ")
    credit_hours = input("Enter credit hours: ")  
    day = input("Enter day: ") 
    start_time = input("Enter start time: ")
    end_time = input("Enter end time: ")
    instructor_name = input("Enter instructor name: ")  
    room_name = input("Enter room name: ")
    current_date = input("Enter date: ")  

    with open(f'timetables_{sid}.txt', 'a') as file:  
        file.write(f"{course_code},{course_name},{week},{credit_hours},{day},{start_time},{end_time},{instructor_name},{room_name},{current_date}\n")  
def update_timetable(studentid):
    timetable_entries = []

    with open(f'timetables_{studentid}.txt', 'r') as file:
        for line in file:
            data = line.strip().split(',')
            timetable_entries.append(data)

    print("Available courses:")
    counter = 1
    for entry in timetable_entries:
        print(f"{counter}. Course Code: {entry[0]}, Course Name: {entry[1]}, Week: {entry[2]}")
        counter += 1

    selection = input("Select the number to update (or 'q' to quit): ")

    if selection.lower() == 'q':
        print("Exiting without updates.")
        return

    try:
        selected_index = int(selection) - 1
        selected_entry = timetable_entries[selected_index]
    except (ValueError, IndexError):
        print("Invalid selection.")
        return

    print("Choose which entry do you want to edit.")
    print(f'[1] - [Course Name] {selected_entry[1]}')
    print(f'[2] - [Week] {selected_entry[2]}')
    print(f'[3] - [Credit Hours] {selected_entry[3]}')
    print(f'[4] - [Day] {selected_entry[4]}')
    print(f'[5] - [Start Time] {selected_entry[5]}')
    print(f'[6] - [End Time] {selected_entry[6]}')
    print(f'[7] - [Instructor Name] {selected_entry[7]}')
    print(f'[8] - [Room Name] {selected_entry[8]}')
    print(f'[9] - [Date] {selected_entry[9]}')
    to_change = int(input("Enter selection: "))

    if 1 <= to_change <= 9:
        new_value = input("Enter new value: ")
        selected_entry[to_change] = new_value
    else:
        print("Invalid selection.")

    with open(f'timetables_{studentid}.txt', 'w') as file:
        for entry in timetable_entries:
            file.write(','.join(entry) + '\n')

    print("Timetable updated successfully.")
def delete_timetable_entry(studentid):
    with open(f'timetables_{studentid}.txt', 'r') as file:
        timetable_entries = file.readlines()

    print("Available entries:")
    for index, entry in enumerate(timetable_entries, start=1):
        data = entry.strip().split(',')
        print(f"{index}. Course Code: {data[0]}, Course Name: {data[1]}")

    selection = input("Select the number to delete (or 'q' to quit): ")

    if selection.lower() == 'q':
        print("Exiting without deletion.")
        return

    try:
        selected_index = int(selection) - 1
        if 0 <= selected_index < len(timetable_entries):
            del timetable_entries[selected_index]
        else:
            print("Invalid selection.")
            return
    except ValueError:
        print("Invalid selection.")
        return

    with open(f'timetables_{studentid}.txt', 'w') as file:
        for entry in timetable_entries:
            file.write(entry)

    print("Entry deleted successfully.")

def display_multiple_timetables(studentid):
    timetable_entries = []

    with open(f'timetables_{studentid}.txt', 'r') as file:
        for line in file:
            data = line.strip().split(',')
            timetable_entries.append(data)

    print("Available courses:")
    counter = 1
    for entry in timetable_entries:
        print(f"{counter}. Course Code: {entry[0]}, Course Name: {entry[1]}, Week: {entry[2]}")
        counter += 1

    selection = input("Enter the number of the subject to display details (or 'q' to quit): ")

    if selection.lower() == 'q':
        print("Exiting.")
        return

    try:
        selected_index = int(selection) - 1
        selected_entry = timetable_entries[selected_index]
    except (ValueError, IndexError):
        print("Invalid selection.")
        return

    print("Course Details:")
    print(f"Course Code: {selected_entry[0]}")
    print(f"Course Name: {selected_entry[1]}")
    print(f"Week: {selected_entry[2]}")
    print(f"Credit Hours: {selected_entry[3]}")
    print(f"Day: {selected_entry[4]}")
    print(f"Start Time: {selected_entry[5]}")
    print(f"End Time: {selected_entry[6]}")
    print(f"Instructor Name: {selected_entry[7]}")
    print(f"Room Name: {selected_entry[8]}")
    print(f"Date: {selected_entry[9]}")
    print()

#Student Assignment Function
def submit_assignment(studentid):
    current_datetime = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")  # Get current date and time
    userinput_coursecode = input("Enter course code: ")
    course_found = False  # Track if the course code is found in the timetable
    
    with open(f'timetables_{studentid}.txt', 'r') as file:
        for line in file:
            data = line.strip().split(',')
            if userinput_coursecode == data[0]:
                course_found = True
                coursecode = data[0]
                coursename = data[1]

                assignmentcode = input("Enter assignment code: ")
                if assignmentcode == data[2]:
                    print("Assignment already submitted.")
                    break

                else:
                    assignmentname = input("Enter assignment name: ")
                    submissionstatus = str("Submitted")
                    with open(f'assignments_{studentid}.txt', 'a') as attendance_file:
                        attendance_file.write(f"{coursecode}, {coursename}, {assignmentcode}, {assignmentname}, {current_datetime}, {current_datetime}, {submissionstatus}\n")
                    print("Assignment submitted successfully.")
                    break
    if not course_found:
        print("Course code not found in timetables.")
def display_assignment_codes(studentid):
    subject_assignments = {}

    with open(f'assignments_{studentid}.txt', 'r') as file:
        for line in file:
            data = line.strip().split(',')
            subject_code = data[0]
            assignment_code = data[2]

            if subject_code not in subject_assignments:
                subject_assignments[subject_code] = set() 
            
            subject_assignments[subject_code].add(assignment_code)  

    # Display the available subject codes and assignment codes
    print("Available Subject and Assignment Codes:")
    counter = 1  

    for subject_code, assignments in subject_assignments.items():
        print(f"Subject Code: {subject_code}")
        for assignment_code in assignments:
            print(f"  {counter}. {assignment_code}")
            counter += 1  
def check_assignment_status(studentid, assignment_selection):
    with open(f'assignments_{studentid}.txt', 'r') as file:
        lines = file.readlines()
        try:
            selected_assignment = lines[int(assignment_selection) - 1].strip().split(',')
            print(f"Course Code: {selected_assignment[0]}")
            print(f"Course Name: {selected_assignment[1]}")
            print(f"Assignment Code: {selected_assignment[2]}")
            print(f"Assignment Name: {selected_assignment[3]}")
            print(f"Submission Date: {selected_assignment[4]}")
            print(f"Latest Update Date: {selected_assignment[5]}")
            print(f"Submission Status: {selected_assignment[6]}")
            if len(selected_assignment) > 7 and selected_assignment[7].strip():  # Check if mark is given
                print(f"Mark Given: {selected_assignment[7]}")
            else:
                print("Mark Given: Unmarked")
        except IndexError:
            print("Assignment not found.")
def update_assignment(studentid):
    current_datetime = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")  
    with open(f'assignments_{studentid}.txt', 'r+') as file:
        lines = file.readlines()
        for i, line in enumerate(lines):
            data = line.strip().split(',')
            print(f"[{i+1}] {data[:4]}")
        line_number = int(input("Enter line number to update: ")) - 1
        if 0 <= line_number < len(lines):
            data = lines[line_number].strip().split(',')
            print(f"Course Code: {data[0]}")
            print(f"Course Name: {data[1]}")
            print(f"Assignment Code: [1] {data[2]}")
            print(f"Assignment Name: [2] {data[3]}")
            print(f"Submission Date: {data[4]}")
            print(f"Latest Update Date: {data[5]}")
            print(f"Submission Status: {data[6]}")
            to_change = int(input("Enter selection: ")) 
            if to_change == 1:
                new_assignment_code = input("Enter new assignment code: ")
                data[2] = new_assignment_code
                data[5] = current_datetime
            elif to_change == 2:
                new_assignment_name = input("Enter new assignment name: ")
                data[3] = new_assignment_name
                data[5] = current_datetime
            else:
                print("Invalid selection!")
            lines[line_number] = ','.join(data) + '\n'
            file.seek(0)
            file.writelines(lines)
            file.truncate()
        else:
            print("Invalid line number")
def display_multiple_assignment(studentid):
        with open(f'assignments_{studentid}.txt', 'r') as file:
            for line in file:
                data = line.strip().split(',')
                print(f"Course Code: {data[0]}")
                print(f"Course Name: {data[1]}")
                print(f"Assignment Code: {data[2]}")
                print(f"Assignment Name: {data[3]}")
                print(f"First Submittion Time: {data[4]}")
                print(f"Latest Submittion Time: {data[5]}")
                print(f"Submittion Status: {data[6]}")
                print()  # Add a blank line for readability
        print() 

#Student Program Function
def student_login():
    studentid = input("Please enter your student ID: ")
    result = check_student_valid(studentid)
    if result:
        print("")
        print(f'Welcome, {result}') 
    else:
        print("")
        print("No student record found for the provided ID.")
        exit()
    check_password(studentid)
    print("")
    print(f"Welcome to EduHub University, {result}")


    confirmation = "n"
    while confirmation.lower() != "y":
        display_student_menu()
        userInput = input("Please Enter Your Selection: ")
        print("")

        if userInput == "1": # Mark Attendance
            print("---Mark Attendance---")
            print("[1] Checkin Attendance")
            print("[2] Attendance Percentages")
            print("[Any] Back to Homepage")
            userInputAttendance = input("Please Enter Your Selection: ")
            print("")
            if userInputAttendance == "1":
                print("---Checkin Attendance---")
                mark_attendance(studentid)
                print("")
            elif userInputAttendance == "2":
                print("---Attendance Percentages---")
                calculate_attendance_percentage(studentid)
                print("")
            else:
                pass            
        elif userInput == "2": # Manage Timetables
            print("[1] Display the Current Timetables")
            print("[Any] Back to Homepage")
            userInputtimetable = input("Please Enter Your Selection: ")
            print("")
            if userInputtimetable == "1":
                print("")
                display_multiple_timetables(studentid)
            else:
                pass                  
        
        elif userInput == "3": # Submit/Check Assignments
            print("[1] Submission")
            print("[2] Check Submission Status")
            print("[3] Update Assignment Status")
            print("[Any] Back to Homepage")
            userInputsub = input("Please Enter Your Selection: ")
            print("")
            if userInputsub == "1":
                print("---Submission---")
                submit_assignment(studentid)
            elif userInputsub == "2":
                print("---Check Submission Status---")
                display_assignment_codes(studentid)  
                assignment_selection = input("Enter the assignment line number you want to check: ")
                check_assignment_status(studentid, assignment_selection)
            elif userInputsub == "3":
                print("---Update Assignment Status---")
                update_assignment(studentid)     
            else:
                print("---Back to Homepage---")
        
        elif userInput == "4": # Display
            print("[1] Display Attendance Status")
            print("[2] Display Timetables")
            print("[3] Display Assignments Status")
            print("[Any] Back to Homepage")
            userInputdisplay = input("Please Enter Your Selection. ")
            print("")
            if userInputdisplay == "1":
                print("---Attendance Status---")
                display_multiple_attendance(studentid)
            elif userInputdisplay == "2":
                print("---Timetables---")
                display_multiple_timetables(studentid)
            elif userInputdisplay == "3":
                print("---Check Submission Status---")
                display_assignment_codes(studentid)  
                assignment_selection = input("Enter the assignment line number you want to check: ")
                check_assignment_status(studentid, assignment_selection)
            else:
                print("---Back to Homepage---")

        elif userInput == "5": #  Exit
            confirmation = input("Are You Sure You Want to End Your Session? [Y/N]: ")
            while confirmation.lower() != "y" and confirmation.lower() != "n":
                confirmation = input("Are You Sure You Want to End Your Session? [Y/N]: ")
        else: # Invalid Selection
            print("Invalid Selection!!")
    return 0

#Admin Program Function
def admin_login():
    admin_password = "admin123"
    password_attempt = input("Enter the admin password: ")
    if password_attempt == admin_password:
        print("Admin login successful.")
        print("")
        admin_menu()
    else:
        print("Incorrect password.")
        exit()
def admin_menu():
    while True:
        print("[1] Manage Attendance")
        print("[2] Manage Timetables")
        print("[3] Manage Assignments")
        print("[4] Manage Students")
        print("[5] Exit Program")
        admin_selection = input("Please select an option: ")
        print("")

        if admin_selection == "1": # managing attendance
            print("--- Manage Attendance ---")
            manage_attendance()
        elif admin_selection == "2": #managing timetables
            print("--- Manage Timetables ---")
            manage_timetables()
        elif admin_selection == "3": #manageassignments and give mark
            print("--- Manage Assignments ---")
            manage_assignments()  
        elif admin_selection == "4": #registering new students and generating their 3 .txt files
            print("--- Manage Students ---")
            manage_students()
        elif admin_selection == "5":
            confirmation = input("Are You Sure You Want to End Your Session? [Y/N]: ")
            while confirmation.lower() != "y" and confirmation.lower() != "n":
                confirmation = input("Are You Sure You Want to End Your Session? [Y/N]: ")
            if confirmation.lower() == "y":
                print("Exiting Program...")
                break
        else:
            print("Invalid Selection!!")

    return 0

#Manage Student Attendance
def manage_attendance():
    student_id = input("Enter the student ID: ")

    if check_student_valid(student_id):
        while True:
            print("[1] Edit Attendance")
            print("[2] Go Back")
            choice = input("Enter your choice: ")
            print("")

            if choice == "1":
                edit_attendance(student_id)
            elif choice == "2":
                return
            else:
                print("Invalid choice. Please try again.")
                print("")

    else:
        print("Invalid student ID.")
        print("")
def edit_attendance(student_id):
    subject_code = input("Enter the subject code: ")
    week = input("Enter the week: ")
    print("")

    attendance_file = f'attendance_{student_id}.txt'
    with open(attendance_file, 'r+') as file:
        lines = file.readlines()
        file.seek(0)  

        updated = False
        for i, line in enumerate(lines):
            data = line.strip().split(',')
            if data[0] == subject_code and data[2] == week:
                if data[5] == "ATTENDED":
                    # If attendance was marked as attended, change it to absent
                    data[5] = "ABSENT"
                    lines[i] = ','.join(data) + '\n'
                    updated = True
                    print("Attendance data updated successfully.")
                else:
                    print("Attendance data was already marked as absent.")
                break
        else:
            print("No matching attendance data found.")

        # Write all the lines back to the file
        file.truncate(0)  # Clear the file content
        file.writelines(lines)

        print("")


def load_students():
    global students
    students = {}
    if os.path.exists('students.txt'):
        with open('students.txt', 'r') as file:
            for line in file:
                student_data = line.strip().split(',')
                student_id = student_data[0]
                student_info = {
                    'name': student_data[1],
                    'course': student_data[2],
                    'school': student_data[3],
                    'password': student_data[4]
                }
                students[student_id] = student_info


def save_students():
    with open('students.txt', 'w') as file:
        for student_id, student_info in students.items():
            student_line = ','.join([student_id, student_info['name'], student_info['course'], student_info['school'], student_info['password']])
            file.write(student_line + '\n')
def create_student_files(student_id):
    attendance_file = f'attendance_{student_id}.txt'
    timetable_file = f'timetables_{student_id}.txt'
    assignment_file = f'assignments_{student_id}.txt'

    for file_name in [attendance_file, timetable_file, assignment_file]:
        with open(file_name, 'w'):
            pass  
def delete_student_files(student_id):
    for file_prefix in ['attendance_', 'timetables_', 'assignments_']:
        file_path = f'{file_prefix}{student_id}.txt'
        if os.path.exists(file_path):
            os.remove(file_path)

#Manage Student Function
def manage_students():
    print("Student Management:")
    print("[1] Add Student")
    print("[2] Update Student")
    print("[3] Delete Student")
    print("[4] Back to Admin Menu")

    user_input = input("Enter Your Choice: ")
    print("")

    if user_input == "1":
        add_student()
    elif user_input == "2":
        update_student()
    elif user_input == "3":
        delete_student()
    elif user_input == "4":
        return
    else:
        print("Invalid Selection!!")
def add_student():
    student_id = input("Enter student ID: ")
    student_name = input("Enter student name: ")
    course = input("Enter student course: ")
    school = input("Enter student school: ")
    password = input("Enter student password: ")
    print("")
    
    # Add student to the students dictionary
    students[student_id] = {'name': student_name, 'course': course, 'school': school, 'password': password, 'attendance': []}
    
    # Save the updated student information to file
    save_students()
    
    # Create student files
    create_student_files(student_id)

    print("Student added successfully!")
    print("")
def update_student():
    student_id = input("Enter student ID to update: ")
    if student_id in students:
        new_name = input("Enter updated student name: ")
        new_course = input("Enter updated student course: ")
        new_school = input("Enter updated student school: ")
        new_password = input("Enter updated student password: ")
        students[student_id]['name'] = new_name
        students[student_id]['course'] = new_course
        students[student_id]['school'] = new_school
        students[student_id]['password'] = new_password

        save_students() 

        print("Student updated successfully!")
        print("")
    else:
        print("Student not found.")
        print("")
def delete_student():
    student_id = input("Enter student ID to delete: ")
    if student_id in students:
        del students[student_id]

        # Save the updated student information to file
        save_students()

        # Delete the student entry from the students.txt file
        with open('students.txt', 'r') as file:
            lines = file.readlines()
        with open('students.txt', 'w') as file:
            for line in lines:
                if not line.startswith(student_id + ','):
                    file.write(line)

        # Also, delete the student files
        delete_student_files(student_id)

        print("Student deleted successfully!")
        print("")
    else:
        print("Student not found.")
        print("")

#Manage Student Timetable
def manage_timetables():
    student_id = input("Enter the student ID: ")

    # Check if student ID is valid
    if check_student_valid(student_id):
        while True:
            print("[1] Create Timetable")
            print("[2] Update Timetable")
            print("[3] Delete Timetable")
            print("[4] Back to Admin Menu")
            choice = input("Enter your choice: ")
            print("")

            if choice == "1":
                create_timetables(student_id)
            elif choice == "2":
                update_timetable(student_id)
            elif choice == "3":
                delete_timetable_entry(student_id)
            elif choice == "4":
                break
            else:
                print("Invalid choice. Please try again.")
                print("")

    else:
        print("Invalid student ID.")
        print("")

#Manage Student Assignment
def manage_assignments():
    while True:
        print("[1] Delete Assignment Submission")
        print("[2] Mark Student Assignment")
        print("[3] Back to Admin Menu")
        admin_selection = input("Please select an option: ")
        print("")

        if admin_selection == "1":
            delete_assignment_submission()
        elif admin_selection == "2":
            mark_student_assignment()
        elif admin_selection == "3":
            return
        else:
            print("Invalid Selection!!")
            print("")
def delete_assignment_submission():
    student_id = input("Enter student ID: ")
    student_name = check_student_valid(student_id)
    if student_name:
        assignments_file = f'assignments_{student_id}.txt'
        if os.path.exists(assignments_file):
            print(f"Assignments submitted by {student_name}:")
            with open(assignments_file, 'r') as file:
                assignments = file.readlines()
                assignment_counter = 1
                for assignment in assignments:
                    print(f"{assignment_counter}. {assignment.strip()}")
                    assignment_counter += 1
            assignment_to_delete = int(input("Enter the number of the assignment to delete: "))
            if 1 <= assignment_to_delete <= len(assignments):
                del assignments[assignment_to_delete - 1]
                with open(assignments_file, 'w') as file:
                    file.writelines(assignments)
                print("Assignment deleted successfully.")
                print("")
            else:
                print("Invalid assignment number.")
                print("")
        else:
            print("No assignments found for this student.")
            print("")
    else:
        print("Invalid student ID.")
        print("")
def mark_student_assignment():
    student_id = input("Enter student ID: ")
    student_name = check_student_valid(student_id)
    if student_name:
        assignments_file = f'assignments_{student_id}.txt'
        if os.path.exists(assignments_file):
            print(f"Assignments submitted by {student_name}:")
            with open(assignments_file, 'r') as file:
                assignments = file.readlines()
                assignment_counter = 1
                for assignment in assignments:
                    print(f"{assignment_counter}. {assignment.strip()}")
                    assignment_counter += 1
            assignment_to_mark = int(input("Enter the number of the assignment to mark: "))
            if 1 <= assignment_to_mark <= len(assignments):
                mark = input("Enter the mark for the assignment: ")
                assignments[assignment_to_mark - 1] = assignments[assignment_to_mark - 1].strip() + f", {mark}\n"
                with open(assignments_file, 'w') as file:
                    file.writelines(assignments)
                print("Assignment marked successfully.")
                print("")
            else:
                print("Invalid assignment number.")
                print("")
        else:
            print("No assignments found for this student.")
            print("")
    else:
        print("Invalid student ID.")
        print("")

#Program Main Function
def main():
    load_students()
    print("Please choose to login as a student or admin.")
    print("[1] Student")
    print("[2] Admin")
    print("")
    user_type = input("Enter your choice: ")
    print("")

    if user_type == "1":
        student_login()
    elif user_type == "2":
        admin_login()
    else:
        print("Invalid Selection!!")
        exit()

main()

