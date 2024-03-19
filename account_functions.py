import numpy as np

def sign_return(sign):
    value = {">":"след","<":"преди","==":"за"}
    return value[sign]

def sign_exsum(ex_sum):
    print(f"1 - Суми по-големи от {ex_sum:.2f} лв.\n2 - Суми по-малки от {ex_sum:.2f} лв.\n3 - Суми равни на {ex_sum:.2f} лв.\n-")
    return_values = {"1":">","2":"<","3":"=="}
    value = input("Избор: ")
    if value == "":
        return sign_exsum(ex_sum)
    return return_values[value]
        
def sign_date(ex_date):
    print(f"1 - Резултати след {ex_date}\n2 - Резултати преди {ex_date}\n3 - За {ex_date}\n-")
    return_values = {"1":">","2":"<","3":"=="}
    value = input("Избор: ")
    return return_values[value]

def get_expense(account):
    from account import session, Expense, Account
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

def get_income(account):
    from account import session, Income, Account
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

month = {
    1: "Януари",
    2: "Февруари",
    3: "Март",
    4: "Април",
    5: "Май",
    6: "Юни",
    7: "Юли",
    8: "Август",
    9: "Септември",
    10: "Октомври",
    11: "Ноември",
    12: "Декември"
}
