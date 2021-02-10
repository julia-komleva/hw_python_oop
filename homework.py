import datetime as dt


class Calculator:
    def __init__(self, limit):
        self.records = []
        self.limit = limit

    def add_record(self, record):
        self.records.append(record)

    def get_today_stats(self):
        stats = 0
        today = dt.date.today()
        for record in self.records:
            if record.date == today:
                stats += record.amount
        return stats

    def get_week_stats(self):
        stats = 0
        today = dt.date.today()
        for record in self.records:
            if today >= record.date >= today - dt.timedelta(days=7):
                stats += record.amount
        return stats


class Record:
    def __init__(self, amount=0, date=None, comment='comment'):
        self.amount = amount
        if date:
            self.date = dt.datetime.strptime(date, '%d.%m.%Y').date()
        else:
            self.date = dt.date.today()
        self.comment = comment

    def __str__(self):
        return f'{self.date} | {self.amount} | {self.comment}'


class CaloriesCalculator(Calculator):

    def get_calories_remained(self):
        balance = self.limit - self.get_today_stats()
        if balance > 0:
            return (f'Сегодня можно съесть что-нибудь ещё, '
                    f'но с общей калорийностью не более {balance} кКал')
        else:
            return 'Хватит есть!'


class CashCalculator(Calculator):
    USD_RATE = 73.73
    EURO_RATE = 89.41
    RUB_RATE = 1

    def get_today_cash_remained(self, currency):
        # to avoid if statements
        currency_rates = {'usd': self.USD_RATE,
                          'eur': self.EURO_RATE,
                          'rub': self.RUB_RATE}

        # output format requirements
        currency_names = {'usd': 'USD', 'eur': 'Euro', 'rub': 'руб'}

        balance = self.limit - self.get_today_stats()
        limit_in_currency = round(balance / currency_rates[currency], 2)

        if limit_in_currency > 0:
            return (f'На сегодня осталось {limit_in_currency} '
                    f'{currency_names[currency]}')
        elif limit_in_currency == 0:
            return 'Денег нет, держись'
        else:
            return (f'Денег нет, держись: твой долг - {abs(limit_in_currency)}'
                    f' {currency_names[currency]}')


cash_calculator = CashCalculator(5000)
cash_calculator.add_record(Record(amount=145, comment='кофе'))
cash_calculator.add_record(Record(amount=300, comment='Серёге за обед'))
cash_calculator.add_record(Record(amount=3000,
                                  comment='бар в Танин др',
                                  date='08.11.2019'))
cash_calculator.add_record(Record(amount=3000,
                                  comment='др',
                                  date='08.02.2021'))

print(cash_calculator.get_today_cash_remained('rub'))
print(cash_calculator.get_today_cash_remained('eur'))
print(cash_calculator.get_today_cash_remained('usd'))

print(cash_calculator.get_today_stats())
print(cash_calculator.get_week_stats())
