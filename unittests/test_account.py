import sys
sys.path.insert(1, './')
import unittest
from unittest.mock import patch, MagicMock, call, builtins
from account import ( Account, Expense, session, Income, show_expense, show_income,
                     show_balans, log_in, login_request, Load_Menu, delete_func,
                      update_menu, change_incomes, change_expenses, change_password )
                       
from datetime import date, timedelta

class TestLogin(unittest.TestCase):

    @patch('account.session')
    @patch('account.bcrypt')
    @patch('os.system')
    def test_log_in_success(self, mock_system, mock_bcrypt, mock_session):
        mock_account = Account(email='test@example.com', password=b'hashed_password')
        mock_session.query(Account).filter().first.return_value = mock_account
        mock_bcrypt.checkpw.return_value = True
        result = log_in('test@example.com', 'password')
        mock_system.assert_called_with('cls')
        self.assertEqual(result, mock_account)

    @patch('account.session')
    @patch('account.bcrypt')
    @patch('os.system')
    def test_log_in_failure(self, mock_system, mock_bcrypt, mock_session):
        mock_session.query(Account).filter().first.return_value = None
        mock_bcrypt.checkpw.return_value = False
        with patch('account.login_request') as mock_login_request:
            log_in('wrong@example.com', 'password')
            mock_login_request.assert_called()

    @patch('os.system')
    @patch('builtins.input', side_effect=['test@example.com', 'password'])
    @patch('account.log_in')
    def test_login_request_success(self, mock_log_in, mock_input, mock_system):
        mock_account = Account(email='test@example.com', password=b'hashed_password')

        login_request(mock_account)

        mock_log_in.assert_called_with('test@example.com', 'password')

#

class TestShowExpense(unittest.TestCase):
    @patch('account.input', side_effect=['2', '100', '', 'additional input']) 
    @patch('account.sum_validate', return_value=100.0)
    @patch('account.sign_exsum', return_value='>')
    @patch('account.session.query')
    def test_show_expense_by_sum(self, mock_query, mock_sign_exsum, mock_sum_validate, mock_input):
        mock_account = MagicMock(spec=Account)
        mock_account.email = 'test@example.com'
        mock_expense = MagicMock(spec=Expense)
        mock_expense.sum_expense = 150.0
        mock_expense.date_expense = '2023-03-18'
        mock_expense.desc_expense = 'Test expense over 100'
        mock_expense.account_email = 'test@example.com'
        mock_query.return_value.join.return_value.filter.return_value.order_by.return_value.all.return_value = [mock_expense]
        show_expense(mock_account)
        mock_query.assert_called_with(Expense)
        self.assertEqual(mock_input.call_count, 3)
        mock_sum_validate.assert_called_once()
        mock_sign_exsum.assert_called_with(100.0)
 
    @patch('account.input', side_effect=['3', 'Test description', '', 'additional input'])
    @patch('account.session.query')
    def test_show_expense_by_description(self, mock_query, mock_input):
        mock_account = MagicMock(spec=Account)
        mock_account.email = 'test@example.com'
        mock_expense = MagicMock(spec=Expense)
        mock_expense.sum_expense = 50.0
        mock_expense.date_expense = '2024-03-18'
        mock_expense.desc_expense = 'Test description'
        mock_expense.account_email = 'test@example.com'
        mock_query.return_value.join.return_value.filter.return_value.order_by.return_value.all.return_value = [mock_expense]
        show_expense(mock_account)
        mock_query.assert_called_with(Expense)
        self.assertEqual(mock_input.call_count, 4)

    @patch('builtins.input', side_effect=iter(['4', '']))
    def test_show_all_expenses(self, mock_input):
        mock_account = MagicMock(spec=Account)
        mock_account.email = 'test@example.com'
        mock_expense1 = MagicMock(spec=Expense)
        mock_expense1.sum_expense = 50.0
        mock_expense1.date_expense = '2024-03-18'
        mock_expense1.desc_expense = 'Groceries'
        mock_expense2 = MagicMock(spec=Expense)
        mock_expense2.sum_expense = 20.0
        mock_expense2.date_expense = '2024-03-19'
        mock_expense2.desc_expense = 'Transport'  
        mock_account.expenses = [mock_expense1, mock_expense2]
        show_expense(mock_account)
        self.assertEqual(mock_input.call_count, 2)

    @patch('builtins.print', MagicMock())
    @patch('builtins.input', side_effect=iter(['5', '2', '', '']))
    def test_show_expenses_for_days(self, mock_input):
        mock_account = MagicMock(spec=Account)
        mock_account.email = 'test@example.com'
        mock_expense1 = MagicMock(spec=Expense)
        mock_expense1.sum_expense = 50.0
        mock_expense1.date_expense = date.today() - timedelta(days=2)
        mock_expense1.desc_expense = 'Groceries'
        mock_expense2 = MagicMock(spec=Expense)
        mock_expense2.sum_expense = 20.0
        mock_expense2.date_expense = date.today() - timedelta(days=1)
        mock_expense2.desc_expense = 'Transport'
        
        with patch('account.session.query') as mock_query:
            mock_query.return_value.join.return_value.filter.return_value.order_by.return_value.all.return_value = [mock_expense1, mock_expense2]
            show_expense(mock_account)
            self.assertEqual(mock_input.call_count, 4) 
            mock_print_calls = [call[0][0] for call in builtins.print.call_args_list]
            expected_output = "Показване на списък с разходи за за 2 дни назад | (test@example.com)\n-"
            self.assertIn(expected_output, mock_print_calls)

class TestShowIncomee(unittest.TestCase):
    @patch('account.input', side_effect=['2', '100', '', 'additional input']) 
    @patch('account.sum_validate', return_value=100.0)
    @patch('account.sign_exsum', return_value='>')
    @patch('account.session.query')
    def test_show_income_by_sum(self, mock_query, mock_sign_exsum, mock_sum_validate, mock_input):
        mock_account = MagicMock(spec=Account)
        mock_account.email = 'test@example.com'
        mock_income = MagicMock(spec=Income)
        mock_income.sum_income = 150.0
        mock_income.date_income = '2023-03-18'
        mock_income.desc_income = 'Test income over 100'
        mock_income.account_email = 'test@example.com'
        mock_query.return_value.join.return_value.filter.return_value.order_by.return_value.all.return_value = [mock_income]
        show_income(mock_account)
        mock_query.assert_called_with(Income)
        self.assertEqual(mock_input.call_count, 3)
        mock_sum_validate.assert_called_once()
        mock_sign_exsum.assert_called_with(100.0)
 
    @patch('account.input', side_effect=['3', 'Test description', '', 'additional input'])
    @patch('account.session.query')
    def test_show_income_by_description(self, mock_query, mock_input):
        mock_account = MagicMock(spec=Account)
        mock_account.email = 'test@example.com'
        mock_income = MagicMock(spec=Income)
        mock_income.sum_income = 50.0
        mock_income.date_income = '2024-03-18'
        mock_income.desc_income = 'Test description'
        mock_income.account_email = 'test@example.com'
        mock_query.return_value.join.return_value.filter.return_value.order_by.return_value.all.return_value = [mock_income]
        show_income(mock_account)
        mock_query.assert_called_with(Income)
        self.assertEqual(mock_input.call_count, 4)

    @patch('builtins.input', side_effect=iter(['4', '']))
    def test_show_all_incomes(self, mock_input):
        mock_account = MagicMock(spec=Account)
        mock_account.email = 'test@example.com'
        mock_expense1 = MagicMock(spec=Expense)
        mock_expense1.sum_expense = 50.0
        mock_expense1.date_expense = '2024-03-18'
        mock_expense1.desc_expense = 'Groceries'
        mock_expense2 = MagicMock(spec=Expense)
        mock_expense2.sum_expense = 20.0
        mock_expense2.date_expense = '2024-03-19'
        mock_expense2.desc_expense = 'Transport'  
        mock_account.expenses = [mock_expense1, mock_expense2]
        show_expense(mock_account)
        self.assertEqual(mock_input.call_count, 2)

    @patch('builtins.print', MagicMock())
    @patch('builtins.input', side_effect=iter(['5', '2', '', '']))
    def test_show_incomes_for_days(self, mock_input):
        mock_account = MagicMock(spec=Account)
        mock_account.email = 'test@example.com'
        mock_income1 = MagicMock(spec=Income)
        mock_income1.sum_income = 50.0
        mock_income1.date_income = date.today() - timedelta(days=2)
        mock_income1.desc_income = 'Groceries'
        mock_income2 = MagicMock(spec=Income)
        mock_income2.sum_income = 20.0
        mock_income2.date_income = date.today() - timedelta(days=1)
        mock_income2.desc_income = 'Transport'
        
        with patch('account.session.query') as mock_query:
            mock_query.return_value.join.return_value.filter.return_value.order_by.return_value.all.return_value = [mock_income1, mock_income2]
            show_income(mock_account)
            self.assertEqual(mock_input.call_count, 4) 
            mock_print_calls = [call[0][0] for call in builtins.print.call_args_list]
            expected_output = "Показване на списък с приходи за 2 дни назад | (test@example.com)\n-"
            self.assertIn(expected_output, mock_print_calls)    


class TestDeleteFunc(unittest.TestCase):
    @patch('account.session')
    @patch('account.update_menu')
    @patch('account.input', return_value='')
    def test_delete_func_with_data(self, mock_input, mock_update_menu, mock_session):
        delete_data = [MagicMock(), MagicMock()]
        current_account = MagicMock()
        delete_func(delete_data, current_account)
        self.assertEqual(mock_session.delete.call_count, len(delete_data))
        mock_session.commit.assert_called_once()
        mock_update_menu.assert_called_once_with(current_account)

    @patch('account.session')
    @patch('account.update_menu')
    @patch('account.input', return_value='')
    def test_delete_func_without_data(self, mock_input, mock_update_menu, mock_session):
        delete_data = []
        current_account = MagicMock()

        delete_func(delete_data, current_account)

        mock_session.delete.assert_not_called()
        mock_session.commit.assert_not_called()
        mock_update_menu.assert_called_once_with(current_account)

    @patch('account.session')
    @patch('account.update_menu')
    @patch('account.input', return_value='')
    def test_delete_func_exception(self, mock_input, mock_update_menu, mock_session):
        delete_data = [MagicMock()]
        current_account = MagicMock()
        mock_session.commit.side_effect = Exception("Test exception")
        delete_func(delete_data, current_account)
        mock_session.rollback.assert_called_once()
        mock_update_menu.assert_called_once_with(current_account)

#####
        
class TestUpdateMenu(unittest.TestCase):
    @patch('account.input', return_value='1')
    @patch('account.change_incomes')
    def test_update_menu_incomes(self, mock_change_incomes, mock_input):
        current_account = 'test_account'
        update_menu(current_account)
        mock_change_incomes.assert_called_once_with(current_account)

    @patch('account.input', return_value='2')
    @patch('account.change_expenses')
    def test_update_menu_expenses(self, mock_change_expenses, mock_input):
        current_account = 'test_account'
        update_menu(current_account)
        mock_change_expenses.assert_called_once_with(current_account)

    @patch('account.input', return_value='3')
    @patch('account.change_password')
    def test_update_menu_password(self, mock_change_password, mock_input):
        current_account = 'test_account'
        update_menu(current_account)
        mock_change_password.assert_called_once_with(current_account)

    @patch('account.input', return_value='4')
    @patch('account.Load_Menu')
    def test_update_menu_load_menu(self, mock_Load_Menu, mock_input):
        current_account = 'test_account'
        update_menu(current_account)
        mock_Load_Menu.assert_called_once_with(current_account)   

if __name__ == '__main__':
    unittest.main()
