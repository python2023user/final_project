import sys
sys.path.insert(1, './')
import unittest
from datetime import date
from unittest.mock import patch
from account import Expense, Income, Account, session, Load_Menu, add_income
from account_functions import get_expense
from account_functions import sign_return, sign_date, sign_exsum
import numpy as np
from validate_functions import sum_validate, email_validate

class TestSignFunctions(unittest.TestCase):
    def test_sign_return(self):
        self.assertEqual(sign_return(">"), "след")
        self.assertEqual(sign_return("<"), "преди")
        self.assertEqual(sign_return("=="), "за")

    def test_sign_exsum(self):
        with unittest.mock.patch('builtins.input', return_value="1"):
            self.assertEqual(sign_exsum(100), ">")

    def test_sign_date(self):
        with unittest.mock.patch('builtins.input', return_value="3"):
            self.assertEqual(sign_date("2024-03-17"), "==")

############


class TestGetExpense(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        account1 = Account(email='test@example.com', name='Test User', password='password123')
        session.add(account1)
        session.add_all([
            Expense(sum_expense=100.0, date_expense=date(2023, 1, 1), desc_expense='Groceries', account_email='test@example.com'),
            Expense(sum_expense=50.0, date_expense=date(2023, 1, 15), desc_expense='Utilities', account_email='test@example.com'),
            Expense(sum_expense=200.0, date_expense=date(2023, 2, 1), desc_expense='Rent', account_email='test@example.com')
        ])
        session.commit()

    def test_get_expense_group_by_month(self):
        from account_functions import get_expense 
        
        account = session.query(Account).filter_by(email='test@example.com').first()
        result = get_expense(account)
        self.assertIsInstance(result, dict)
        january_expenses = np.array([100.0, 50.0])
        np.testing.assert_array_equal(result[2023][1], january_expenses)
        february_expenses = np.array([200.0])
        np.testing.assert_array_equal(result[2023][2], february_expenses)


    @classmethod
    def tearDownClass(cls):
        account_to_delete = session.query(Account).filter(Account.email == 'test@example.com').first()
        if account_to_delete:
            session.delete(account_to_delete)
            session.commit()

###############

class TestGetIncome(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        account1 = Account(email='test@example.com', name='Test User', password='password123')
        session.add(account1)
        session.add_all([
            Income(sum_income=100.0, date_income=date(2023, 1, 1), desc_income='Groceries', account_email='test@example.com'),
            Income(sum_income=50.0, date_income=date(2023, 1, 15), desc_income='Utilities', account_email='test@example.com'),
            Income(sum_income=200.0, date_income=date(2023, 2, 1), desc_income='Rent', account_email='test@example.com')
        ])
        session.commit()

    def test_get_income_group_by_month(self):
        from account_functions import get_income
        
        account = session.query(Account).filter_by(email='test@example.com').first()
        result = get_income(account)
        self.assertIsInstance(result, dict)
        january_incomes = np.array([100.0, 50.0])
        np.testing.assert_array_equal(result[2023][1], january_incomes)
        february_incomes = np.array([200.0])
        np.testing.assert_array_equal(result[2023][2], february_incomes)

    @classmethod
    def tearDownClass(cls):
        account_to_delete = session.query(Account).filter(Account.email == 'test@example.com').first()
        if account_to_delete:
            session.delete(account_to_delete)
            session.commit()



if __name__ == '__main__':
    unittest.main()