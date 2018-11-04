import datetime

WEEKDAY = '.'
WEEKEND = 'S'
HOLIDAY = 'H'


class Day(object):

    date = None
    _value = 0

    def __init__(self, date):
        self.date = date
        self._value = WEEKDAY if date.weekday() < 5 else WEEKEND

    def set_holiday(self):
        self._value = HOLIDAY

    def __str__(self):
        return self._value


class DateArray(object):

    start_date = None
    end_date = None
    dates = []

    def __init__(self, start_date, end_date):
        self.start_date = start_date
        self.end_date = end_date
        self.dates = [ Day(start_date + datetime.timedelta(days=n)) for n in range((end_date - start_date).days + 1) ]

    def __contains__(self, item):
        if not isinstance(item, Day):
            return False
        return self.start_date <= item.date <= self.end_date

    def add_holiday(self, date_array):
        for date in self.dates:
            if date in date_array:
                date.set_holiday()

    def pretty_print(self):
        month = 0
        for date in self.dates:
            if date.date.month > month:
                print ''
                print '  ' * (date.date.weekday()),
                month = date.date.month
            print date,


if __name__ == '__main__':
    start_date = datetime.datetime(2019, 1, 1)
    end_date = datetime.datetime(2019, 12, 31)

    all_dates = DateArray(start_date, end_date)
    summer = DateArray(
        datetime.datetime(2019, 6, 1),
        datetime.datetime(2019, 6, 14),
    )
    all_dates.add_holiday(summer)

    all_dates.pretty_print()
