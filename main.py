import datetime
import copy

WEEKDAY = '.'
WEEKEND = 'S'
HOLIDAY = 'H'
SUGGEST = 'h'


ALLOWANCE = 25


class Day(object):

    date = None
    _value = 0

    def __init__(self, date):
        self.date = date
        self._value = WEEKDAY if date.weekday() < 5 else WEEKEND

    def set_holiday(self):
        self._value = HOLIDAY

    def set_suggestion(self):
        self._value = SUGGEST

    def is_holiday(self, include_suggestions=False):
        return self._value == HOLIDAY or (include_suggestions and self._value == SUGGEST)

    def is_workday(self):
        return self._value == WEEKDAY

    def __str__(self):
        return self._value


class DateArray(object):

    start_date = None
    end_date = None
    dates = []
    remaining_days = ALLOWANCE

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
                self.remaining_days -= 1

    def max_days_between_holidays(self, include_suggestions=False):
        _dates = copy.copy(self.dates)
        blocks = list()
        block = list()
        while _dates:
            date = _dates.pop(0)
            if not date.is_holiday(include_suggestions=include_suggestions):
                block.append(date)
            else:
                blocks.append(block)
                block = list()
        else:
            blocks.append(block)
        return max([len(b) for b in blocks])

    def add_sugestions(self):
        total_days = len( [d for d in self.dates if not d.is_holiday()] )
        distribution = float( total_days - self.remaining_days ) / self.remaining_days
        count = 0
        for date in self.dates:
            count += 1
            if date.is_holiday():
                count = 0
            if count > distribution and date.is_workday():
                date.set_suggestion()
                self.remaining_days -= 1
                count = 0

    def print_key(self):
        print 'Key:'
        the_key = {
            WEEKDAY: 'working day',
            WEEKEND: 'weekend',
            HOLIDAY: 'holiday',
            SUGGEST: 'suggested holiday',
        }
        for key, value in the_key.items():
            print '\t{key} = {meaning}'.format(key=key, meaning=value)

    def pretty_print(self):
        month = 0
        for date in self.dates:
            if date.date.month > month:
                print ''
                print '  ' * (date.date.weekday()),
                month = date.date.month
            print date,
        print ''
        print 'max days between holidays ignoring suggestions:', self.max_days_between_holidays()
        print 'max days between holidays with suggestions:', self.max_days_between_holidays(include_suggestions=True)
        print 'days leave not used (with suggestions):', self.remaining_days


if __name__ == '__main__':
    start_date = datetime.datetime(2019, 1, 1)
    end_date = datetime.datetime(2019, 12, 31)

    all_dates = DateArray(start_date, end_date)
    summer = DateArray(
        datetime.datetime(2019, 6, 1),
        datetime.datetime(2019, 6, 14),
    )
    all_dates.add_holiday(summer)

    all_dates.add_sugestions()
    all_dates.print_key()
    all_dates.pretty_print()
