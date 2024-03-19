import bcrypt
from datetime import datetime
from email_validator import validate_email

def password_validator(current_account, status=1):
    from account import Load_Menu
    if status == "change":
        value = " нова "
    else:
        value = " "
    while True:
        password_check = input(f"Въведете{value}парола: ")
        if password_check == "":
            return Load_Menu(current_account)
        nums = False
        uppers = False
        lowers = False
        space = False
        
        for x in password_check:
            if x.isnumeric():
                nums = True
            elif x.islower():
                lowers = True
            elif x.isupper():
                uppers = True
            elif chr(32) == x:
                space = True

        if (nums == False or uppers == False or lowers == False) or space == True:
            print("-\n* Паролата трябва да съдържа главни и малки букви на латиница, цифри и дължина от най-малко от 8 знака!\n-")
            continue
        else:
            hashed_password = bcrypt.hashpw(password_check.encode('utf-8'), bcrypt.gensalt())
            return hashed_password, password_check
        
def date_validation(operation):
    value = {"change":"дата на информацията за промяна ", "new_date": "нова дата за промяна ", "search": "дата", "delete":"дата за изтриване"}
    while True:
        date_input = input(f"Въведете {value[operation]}във формат YYYY-MM-DD: ")
        date_format = '%Y-%m-%d'
        try:
            datetime.strptime(date_input, date_format)
            return date_input
        except ValueError as e:
            print(f"Грешен формат: {e}\n-")
            input("Натиснете 'enter', за да продължите...")
            continue

def sum_validate(operation=1):
    value = {"delete":"сума за изтриване","change":"сума от информацията за промяна", "new_sum":"нова сума",1:"сума"}
    
    while True:
        try:
            input_sum = float(input(f"Въведете {value[operation]} (в лева): "))
            if input_sum <= 0:
                print("* Невалидна сума!")
                continue
            else:
                return float(input_sum)
           
        except:
            print("* Невалидна сума!")
            continue

def email_validate(current_account):
    from account import Load_Menu
    while True:
        email_check = input("Въведете email: ")
        if email_check == "":
            return Load_Menu(current_account)
        try:
            validate_email(email_check, check_deliverability=False)
            return email_check
        except:
            print("-\nНевалиден email!\n-")
            continue

def days_validate():
     while True:
        try:
            input_days= int(input(f"Въведете брой дни: "))
            if input_days <= 0:
                print("* Невалидна заявка!")
                continue
            else:
                return int(input_days)
           
        except:
            print("* Невалидна заявка!")
            continue

