import datetime as dt


class Calculator:
    def __init__(self, limit):
        self.records = []
        self.limit = limit

    def add_record(self, record):
        self.records.append(record)

    def get_balance(self):
        return self.limit - self.get_today_stats()

    def get_today_stats(self):
        today = dt.date.today()
        return sum([record.amount for record in self.records if record.date == today])

    def get_week_stats(self):
        today = dt.date.today()
        start_date = today - dt.timedelta(days=7)
        return sum([record.amount for record in self.records if today >= record.date >= start_date])


class Record:
    def __init__(self, amount, comment, date=None):
        self.amount = amount
        if date is None:
            self.date = dt.date.today()
        else:
            self.date = dt.datetime.strptime(date, '%d.%m.%Y').date()
        self.comment = comment

    def __str__(self):
        return f'{self.date} | {self.amount} | {self.comment}'


class CaloriesCalculator(Calculator):

    def get_calories_remained(self):
        balance = self.get_balance()
        if balance > 0:
            return ('Сегодня можно съесть что-нибудь ещё, '
                    f'но с общей калорийностью не более {balance} кКал')
        return 'Хватит есть!'


class CashCalculator(Calculator):
    USD_RATE = 73.73
    EURO_RATE = 89.41
    RUB_RATE = 1

    def get_today_cash_remained(self, currency):

        currencies = {'usd': (self.USD_RATE, 'USD'),
                      'eur': (self.EURO_RATE, 'Euro'),
                      'rub': (self.RUB_RATE, 'руб')}

        balance = self.limit - self.get_today_stats()
        if balance == 0:
            return 'Денег нет, держись'

        balance_in_currency = round(balance / currencies[currency][0], 2)
        currency_name = currencies[currency][1]

        if balance_in_currency > 0:
            return (f'На сегодня осталось {balance_in_currency} '
                    f'{currency_name}')
        else:
            return (f'Денег нет, держись: твой долг - '
                    f'{abs(balance_in_currency)}'
                    f' {currency_name}')
