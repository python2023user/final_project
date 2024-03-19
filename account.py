import os
import time
from sqlalchemy.exc import IntegrityError
from diagram import Load_diagram
from datetime import datetime
from account_functions import month, sign_date, sign_return, sign_exsum
import bcrypt
from sqlalchemy import Column, Date, Float, ForeignKey, Integer, String, create_engine, func
from sqlalchemy.orm import declarative_base, relationship, sessionmaker
from validate_functions import sum_validate, date_validation, email_validate, password_validator, days_validate
from datetime import date, timedelta
import numpy as np

##############################################################################
# Create database => Start
##############################################################################
#

engine = create_engine('sqlite:///accounts.db', echo=False, query_cache_size=0)
Base = declarative_base()
Base.metadata.bind = engine
Session = sessionmaker(bind=engine)
session = Session()

class Account(Base):
    __tablename__ = 'accounts'
    id = Column(Integer, primary_key=True)
    email = Column(String, unique=True)
    name = Column(String)
    password = Column(String)
    expenses = relationship("Expense", back_populates="account")
    incomes = relationship("Income", back_populates="account")
    def __repr__(self):
        return f"<Account(email='{self.email}',name='{self.name}', password='{self.password}')>"

class Expense(Base):
    __tablename__ = 'expenses'
    id = Column(Integer, primary_key=True)
    sum_expense = Column(Float)
    date_expense = Column(Date)
    desc_expense = Column(String)
    account_email = Column(String, ForeignKey('accounts.email'))
    account = relationship("Account", back_populates="expenses")

    def __repr__(self):
        return f"<Expense(sum_expense={self.sum_expense}, date_expense='{self.date_expense}', desc_expense='{self.desc_expense}', account_email='{self.account_email}')>"

class Income(Base):
    __tablename__ = 'incomes'
    id = Column(Integer, primary_key=True)
    sum_income = Column(Float)
    date_income = Column(Date)
    desc_income = Column(String)
    account_email = Column(String, ForeignKey('accounts.email'))
    account = relationship("Account", back_populates="incomes")

    def __repr__(self):
        return f"<Income(sum_income={self.sum_income}, date_income='{self.date_income}', desc_income='{self.desc_income}', account_email='{self.account_email}')>"

Base.metadata.create_all(engine)

#
##############################################################################
# Create database => End
##############################################################################
# Account create => Start
##############################################################################
#
        
def create_account(email_input, name_input, password_input, password_normal_input):
    existing_account = session.query(Account).filter(func.lower(Account.email) == email_input.lower()).first()
    if existing_account:
        print(f"Потребителското име {email_input} е заето. Моля, изберете друго.")
        input("-\nНатиснете 'enter', за да продължите...")
        return account_request()
    new_account = Account(email=email_input, password=password_input, name=name_input)
    session.add(new_account)
    session.commit()
    print(f"Създадохте нов акаунт с email '{email_input}', име '{name_input}' и парола {password_normal_input}.")
    input("-\nНатиснете 'enter', за да продължите...")
    return new_account
#
def account_request(current_account):
    from validate_functions import password_validator
    os.system('cls' if os.name == 'nt' else 'clear')
    print("##############################\n# Създаване на акаунт\n# Натиснете 'enter' за отказ\n##############################\n-")
    email_input = email_validate(current_account)
    password_input, password_normal_input = password_validator(current_account)
    name_input = input("Въведете име: ")
    if name_input == "":
        return Load_Menu(current_account)
    return create_account(email_input.strip(), name_input.strip(), password_input.strip(), password_normal_input)

#
##############################################################################
# Account create => End
##############################################################################
# Account login => Start
##############################################################################
#

def log_in(email_input, password_input):
    account = session.query(Account).filter(func.lower(Account.email) == email_input.lower()).first()
    if account and bcrypt.checkpw(password_input.encode('utf-8'), account.password):
        os.system('cls')
        print(f"Успешно влизане като '{account.email}'.")
        time.sleep(1.5)
        return account
    else:
        print(f"-\n* Невалидно потребителско име или парола!")
        time.sleep(1.5)
        return login_request(current_account)
    
#
    
def login_request(current_account):
    os.system('cls' if os.name == 'nt' else 'clear')
    print("##############################\n# Влизане в акаунт\n# Натиснете 'enter' за отказ\n##############################\n-")
    email_input = input("Въведете email: ")
    if email_input == "":
        return Load_Menu(current_account)
    password_input = input("Въведете парола: ")
    if password_input == "":
        return Load_Menu(current_account)
    else:
        return log_in(email_input.strip(), password_input.strip())
    
#
##############################################################################
# Account login => End
##############################################################################
# Menus => Start
##############################################################################
#

current_account = None
def Load_Menu(current_account):
    if current_account:
        os.system('cls' if os.name == 'nt' else 'clear')
        print(f"############################################################\n# Главно меню | Акаунт: {current_account.name} ({current_account.email})\n############################################################\n-")
        print(f"1 - Добавяне на приход\n2 - Добавяне на разход\n3 - Показване на данни\n4 - Промяна на данни\n5 - Изход от акаунта\n6 - Изход от програмата\n-")
        value = input("Избор: ")
        if value == "1":
            add_income(current_account)
        elif value == "2":
            add_expense(current_account)
        elif value == "3":
            show_data_menu(current_account)
        elif value == "4":
            update_menu(current_account)
        elif value == "5":
            print(f"Излизане от акаунт {current_account.email}")
            current_account = None
            os.system('cls')
            Load_Menu(current_account)
        elif value == "6":
            time.sleep(0.5)
            session.close()
            os.system('cls' if os.name == 'nt' else 'clear')
            print("Излизане от програмата...")
            exit()
    else:
        os.system('cls' if os.name == 'nt' else 'clear')
        print("##############################\n-\n1 - Създаване на акаунт\n2 - Влизане в акаунт\n3 - Край на програмата\n-")
        value = input("Избор: ")
        if value == "1":
            current_account = account_request(current_account)
            return Load_Menu(current_account)
        elif value == "2":
            current_account = login_request(current_account)
            return Load_Menu(current_account)
        elif value == "3":
            os.system('cls' if os.name == 'nt' else 'clear')
            session.close()
            print("Излизане от програмата...")
            exit()
        else:
            Load_Menu(current_account)

def update_menu(current_account):
    os.system('cls' if os.name == 'nt' else 'clear')
    print(f"##############################\n# Промяна\n-\n1 - Промяна на данни за приходи\n2 - Промяна на данни за разходи\n3 - Промяна на парола\n4 - Назад\n-")
    value = input("Избор: ")
    if value == "1":
        change_incomes(current_account)
    elif value == "2":
        change_expenses(current_account)
    elif value == "3":
        change_password(current_account)
    elif value == "4":
        Load_Menu(current_account)
#

def show_data_menu(account):
    os.system('cls' if os.name == 'nt' else 'clear')
    print("##############################\n# Преглед\n##############################\n-")
    print("1 - Баланс\n2 - Преглед на приходите\n3 - Преглед на разходите\n4 - Диаграма\n5 - Връщане към главното меню\n-")
    value = input("Избор: ")
    if value == "1":
        show_balans(account)
    if value == "2":
        show_income(account)
    if value == "3":
        show_expense(account)
    if value == "4":
        exp = get_expense(account)
        inc = get_income(account)
        Load_diagram(exp, inc, month)
    if value == "5":
        Load_Menu(account)
    else:
        show_data_menu(account)

#
##############################################################################
# Menus => End
##############################################################################
# Update => Start
##############################################################################
#
        
def change_expenses(current_account):
    # from account import session, Expense, delete_func, update_menu
    os.system('cls' if os.name == 'nt' else 'clear')
    print("##############################\n# Промяна на разходи\n-\n1 - Промяна на дата\n2 - Промяна на сума\n3 - Промяна на описание\n4 - Изтриване\n5 - Назад\n-")
    value = input("Избор: ")
    if value == "1":
        try:
            date_detect = date_validation('change')
            sum_detect = sum_validate("change")
            desc_detect = input("Въведете описанието на информацията за промяна: ")
            new_value = date_validation('new_date')
            expense = session.query(Expense).filter_by(desc_expense=desc_detect, date_expense=date_detect, sum_expense=sum_detect, account_email=current_account.email).first()
            if expense:
                expense.date_expense = datetime.strptime(new_value, '%Y-%m-%d')
                session.commit()
                print(f"Успешно променена дата от {date_detect} на {new_value}")
            else:
                print("Не е намерен разход с тези параметри.")
        except Exception as e:
            session.rollback()
            print(f"Възникна грешка: {e}")
        finally:
            input("-\nНатиснете 'enter' за връщане назад...")
            change_expenses(current_account)

    elif value == "2":
        try:
            date_detect = date_validation('change')
            sum_detect = sum_validate("change")
            desc_detect = input("Въведете описанието на информацията за промяна: ")
            new_value = sum_validate("new_sum")
            expense = session.query(Expense).filter_by(desc_expense=desc_detect, date_expense=date_detect, \
                                sum_expense=sum_detect, account_email=current_account.email).first()
            if expense:
                expense.sum_expense = new_value
                session.commit()
                print(f"Успешно променена сума от {sum_detect:.2f} лв. на {new_value:.2f} лв.")
            else:
                print("Не е намерен разход с тези параметри.")
        except Exception as e:
            session.rollback()
            print(f"Възникна грешка: {e}")
        finally:
            input("Натиснете 'enter' за връщане назад...")
            change_expenses(current_account)

    elif value == "3":
        try:
            date_detect = date_validation('change')
            sum_detect = sum_validate("change")
            desc_detect = input("Въведете описанието на информацията за промяна: ")
            new_value = input("Въведете ново описание: ")
            expense = session.query(Expense).filter_by(desc_expense=desc_detect, date_expense=date_detect, \
                                sum_expense=sum_detect, account_email=current_account.email).first()
            if expense:
                expense.desc_expense = new_value
                session.commit()
                print(f"Успешно променео описание от {desc_detect} на {new_value}")
            else:
                print("Не е намерен разход с тези параметри.")
        except Exception as e:
            session.rollback()
            print(f"Възникна грешка: {e}")

        finally:
            input("Натиснете 'enter' за връщане назад...")
            change_expenses(current_account)

    elif value == "4":
        os.system('cls' if os.name == 'nt' else 'clear')
        print("##############################\n# Изтриване на разходи\n-\n1 - Изтриване по дата\n2 - Изтриване по сума\n3 - Изтриване по описание\n4 - Назад\n-")
        action = input("Избор: ")
        if action == "1":
            select_value = date_validation("delete")
            delete_expenses = session.query(Expense).filter_by(date_expense=select_value,account_email=current_account.email).all()
            delete_func(delete_expenses, current_account)
        elif action == "2":
            select_value = sum_validate("delete")
            delete_expenses = session.query(Expense).filter_by(sum_expense=select_value,account_email=current_account.email).all()
            delete_func(delete_expenses, current_account)
        elif action == "3":
            select_value = input("Въведете описание: ")
            delete_expenses = session.query(Expense).filter_by(desc_expense=select_value,account_email=current_account.email).all()
            delete_func(delete_expenses, current_account)
        elif action == "4":
            change_expenses(current_account)
    elif value == "5":
        update_menu(current_account)        

#

def change_incomes(current_account):  
    os.system('cls' if os.name == 'nt' else 'clear')
    print("##############################\n# Промяна на приходи\n-\n1 - Промяна на дата\n2 - Промяна на сума\n3 - Промяна на описание\n4 - Изтриване\n5 - Назад\n-")
    value = input("Избор: ")
    if value == "1":
        try:
            date_detect = date_validation('change')
            sum_detect = sum_validate("change")
            desc_detect = input("Въведете описанието на информацията за изтриване: ")
            new_value = date_validation('new_date')
            income = session.query(Income).filter_by(desc_income=desc_detect, date_income=date_detect, sum_income=sum_detect, account_email=current_account.email).first()
            if income:
                income.date_income = datetime.strptime(new_value, '%Y-%m-%d')
                session.commit()
                print(f"Успешно променена дата от {date_detect} на {new_value}")
            else:
                print("Не е намерен приход с тези параметри.")
                
        except Exception as e:
            session.rollback()
            print(f"Възникна грешка: {e}")
            
        finally:
            input("-\nНатиснете 'enter' за връщане назад...")
            change_incomes(current_account)
    
    elif value == "2":
        try:
            date_detect = date_validation('change')
            sum_detect = sum_validate("change")
            desc_detect = input("Въведете описанието на информацията за промяна: ")
            new_value = sum_validate("new_sum")
            income = session.query(Income).filter_by(desc_income=desc_detect, date_income=date_detect, sum_income=sum_detect, account_email=current_account.email).first()
            if income:
                income.sum_income = new_value
                session.commit()
                print(f"Успешно променена сума от {sum_detect:.2f} лв. на {new_value:.2f} лв.")
            else:
                print("Не е намерен приход с тези параметри.")

        except Exception as e:
            session.rollback()
            print(f"Възникна грешка: {e}")
            
        finally:
            input("-\nНатиснете 'enter' за връщане назад...")
            change_incomes(current_account)

    elif value == "3":
        try:
            date_detect = date_validation('change')
            sum_detect = sum_validate("change")
            desc_detect = input("Въведете описанието на информацията за промяна: ")
            new_value = input("Въведете ново описание: ")
            income = session.query(Income).filter_by(desc_income=desc_detect, date_income=date_detect, sum_income=sum_detect, account_email=current_account.email).first()
            if income:
                income.desc_income = new_value
                session.commit()
                print(f"Успешно променео описание от {desc_detect} на {new_value}")
            else:
                print("Не е намерен приход с тези параметри.")
        except Exception as e:
            session.rollback()
            print(f"Възникна грешка: {e}")
            
        finally:
            input("-\nНатиснете 'enter' за връщане назад...")
            change_incomes(current_account)

    elif value == "4":
        os.system('cls' if os.name == 'nt' else 'clear')
        print("##############################\n# Изтриване на приходи\n-\n1 - Изтриване по дата\n2 - Изтриване по сума\n3 - Изтриване по описание\n4 - Назад\n-")
        action = input("Избор: ")
        if action == "1":
            select_value = date_validation("delete")
            delete_incomes = session.query(Income).filter_by(date_income=select_value,account_email=current_account.email).all()
            print(delete_incomes)
            delete_func(delete_incomes, current_account)
        elif action == "2":
            select_value = sum_validate("delete")
            delete_incomes = session.query(Income).filter_by(sum_income=select_value,account_email=current_account.email).all()
            delete_func(delete_incomes, current_account)
        elif action == "3":
            select_value = input("Въведете описание: ")
            delete_incomes = session.query(Income).filter_by(desc_income=select_value,account_email=current_account.email).all()
            delete_func(delete_incomes, current_account)
        elif action == "4":
            change_incomes(current_account)
    elif value == "5":
        update_menu(current_account)

#

def change_password(current_account):
    from account import session, Load_Menu, update_menu
    os.system('cls' if os.name == 'nt' else 'clear')
    print("##############################\n# Промяна на парола\n-")
    new_password, normal_password = password_validator(current_account, "change")
    current_account.password = new_password
    try:
        session.commit()
        print(f"-\n* Паролата е успоешно променена на '{normal_password}'")
    except:
        print("Грешка в промяната на паролата!")
    finally:
        input("-\nНатиснете 'enter' за връщане назад...")
        update_menu(current_account)

#
##############################################################################
# Update => End
##############################################################################
# Show incomes => Start
##############################################################################
#

def show_expense(u_account):
    os.system('cls' if os.name == 'nt' else 'clear')
    print("##############################\n# Разходи\n##############################\n-\n1 - Преглед по дата\n2 - Преглед по сума\n\
3 - Преглед по описание\n4 - Преглед на всички разходи\n5 - Показване на разходи за определени дни назад\n6 - Назад\n")
    value = input("Избор: ")

    if value == "1":
        ex_date = date_validation("search")
        if ex_date == "":
            show_expense(u_account)
        sign = sign_date(ex_date)
        os.system('cls')
        if sign == ">":
            show_expense_by_date = session.query(Expense).join(Account).filter(Account.email == u_account.email, \
                                Expense.date_expense > ex_date).order_by(Expense.date_expense).all()
        if sign == "<":
            show_expense_by_date = session.query(Expense).join(Account).filter(Account.email == u_account.email, \
                                Expense.date_expense < ex_date).order_by(Expense.date_expense).all()
        if sign == "==":
            show_expense_by_date = session.query(Expense).join(Account).filter(Account.email == u_account.email, \
                                Expense.date_expense == ex_date).order_by(Expense.date_expense).all()
        print(f"Показване на разходите {sign_return(sign)} {ex_date} | ({u_account.email})\n-")
        for expense_result in show_expense_by_date:
            print(f"{expense_result.sum_expense:.2f} лв. | дата: {expense_result.date_expense} | описание: {expense_result.desc_expense} ")
        if show_expense_by_date == []:
            print("Няма резултати!")
        input("-\nНатиснете 'enter' за връщане към менюто...")
        os.system('cls')
        show_expense(u_account)

    elif value == "2":
        ex_sum = sum_validate()
        sign = sign_exsum(ex_sum)
        if sign == "":
            show_expense(u_account)
        os.system('cls')
        print(f"Показване на разходите за резултат {sign} {ex_sum:.2f} | ({u_account.email})\n-")
        if sign == ">":
            show_expense_by_sum = session.query(Expense).join(Account).filter(Account.email == u_account.email, \
                                Expense.sum_expense > ex_sum).order_by(Expense.sum_expense).all()
        if sign == "<":
            show_expense_by_sum = session.query(Expense).join(Account).filter(Account.email == u_account.email, \
                                Expense.sum_expense < ex_sum).order_by(Expense.sum_expense).all()
        if sign == "==":
            show_expense_by_sum = session.query(Expense).join(Account).filter(Account.email == u_account.email, \
                                Expense.sum_expense == ex_sum).order_by(Expense.sum_expense).all()
        for expense_result in show_expense_by_sum:
            print(f"{expense_result.sum_expense:.2f} лв. | дата: {expense_result.date_expense} | описание: {expense_result.desc_expense} ")
        if show_expense_by_sum == []:
            print("Няма резултати!")
        input("-\nНатиснете 'enter' за връщане към менюто...")
        os.system('cls')
        show_expense(u_account)
    
    elif value == "3":
        ex_desc = input("Въведете описание за разход: ") + "%"
        if ex_desc == "":
            show_expense(u_account)
        os.system('cls')
        print(f"Показване на разходите за '{ex_desc.replace("%","...")}' | ({u_account.email})")
        show_expense_by_desc = session.query(Expense).join(Account).filter(Account.email == u_account.email, \
                            Expense.desc_expense.like(ex_desc)).order_by(Expense.date_expense).all()
        for expense_result in show_expense_by_desc:
            print(f"{expense_result.sum_expense:.2f} лв. | дата: {expense_result.date_expense} | описание: {expense_result.desc_expense} ")
        if show_expense_by_desc == []:
            print("Няма резултати!\n-")
        input("Натиснете 'enter' за връщане към менюто...")
        os.system('cls')
        show_expense(u_account)
    
    elif value == "4":
        os.system('cls')
        print(f"Показване на списък с всички разходи | ({u_account.email})\n-")
        for expens in u_account.expenses:
            print(f"{expens.sum_expense:.2f} лв. | дата: {expens.date_expense} | описание: {expens.desc_expense}")
        if u_account.expenses == []:
            print("Няма резултати!")
        input("-\nНатиснете 'enter' за връщане към менюто...")
        os.system('cls')

    elif value == "5":
        old_days = days_validate()
        old_days_ = date.today() - timedelta(days=old_days)
        os.system('cls')
        print(f"Показване на списък с разходи за за {old_days} {'дни' if old_days > 1 else 'ден'} назад | ({u_account.email})\n-")
        older_data = session.query(Expense).join(Account).filter(Account.email == u_account.email, \
                            Expense.date_expense >= old_days_).order_by(Expense.date_expense).all()
        for data in older_data:
            print(f"{data.sum_expense:.2f} лв. | дата: {data.date_expense} | описание: {data.desc_expense}")
        if older_data == []:
            print("Няма резултати!")
        input("-\nНатиснете 'enter' за връщане към менюто...")
        os.system('cls')
        show_expense(u_account)

#

def show_income(account):
    os.system('cls' if os.name == 'nt' else 'clear')
    print("##############################\n# Приходи\n##############################\n-\n1 - Преглед по дата\n2 - Преглед по сума\n\
3 - Преглед по описание\n4 - Преглед на всички приходи\n5 - Показване на приходи за определени дни назад\n6 - Назад\n")
    value = input("Избор: ")
    if value == "1":
        in_date = date_validation("search")
        if in_date == "":
            show_income(account)
        sign = sign_date(in_date)
        os.system('cls')
        if sign == ">":
            show_income_by_date = session.query(Income).join(Account).filter(Account.email == account.email, \
                                Income.date_income > in_date).order_by(Income.date_income).all()
        if sign == "<":
            show_income_by_date = session.query(Income).join(Account).filter(Account.email == account.email, \
                                Income.date_income < in_date).order_by(Income.date_income).all()
        if sign == "==":
            show_income_by_date = session.query(Income).join(Account).filter(Account.email == account.email, \
                                Income.date_income == in_date).order_by(Income.date_income).all()
        print(f"Показване на приходи {sign_return(sign)} {in_date} | ({account.email})\n-")
        for income_result in show_income_by_date:
            print(f"{income_result.sum_income:.2f} лв. | дата: {income_result.date_income} | описание: {income_result.desc_income} ")
        if show_income_by_date == []:
            print("Няма резултати!")
        input("-\nНатиснете 'enter' за връщане към менюто...")
        os.system('cls')
        show_income(account)

    elif value == "2":
        in_sum = sum_validate()
        sign = sign_exsum(in_sum)
        if sign == "":
            show_income(account)
        os.system('cls')
        print(f"##############################\n# Показване на приходи за резултат {sign} {in_sum:.2f} | ({account.email})\n-")
        if sign == ">":
            show_income_by_sum = session.query(Income).join(Account).filter(Account.email == account.email, \
                                Income.sum_income > in_sum).order_by(Income.sum_income).all()
        if sign == "<":
            show_income_by_sum = session.query(Income).join(Account).filter(Account.email == account.email, \
                                Income.sum_income < in_sum).order_by(Income.sum_income).all()
        if sign == "==":
            show_income_by_sum = session.query(Income).join(Account).filter(Account.email == account.email, \
                                Income.sum_income == in_sum).order_by(Income.sum_income).all()
        for income_result in show_income_by_sum:
            print(f"{income_result.sum_income:.2f} лв. | дата: {income_result.date_income} | описание: {income_result.desc_income} ")
        if show_income_by_sum == []:
            print("Няма резултати!")
        input("-\nНатиснете 'enter' за връщане към менюто...")
        os.system('cls')
        show_income(account)
    
    elif value == "3":
        in_desc = input("Въведете описание за приход: ") + "%"
        if in_desc == "":
            show_income(account)
        os.system('cls')
        print(f"##############################\n# Показване на приходите за '{in_desc.replace("%","...")}' | ({account.email})\n-")
        show_income_by_desc = session.query(Income).join(Account).filter(Account.email == account.email,\
        Income.desc_income.like(in_desc)).order_by(Income.date_income).all()
        for income_result in show_income_by_desc:
            print(f"{income_result.sum_income:.2f} лв. | дата: {income_result.date_income} | описание: {income_result.desc_income} ")
        if show_income_by_desc == []:
            print("Няма резултати!")
        input("-\nНатиснете 'enter' за връщане към менюто...")
        os.system('cls')
        show_income(account)
    
    elif value == "4":
        os.system('cls')
        print(f"Показване на списък с всички приходи | {account.name} ({account.email})\n-")
        for income in account.incomes:
            print(f"{income.sum_income:.2f} лв. | дата: {income.date_income} | описание: {income.desc_income}")
        if account.incomes == []:
            print("Няма резултати!")
        input("-\nНатиснете 'enter' за връщане към менюто...")
        os.system('cls')
        show_income(account)

    elif value == "5":
        old_days = days_validate()
        old_days_ = date.today() - timedelta(days=old_days)
        os.system('cls')
        print(f"Показване на списък с приходи за {old_days} {'дни' if old_days > 1 else 'ден'} назад | ({account.email})\n-")
        older_data = session.query(Income).join(Account).filter(Account.email == account.email, \
                Income.date_income >= old_days_).order_by(Income.date_income).all()
        for data in older_data:
            print(f"{data.sum_income:.2f} лв. | дата: {data.date_income} | описание: {data.desc_income}")
        if older_data == []:
            print("Няма резултати!")
        input("-\nНатиснете 'enter' за връщане към менюто...")
        os.system('cls')
        show_income(account)

#
##############################################################################
# Show incomes => end
##############################################################################
# delete => Start
##############################################################################
#
        
def delete_func(delete_data, current_account):
    try:
        if delete_data:
            for record in delete_data:
                session.delete(record)
            session.commit()
            session.expire_all()
            print("Записите са изтрити успешно!\n-")
        else:
            print("Не е намерен запис с тези параметри.")
    except Exception as e:
        session.rollback()
        print(f"Възникна грешка: {e}")

    finally:
        input("Натиснете 'enter' за връщане назад...")
        update_menu(current_account)  

#
##############################################################################
# delete => end
##############################################################################
# Show balans => Start
##############################################################################
#
        
def show_balans(u_account):
    from account_functions import month
    os.system('cls' if os.name == 'nt' else 'clear')
    last_year = date.today() - timedelta(days=365)
    last_year_income = session.query(Income).join(Account).filter(Account.email == u_account.email, \
                Income.date_income >= last_year).order_by(Income.date_income).all()
    last_year_expense = session.query(Expense).join(Account).filter(Account.email == u_account.email, \
                Expense.date_expense >= last_year).order_by(Expense.date_expense).all()
    list_last_year_expense = []
    list_last_year_income = []
    for y in last_year_income:
        list_last_year_income.append(y.sum_income)
    for y in last_year_expense:
        list_last_year_expense.append(y.sum_expense)
    sum_last_year_income = sum(list_last_year_income)
    sum_last_year_expense = sum(list_last_year_expense)
    def nth(x):
        if x in [1,21,31]:
            return "ви"
        elif x in [2,22]:
            return "ри"
        elif x in [7,8,27,28]:
            return "ми"
        else:
            return "ти"
    exp = get_expense(u_account)
    try:
        year_exp = list(exp.keys())[-1]
    except:
        year_exp = {1:{1:1}}
    inc = get_income(u_account)
    
    try:
        year_inc = list(inc.keys())[-1]
    except:
        year_inc = {1:{1:1}}
    try:
        last_month = np.sum(exp[year_exp][list(exp[year_exp].keys())[-1]]) / 30
    except:
        last_month = 1
    balans = sum(income.sum_income for income in u_account.incomes) - sum(expense.sum_expense for expense in u_account.expenses)
    rundown = int(balans / last_month)
    upcoming_list = []
    date_string = date.today()
    days_limit_end = date_string - timedelta(days=20)
    days_limmit_start = date_string - timedelta(days=30)
    rundown_status = session.query(Expense).join(Account).filter(
            Account.email == u_account.email, Expense.date_expense < days_limmit_start
            ).order_by(Expense.date_expense).limit(5).all()
    
    upcoming = session.query(Expense).join(Account).filter(
            Account.email == u_account.email, Expense.date_expense >= days_limmit_start, Expense.date_expense < days_limit_end
            ).order_by(Expense.date_expense).limit(5).all()
    for acc in upcoming:
        upcoming_list.append(f"{acc.date_expense.day}-{nth(acc.date_expense.day)} - {acc.desc_expense} (около {acc.sum_expense:.2f} лв.)")
    print(f"###############################################\n# Баланс: {sum(income.sum_income for income in u_account.incomes) - \
                                            sum(expense.sum_expense for expense in u_account.expenses):.2f} лв. | Дата: {date.today()}")
    print(f"# Акаунт: {u_account.email} | Име: {u_account.name}")
    print("-")
    print(f"> Общо приходи: {sum(income.sum_income for income in u_account.incomes):.2f} лв. \
(за последната година: {sum_last_year_income:.2f} лв.)")
    print(f"> Общо разходи: {sum(expense.sum_expense for expense in u_account.expenses):.2f} лв. \
(за последната година: {sum_last_year_expense:.2f} лв.)")
    try:
        print(f"> Разход за последния месец {month[list(exp[year_inc].keys())[-1]]}: {np.sum(exp[year_exp][list(exp[year_exp].keys())[-1]]):.2f} лв. \
(средно на ден: {np.sum(exp[year_exp][list(exp[year_exp].keys())[-1]])/30:.2f} лв.)")
    except:
        pass
    try:
        print(f"> Приход за последния месец {month[list(exp[year_inc].keys())[-1]]}: {np.sum(inc[year_inc][list(exp[year_inc].keys())[-1]]):.2f} лв. \
(средно на ден: {np.sum(inc[year_inc][list(exp[year_inc].keys())[-1]])/30:.2f} лв.)")
    except:
        pass
    if rundown_status:
        print(f"> Наличната сума е достатъчна за около {rundown} дни без приходи.")
    else:
        print(f"> Недостатъчна информация за анализ на приходи и разходи (необходими са 30 дни).")

    if upcoming_list:
        print(f"> Възможни предстоящи разходи: {", ".join(upcoming_list)}")
    input("-\n* Натиснете 'enter' за връщане назад...")
    show_data_menu(u_account)

#
##############################################################################
# Show balans => End
##############################################################################
# Add functions => Start
##############################################################################
#

def add_income(current_account):
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        print("##############################\n# Добавяне на приходи\n-")
        current_date = date.today()
        sum_income = sum_validate()
        desc_income = input("Въведете описание на прихода: ")
        try:
            income = Income(sum_income=sum_income, date_income=current_date, desc_income=desc_income, account_email=current_account.email)
            session.add(income)
            session.commit()
            print(f"-\nУспешно добавен приход от {sum_income} на {current_date} с описание '{desc_income}'.")
            print("-\nВъведете '1' за връщане назад или 'enter' без стойност за добавяне на нова сума")
            if input() == "1":
                Load_Menu(current_account)
                break
            else:
                continue
        except IntegrityError as e:
            session.rollback()
            print(f"Грешка при добавяне на приход: {e}")
            if input("Желаете ли да опитате пак? да/не: ") == "да":
                continue
            else:
                Load_Menu(current_account)
                break

#
            
def add_expense(current_account):
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        print("##############################\n# Добавяне на разходи\n-")
        current_date = date.today()
        sum_expense = sum_validate()
        desc_expense = input("Въведете описание на разхода: ")
        try:
            expense = Expense(sum_expense=sum_expense, date_expense=current_date, desc_expense=desc_expense, account_email=current_account.email)
            session.add(expense)
            session.commit()
            print(f"Успешно добвен разход от {sum_expense} на {current_date} с описание '{desc_expense}'.")
            print("-\nВъведете '1' за връщане назад или 'enter' без стойност за добавяне на нова сума.")
            if input() == "1":
                Load_Menu(current_account)
                break
            else:
                continue
        except IntegrityError as e:
            session.rollback()
            print(f"-\n* Грешка при добавяне на разход: {e}")
            if input("Желаете ли да опитате пак? да/не: ") == "да":
                continue
            else:
                Load_Menu(current_account)
                break

#
##############################################################################
# Add functions => End
##############################################################################
# Get functions => Start
##############################################################################
#    
                        
def get_expense(account):
    query = session.query(Expense).join(Account).filter(Account.email == account.email).order_by(Expense.date_expense)
    current_month = None
    current_year = None
    current_data = []
    result = []
    for row in query:
        month = row.date_expense.month
        year = row.date_expense.year
        if month != current_month or year != current_year:
            if current_data:
                result.append((current_month, current_year, current_data))
            current_month = month
            current_year = year
            current_data = []
        current_data.append((row.date_expense, row.sum_expense))
    if current_data:
        result.append((current_month, current_year, current_data))
    y = {}
    m = {}
    for month, year, data in result:
        price = [x[1] for x in data]
        if year not in y:
            y[year] = {}
        m[month] = np.array(price)
        y[year][month] = m[month]
    return y

#

def get_income(account):
    query = session.query(Income).join(Account).filter(Account.email == account.email).order_by(Income.date_income)
    current_month = None
    current_year = None
    current_data = []
    result = []
    for row in query:
        month = row.date_income.month
        year = row.date_income.year
        if month != current_month or year != current_year:
            if current_data:
                result.append((current_month, current_year, current_data))
            current_month = month
            current_year = year
            current_data = []
        current_data.append((row.date_income, row.sum_income))
    if current_data:
        result.append((current_month, current_year, current_data))
    y = {}
    m = {}
    for month, year, data in result:
        price = [x[1] for x in data]
        if year not in y:
            y[year] = {}
        m[month] = np.array(price)
        y[year][month] = m[month]
    return y

#
##############################################################################
# Get functions => end
##############################################################################


if __name__ == '__main__':
    Load_Menu(current_account)



