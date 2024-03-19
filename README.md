# Financial Manager with console interface. (Bulgarian)

Available options:

 * Account option with username, password and name (passwords are encrypted)
   - Create account/Log in account
  
 * Add income/expense sum, reason (automatic added current date)
  
 * Delete incomes/expenses by date/sum/reason
  
 * Change incomes/expenses/password
  
 * DAta viewer
   - sorted by time, reason, sum, days ago
  
 * Balkans viewer (for all time, yearly, monthly)
   - rundown, possible subsequent costs
  
 * Diagram incomes/expenses for every one month and complete view

All packages:
  - os, time, datetime, sqlalchemy, bcrypt, numpy, tkinter, matplotlibm, unittest and coverage (for testing)

Installation:
  - git clone https://github.com/python2023user/final_project

  - conda install --file requirements.txt
    or
  - conda install -c conda-forge --file requirements.txt

How to use:
  - Start account.py file with command 'py account.py' or 'python account.py'
  - The database has 2 saved accounts with sample data for a year back

* Account 1:
  - email: ivan@example.com
  - password: Abc123456
 
* Account2:
  - email: petar@example.com
  - password: Abc123456
 
