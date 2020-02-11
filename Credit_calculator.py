# JetBrains Academy/Python Developer
# Project: Credit Calculator
# Stage 4/4: Differentiate payment

import sys
import math
import argparse


class Get:
    def credit_principal(self):
        """It is required to ask the user to input the credit principal"""
        return float(input('Enter the credit principal: '))

    def monthly_payment(self):
        """It is required to ask the user to input the monthly payment"""
        return float(input('Enter the monthly payment: '))

    def credit_interest(self):
        """It is required to ask the user to input the credit interest"""
        return float(input('Enter the credit interest: '))

    def count_of_periods(self):
        """It is required to ask the user to input the count of periods"""
        return float(input('Enter the count of periods: '))

    def type_calculate(self):
        """The user should tell what needs to be calculated (the monthly payment or the count of periods)"""
        print('What do you want to calculate?')
        print('type "n" - for count of months,')
        print('type "a" - for annuity monthly payment,')
        print('type "p" - for credit principal:')
        print('type "d" - for differentiate payment:')
        return input().strip()


class Shell:
    def __init__(self):
        self.is_shell = True
        parser = argparse.ArgumentParser()
        parser.add_argument('--type', default=None, type=str)
        parser.add_argument('--payment', default=None, type=float)
        parser.add_argument('--principal', default=None, type=float)
        parser.add_argument('--periods', default=None, type=float)
        parser.add_argument('--interest', default=None, type=float)
        self.args = parser.parse_args(sys.argv[1:])
        if not self.run_from_shell():
            self.is_shell = False
            return

    def run_from_shell(self):
        """Returns true if the script is run with parameters from the command line, otherwise false"""
        return True if len(sys.argv) > 1 else False

    def get_type_calculate(self):
        """Returns type_calculate if the received parameters are correct, otherwise error"""
        for i in [self.args.type, self.args.principal, self.args.periods, self.args.interest, self.args.payment]:
            if type(i) is float and i < 0.0:
                return 'error'
        if len(sys.argv) != 5:
            return 'error'
        if self.args.type == 'annuity':
            if self.args.periods and self.args.interest and self.args.principal:
                return 'a'
            if self.args.payment and self.args.periods and self.args.interest:
                return 'p'
            if self.args.principal and self.args.payment and self.args.interest:
                return 'n'
        if self.args.type == 'diff':
            if self.args.principal and self.args.periods and self.args.interest:
                return 'd'
        return 'error'


class Calculator:
    def __init__(self):
        self.get = Get()
        self.shell = Shell()
        self.credit_principal = 0.0
        self.monthly_payment = 0.0
        self.credit_interest = 0.0
        self.count_of_period = 0.0
        if self.shell.is_shell:
            self.type_calculate = self.shell.get_type_calculate()
        else:
            self.type_calculate = self.get.type_calculate()
        self.calculate()

    def calc_count_of_months(self):
        """Calculate count of month and return a answer as the string"""
        i = self.credit_interest / 1200
        months = math.ceil(math.log(self.monthly_payment / (self.monthly_payment - i * self.credit_principal), 1 + i))
        years = months // 12
        remainder = months - years * 12
        out = ''
        if years > 0 and remainder > 0:
            out = f'You need {years} years and {remainder} months to repay this credit!'
        elif remainder == 0 and years > 0:
            out = f'You need {years} {"year" if years == 1 else "years"} to repay this credit!'
        elif years == 0 and remainder > 0:
            out = f'You need {remainder} months to repay this credit!'
        else:
            out = f'Something wrong!'
        return out + f'\nOverpayment = {math.ceil(self.monthly_payment * months - self.credit_principal)}'

    def calc_annuity_payment(self):
        """Calculate annuity payment and return it as the string"""
        i = self.credit_interest / 1200
        a1 = i * (1 + i) ** self.count_of_period
        a2 = (1 + i) ** self.count_of_period - 1
        annuity_payment = math.ceil(self.credit_principal * a1 / a2)
        return f'Your annuity payment = {annuity_payment}!\n' \
               f'Overpayment = {math.ceil(annuity_payment * self.count_of_period - self.credit_principal)}'

    def calc_credit_principal(self):
        """Calculate credit principal and return it as the string"""
        i = self.credit_interest / 1200
        a1 = i * (1 + i) ** self.count_of_period
        a2 = (1 + i) ** self.count_of_period - 1
        credit_principal = math.floor(self.monthly_payment / (a1 / a2))
        return f'Your credit principal = {credit_principal}!\n' \
               f'Overpayment = {math.ceil(self.monthly_payment * self.count_of_period - credit_principal)}'

    def mth_differentiated_payment(self, m):
        """Main formula for calculate month differentiated payment"""
        i = self.credit_interest / 1200
        output = self.credit_principal / self.count_of_period + i * \
                 (self.credit_principal - (self.credit_principal * (m - 1) / self.count_of_period))
        return math.ceil(output)

    def calc_mth_differentiated_payment(self):
        """Calculate month differentiated payment and return it as the string"""
        amount = 0
        formatted_output = ''
        for m in range(int(self.count_of_period)):
            diff = self.mth_differentiated_payment(m + 1)
            amount += diff
            formatted_output += f'Month {m + 1}: paid out {diff}\n'
        overpayment = int(amount - self.credit_principal)
        formatted_output += f'\nOverpayment = {overpayment}'
        return formatted_output

    def calculate(self):
        """Main calculation function"""
        if self.type_calculate == 'n':
            if self.shell.is_shell:
                self.credit_principal = self.shell.args.principal
                self.monthly_payment = self.shell.args.payment
                self.credit_interest = self.shell.args.interest
            else:
                self.credit_principal = float(input('Enter credit principal: '))
                self.monthly_payment = float(input('Enter monthly payment: '))
                self.credit_interest = float(input('Enter credit interest: '))
            print(self.calc_count_of_months())
        elif self.type_calculate == 'a':
            if self.shell.is_shell:
                self.credit_principal = self.shell.args.principal
                self.count_of_period = self.shell.args.periods
                self.credit_interest = self.shell.args.interest
            else:
                self.credit_principal = float(input('Enter credit principal: '))
                self.count_of_period = float(input('Enter count of periods: '))
                self.credit_interest = float(input('Enter credit interest: '))
            print(self.calc_annuity_payment())
        elif self.type_calculate == 'p':
            if self.shell.is_shell:
                self.monthly_payment = self.shell.args.payment
                self.count_of_period = self.shell.args.periods
                self.credit_interest = self.shell.args.interest
            else:
                self.monthly_payment = float(input('Enter monthly payment: '))
                self.count_of_period = float(input('Enter count of periods: '))
                self.credit_interest = float(input('Enter credit interest: '))
            print(self.calc_credit_principal())
        elif self.type_calculate == 'd':
            if self.shell.is_shell:
                self.credit_principal = self.shell.args.principal
                self.count_of_period = self.shell.args.periods
                self.credit_interest = self.shell.args.interest
            else:
                self.credit_principal = float(input('Enter credit principal: '))
                self.count_of_period = float(input('Enter count of periods: '))
                self.credit_interest = float(input('Enter credit interest: '))
            print(self.calc_mth_differentiated_payment())
        else:
            print('Incorrect parameters.')


if __name__ == "__main__":
    calc = Calculator()
