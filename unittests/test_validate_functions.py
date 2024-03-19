import sys
sys.path.insert(1, './')
import unittest
from validate_functions import *
from unittest.mock import patch
from account import Load_Menu

class TestSumValidate(unittest.TestCase):
    def test_sum_validate(self):
        with unittest.mock.patch('builtins.input', return_value='100'):
            self.assertEqual(sum_validate(1), 100.0)

        with unittest.mock.patch('builtins.input', return_value='200.50'):
            self.assertEqual(sum_validate("new_sum"), 200.5)

        with unittest.mock.patch('builtins.input', side_effect=['invalid', '300']):
            self.assertEqual(sum_validate("change"), 300.0)


@patch('account.Load_Menu')
@patch('bcrypt.hashpw')
@patch('bcrypt.gensalt')
class TestPasswordValidator(unittest.TestCase):
    def test_empty_password_redirects_to_menu(self, mock_gensalt, mock_hashpw, mock_Load_Menu):
        with patch('builtins.input', return_value=''):
            password_validator('dummy_account')
            mock_Load_Menu.assert_called_once()

    def test_password_with_all_requirements_returns_hash(self, mock_gensalt, mock_hashpw, mock_Load_Menu):
        password = "Valid1Password"
        mock_gensalt.return_value = b'somesalt'
        expected_hash = bcrypt.hashpw(password.encode('utf-8'), b'somesalt')
        mock_hashpw.return_value = expected_hash

        with patch('builtins.input', return_value=password):
            hashed_password, plain_password = password_validator('dummy_account', status=0)
            self.assertEqual(plain_password, password)
            self.assertEqual(hashed_password, expected_hash)

    def test_invalid_password_prompts_again(self, mock_gensalt, mock_hashpw, mock_Load_Menu):
        invalid_password = "short"
        valid_password = "Valid1Password"
        mock_gensalt.return_value = b'somesalt'
        expected_hash = bcrypt.hashpw(valid_password.encode('utf-8'), b'somesalt')
        mock_hashpw.return_value = expected_hash

        with patch('builtins.input', side_effect=[invalid_password, valid_password]) as mock_input:
            hashed_password, plain_password = password_validator('dummy_account', status=0)
            self.assertEqual(mock_input.call_count, 2)
            self.assertEqual(plain_password, valid_password)
            self.assertEqual(hashed_password, expected_hash)

class TestDateValidation(unittest.TestCase):
    @patch('builtins.input', side_effect=['2023-03-17'])
    @patch('builtins.print')
    def test_date_validation_valid(self, mock_print, mock_input):
        operation = 'new_date'
        expected_date = '2023-03-17'
        result = date_validation(operation)
        self.assertEqual(result, expected_date)


class TestEmailValidation(unittest.TestCase):

    @patch('builtins.input', return_value="test@example.com")
    @patch('validate_functions.validate_email')  
    def test_valid_email(self, mock_validate_email, mock_input):
        mock_validate_email.return_value = None
        result = email_validate("current_account")  
        self.assertEqual(result, "test@example.com")

    @patch('builtins.input', return_value="")
    @patch('account.Load_Menu')  
    @patch('validate_functions.validate_email')  
    def test_empty_email(self, mock_validate_email, mock_load_menu, mock_input):
        mock_load_menu.return_value = "Load Menu Returned"
        result = email_validate("current_account") 
        self.assertEqual(result, "Load Menu Returned")

    # @patch('builtins.input', return_value="wrong_email_format")
    # @patch('validate_functions.validate_email')  
    # def test_invalid_email(self, mock_validate_email, mock_input):
    #     mock_validate_email.side_effect = Exception('Invalid email')
    #     with self.assertRaises(Exception) as context:
    #         email_validate("current_account") 
    #     self.assertTrue('Невалиден email!' in str(context.exception))
    # @patch('builtins.input', return_value="wrong_email_format")
    # @patch('validate_functions.validate_email')  # Replace with your correct module
    # def test_invalid_email(self, mock_validate_email, mock_input):
    #     mock_validate_email.side_effect = Exception('Invalid email')
    #     with self.assertRaises(Exception) as context:
    #         email_validate("MockAccount")  # Replace "MockAccount" with the actual account object if needed
    #     self.assertTrue('-\nНевалиден email!\n-' in str(context.exception))


if __name__ == '__main__':
    unittest.main()