# ==== Importing Libraries ====

from datetime import datetime, date
import os.path

# ==== User-Defined Functions ====

# registers a new user
def reg_user():
    # only admin can access
    if username_current != "admin":
        print("Only username 'admin' can register new users.")
        return
    # ask for new username and password, and to confirm
    username_new = input("New username : ")
    for name in username_log:
        while username_new == name:
            username_new = input("Username already exists. Please enter a different username : ")
    password_new = input("New password : ")
    password_new_confirm = input("Confirm new password : ")

    # as long as password and its confirmation do not match, let user know and ask again
    while password_new_confirm != password_new:
        print("\nPassword confirmation did not match password. Please try again.\n")
        password_new = input("New password : ")
        password_new_confirm = input("Confirm new password : ")
        
    # prepare string to be appended to user.txt, then append to file
    # \n used so new string is entered on new line in file
    user_new = f"\n{username_new}, {password_new}"
    with open("user.txt","a") as add_user:
        add_user.write(user_new)
    print("\nNew user registered.")

# adds a new task
def add_task():
    # ask for details
    task_user = input("Username of person task will be assigned to : ")
    while not(task_user in username_log):
        task_user = input("\nUsername not currently registered. Please try again.\n"
                          "Enter the username of person this task will be assigned to : ")
    task_title = input("Task title : ")
    task_desc = input("Task description: ")
    # looked up how to get current date in desired format and referred to the following webpage:
    # https://www.geeksforgeeks.org/python-strftime-function/
    task_date_assigned = datetime.now().strftime("%d %b %Y")
    task_date_due = input("Due date (e.g. 01 Jan 1900) : ")
    task_completion = "No"
    task_new = f"\n{task_user}@@, {task_title}@@, {task_desc}@@, {task_date_assigned}@@, {task_date_due}@@, {task_completion}"
    # append new task info to task file
    with open("tasks.txt","a") as tasks:
        tasks.write(task_new)
    print("\nTask logged.")

# prints all tasks
def view_all():
    with open("tasks.txt","r") as task_file:
        for task in task_file:
            # strip new line escape characters and split items in each line of the tasks file
            task = task.strip("\n").split("@@, ")
            # print items using indexing
            print(f"Task :\t\t\t{task[1]}")
            print(f"Assigned to :\t\t{task[0]}")
            print(f"Date assigned : \t{task[3]}")
            print(f"Due date :\t\t{task[4]}")
            print(f"Task complete?\t\t{task[5]}")
            print(f"Task description :\n  {task[2]}\n")
    print("All tasks listed above.")

# prints all tasks assigned to user currently logged in
def view_mine():
    task_user = open("tasks.txt","r")
    # create a list from the file for manipulation, where each list item is a line from the file
    tasks_existing = list(task_user)
    task_user.close()

    # set initial 'view mine' task number to 0
    vm_no = 0
    # create variable to keep track of index of line in file
    va_no = -1
    # create dictionary with vm task number as key, and va task index as value
    vm_va_ref = {}
    # variable to store tasks which will be used to write over existing task file
    tasks_new = []

    # loop to extract task information
    for line in tasks_existing:
        va_no += 1
        # strip new line escape characters and split items in each line of the tasks file
        line = line.strip("\n").split("@@, ")
        # run loop below only if the username used matches the item containing the username in 
        # the task
        if line[0] == username_current:
            # increase count indicating task number and append line to the new task file list
            vm_no += 1
            print(f"Task #{vm_no}")
            print(f"Task :\t\t\t{line[1]}")
            print(f"Date assigned : \t{line[3]}")
            print(f"Due date :\t\t{line[4]}")
            print(f"Task complete?\t\t{line[5]}")
            print(f"Task description :\n  {line[2]}\n")
            vm_va_ref[vm_no] = va_no
            tasks_new.append(line)
        else:
            # append line to the new task file list even if task not assigned to username 
            # because it will be new task file containing all tasks
            tasks_new.append(line)

    # ask for task number or exit
    chosen_vm = int(input(f"All tasks assigned to {username_current} listed above.\n"
                          "Enter a task number to modify that task, or -1 to return to "
                          "the main menu : "))

    while True:        
        # exit function if input is -1
        if chosen_vm == -1:
            return

        # if user input is outside of the range of task numbers or not -1
        elif not(chosen_vm in range(1,vm_no+1) or chosen_vm == -1):
            chosen_vm = int(input(f"\nTask number not recognised. Please try again.\n"
                                  "Enter a task number to go directly to that task, or -1 "
                                  "to return to the main menu : "))

        # if task number is valid and selected task is complete
        elif (tasks_new[vm_va_ref[chosen_vm]][5] == "Yes") and (chosen_vm in range(1, vm_no+1)):
                    print("\nThis task is marked as complete; changes to this task cannot be made.")
                    chosen_vm = int(input(f"\nEnter a different task number to modify that task, "
                                          "or -1 to return to the main menu : "))
        
        else:
            break

    # if user input is a valid task number, present modification options
    if chosen_vm in range(1, vm_no+1):
            complete_or_edit = input("\nWould you like to mark the task as complete (C), "
                                     "or edit the task (E)? ")
    if complete_or_edit.lower() == "c":
        tasks_new[vm_va_ref[chosen_vm]][5] = "Yes"
        print("\nThe task is now marked as complete.")

    # present edit options
    elif complete_or_edit.lower() == "e":
        edit_task = input('''\nWhat would you like to do?
1. Change the username of the person to whom the task is assigned to
2. Change the due date of the task
Enter 1 or 2 : ''')
        # where input is not recognised 
        while edit_task != "1" and edit_task != "2":
            edit_task = input('''\nInput not recognised. Please try again.
1. Change the username of the person to whom the task is assigned to
2. Change the due date of the task
Enter 1 or 2 : ''')
        print("")
        # assign new username to task segment
        if edit_task == "1":
            new_task_user = input("Enter username which will be assigned to this task : ")
            # if user tries to assign task to username which is not registered
            while not(new_task_user in username_log):
                new_task_user = input("\nUsername not currently registered. Please try again."
                                      "\nEnter username which will be assigned to this task : ")
            tasks_new[vm_va_ref[chosen_vm]][0] = new_task_user
            print(f"\nTask now assigned to {tasks_new[vm_va_ref[chosen_vm]][0]}.")
        # assign new new date segment
        else:
            tasks_new[vm_va_ref[chosen_vm]][4] = input("Enter new due date : ")
            print("\nDue date changed.")

    # overwrite existing tasks file with new task info
    task_user = open("tasks.txt","w")
    for line in tasks_new:
        line = ", ".join(line) + "\n"
        task_user.write(line)
    task_user.close()

# generates reports of tasks and users
def reports():
    # task overview file
    task_all = open("tasks.txt", "r")
    # create a list of the file for use in user overview section
    task_all_list = list(task_all)
    task_all.close()
    task_total = 0
    task_completed = 0
    task_overdue = 0
    # loop through for each task
    for task in task_all_list:
        task = task.strip("\n").split("@@, ")
        task_total += 1
        # if task is completed, add to the completion counter
        if task[5] == "Yes":
            task_completed += 1
        # check if the current date is greater / later than the due date of the task
        # convert due date in task file to the right format so the two dates can be compared
        # converting date string into datetime:
        # https://stackoverflow.com/questions/31796798/python-convert-month-name-to-integer
        # https://datagy.io/python-string-to-date/
        # converting datetime to date data type:
        # https://www.geeksforgeeks.org/how-to-convert-datetime-to-date-in-python/
        elif date.today() > datetime.strptime(task[4], "%d %b %Y").date():
            task_overdue += 1
    # write information to output file task_overview.txt
    task_overview = open("task_overview.txt", "w")
    task_overview.write(f'''Total number of tasks recorded\t\t\t:\t{task_total}
Total number of completed tasks\t\t\t:\t{task_completed}
Total number of uncompleted tasks\t\t:\t{task_total - task_completed}
Total number of uncompleted, overdue tasks\t:\t{task_overdue}
Perentage of tasks which are incomplete\t\t:\t{round((task_total - task_completed) / task_total * 100, 2)}%
Percentage of all tasks which are overdue\t:\t{round(task_overdue / task_total * 100, 2)}%''')
    task_overview.close()

    # user overview file
    user_overview = open("user_overview.txt", "w")
    user_overview.write(f"Total number of registered users\t\t:\t{len(username_log)}\n"
                        "Total number of tasks recorded\t\t\t:\t{task_total}\n")
    # run loop for each user
    for user in username_log:
        # variables to keep track of counts
        user_task_total = 0
        user_task_incomplete = 0
        user_task_overdue = 0
        # run loop for each task
        for task in task_all_list:
            task = task.strip("\n").split("@@, ")
            # if username in task matches user, add to user total
            if task[0] == user:
                user_task_total += 1
                # if the task is not completed, add to incomplete counter
                if task[5] == "No":
                    user_task_incomplete += 1
                    # if task is overdue, add to overdue counter; see task overview section above for explanation of code
                    if date.today() > datetime.strptime(task[4], "%d %b %Y").date():
                        user_task_overdue += 1
        # write information to output file user.txt if user has tasks
        if user_task_total != 0:
            user_overview.write(f'''\n{user}
Assigned tasks\t\t\t\t\t:\t{user_task_total}
Percentage of all tasks assigned to user\t:\t{round(user_task_total / task_total * 100, 2)}%
Percentage of user tasks completed\t\t:\t{round((user_task_total - user_task_incomplete) / user_task_total * 100, 2)}%
Percentage of user tasks to be completed\t:\t{round(user_task_incomplete / user_task_total * 100, 2)}%
Percentage of overdue user tasks\t\t:\t{round(user_task_overdue / user_task_total * 100, 2)}%
''')
        else:
            # write the following to output file user.txt for users with no tasks
            user_overview.write(f"\nThere are currently no tasks assigned to {user}.\n")
    user_overview.close()
    print("Task overview and user overview reports have been generated.")

# prints an overview of all tasks and users based on the report generated
# information printed will not be up-to-date if user did not generate reports after any updates
def stats():
    # generate reports if they do not exist
    # https://www.pythontutorial.net/python-basics/python-check-if-file-exists/
    if not(os.path.exists("user_overview.txt")) or not(os.path.exists("task_overview.txt")):
        reports()
    
    print("Task Overview\n")
    # read and print lines from task_overview.txt
    task_overview = open("task_overview.txt", "r")
    for task_o in task_overview:
        task_o = task_o.strip("\n")
        print(task_o)
    task_overview.close()
    
    print("\nUser Overview\n")
    # read and print lines from user_overview.txt
    user_overview = open("user_overview.txt", "r")
    for user_o in user_overview:
        user_o = user_o.strip("\n")
        print(user_o)
    user_overview.close()
    print("\nTask and user statistics are displayed above.")


# ==== Login Section ====

# open and read user.txt while houses all login details
with open("user.txt", "r") as login_file:
    # create empty list to store login info
    login_info = []

    # for each line in the file
    for set in login_file:
        # eliminate spaces in the line and split the string by commas, resulting in username 
        # and password as separate items
        set = set.replace(" ", "").split(",")
        # add items to login_info
        login_info += set
    
    # strip new line escape characters from individual items in login_info
    for each in range(len(login_info)):
            login_info[each] = login_info[each].strip("\n")

# create empty lists to store usernames and passwords separately
username_log = []
password_log = []

# add even-number index items from login_info to username_log, and odd-numbered index items 
# to password_log
for i in range(len(login_info)):
    if i % 2 == 0:
        username_log.append(login_info[i])
    else:
        password_log.append(login_info[i])

# ask for username and password
username_current = input("Input username : ")
password_input = input("Input password : ")

# variable checking if correct credentials have been entered
credential_check = False
while credential_check == False:
    # repeat loop for each item in username_log
    for username_entry in username_log:
        # if item and username input match
        if username_entry == username_current:
            # log index of the item as username_index
            username_index = login_info.index(username_current)
            # if password input matches the item directly after the username item indexed 
            if password_input == login_info[username_index+1]:
                credential_check = True
    
    # if inputs do not satisfy the lines above
    if credential_check == False:
        # ask user to re-enter credentials
        print("\nCredentials incorrect. Please try again.\n")
        username_current = input("Input username : ")
        password_input = input("Input password : ")

print("\nCredentials accepted.")

# ==== Menu Section ====

while True:
    # presenting the menu to the user and 
    # making sure that the user input is coneverted to lower case
    # edited menu below from template to make neater
    menu = input('''\nSelect one of the following options below:
r\t-\tRegistering a user
a\t-\tAdding a task
va\t-\tView all tasks
vm\t-\tView my task
gr\t-\tGenerate reports
ds\t-\tDisplay statistics
e\t-\tExit
:''').lower()
    print("")

# ==== Register New User Section ====

    if menu == 'r':
        print("You would like to register a new user.\n")
        reg_user()

    elif menu == 'a':
        print("You would like to add a new task.\n")
        add_task()

    elif menu == 'va':
        view_all()

    elif menu == 'vm':
        view_mine()

    elif menu == 'gr':
        reports()

    elif menu == 'ds':
        stats()

    elif menu == 'e':
        print("Program terminated.\n")
        exit()

    else:
        print("Input not recognised; please try again. ")