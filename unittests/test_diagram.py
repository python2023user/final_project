import unittest
import numpy as np

def summarize_data(exp, inc, month):
    expense_list = []
    income_list = []
    months = []
    months_names = []

    for x, y in exp.items():
        for z in exp[x]:
            months.append(str(z))
            months_names.append(f"{month[z]} ({x})")
            expense_list.append(np.sum(exp[x][z]))
    for x, y in inc.items():
        for z in inc[x]:
            income_list.append(np.sum(inc[x][z]))

    return expense_list, income_list, months, months_names


class TestDataProcessing(unittest.TestCase):
    def test_summarize_data(self):
        exp = {'2023': {1: [50, 100], 2: [30]}, '2024': {1: [20]}}
        inc = {'2023': {1: [200], 2: [100]}, '2024': {1: [300]}}
        month = {1: 'January', 2: 'February'}
        expected_expense_list = [150, 30, 20]
        expected_income_list = [200, 100, 300]
        expected_months = ['1', '2', '1']
        expected_months_names = ['January (2023)', 'February (2023)', 'January (2024)']
        expense_list, income_list, months, months_names = summarize_data(exp, inc, month)
        self.assertEqual(expense_list, expected_expense_list)
        self.assertEqual(income_list, expected_income_list)
        self.assertEqual(months, expected_months)
        self.assertEqual(months_names, expected_months_names)

if __name__ == '__main__':
    unittest.main()