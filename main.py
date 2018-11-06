import ConfigParser
import datetime
import copy

WEEKDAY = '.'
WEEKEND = 'S'
HOLIDAY = 'H'
SUGGEST = 'h'


class Day(object):
    ''' represents a date and stores it's holiday status '''

    date = None
    _value = 0

    def __init__(self, date):
        self.date = date
        self._value = WEEKDAY if date.weekday() < 5 else WEEKEND

    def set_holiday(self):
        ''' set this day as a holiday '''
        self._value = HOLIDAY

    def set_suggestion(self):
        ''' set this day as a suggested holiday '''
        self._value = SUGGEST

    def is_holiday(self, include_suggestions=False):
        ''' is this day a holiday '''
        return self._value == HOLIDAY or (include_suggestions and self.is_suggestion())

    def is_suggestion(self):
        ''' is this day a holiday '''
        return self._value == SUGGEST

    def is_workday(self):
        ''' is this day a working day? (not holiday or weekend) '''
        return self._value == WEEKDAY

    def __str__(self):
        return self._value


class DateArray(object):
    ''' a range of dates '''

    start_date = None
    end_date = None
    dates = []
    remaining_days = 0

    def __init__(self, start_date, end_date):
        self.start_date = start_date
        self.end_date = end_date
        self.dates = [ Day(start_date + datetime.timedelta(days=n)) for n in range((end_date - start_date).days + 1) ]
        self.remaining_days = ALLOWANCE

    def __contains__(self, item):
        if not isinstance(item, Day):
            return False
        return self.start_date <= item.date <= self.end_date

    def add_holiday(self, date_array):
        ''' date_array: DateArray

        add date_array as a holiday inside this DateArray but setting all days
        in the intersection as holiday days
        '''
        for date in self.dates:
            if date in date_array:
                if date.is_workday():
                    self.remaining_days -= 1
                date.set_holiday()

    def max_days_between_holidays(self, include_suggestions=False):
        ''' returns: int

        the maximum number of days between holidays in this DateArray. Weekend
        days are included so this number may be slightly misleading.
        '''
        #TODO weekends that touch holidays should be marked as holidays
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

    def add_sugestions_naive(self):
        '''add suggestions inplace by setting work days to suggestions at evan
        intervals throughout the year around holidays. Note that if it falls on
        a weekend it is moved to the following monday'''

        if self.remaining_days <= 0:
            return

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

    def add_sugestions(self):
        ''' distribute days evenly over working days '''

        all_working_days = [d for d in self.dates if d.is_workday()]
        # take floor
        partition_size = int(len(all_working_days) / self.remaining_days)
        for i in range(partition_size,len(all_working_days), partition_size):
            all_working_days[i].set_suggestion()
            self.remaining_days -= 1

    def print_key(self):
        ''' print the key of the pretty_print '''
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
        ''' print this DateArray with each new line being a month, aligning
        weekends '''
        print ''
        print ' ' * 4, 'M T W T F S S ' * 5,
        month = 0
        for date in self.dates:
            if date.date.month > month:
                print '\n%s' % date.date.strftime('%b'),
                print '  ' * (date.date.weekday()),
                month = date.date.month
            print date,
        print '\n'
        print 'max days between holidays ignoring suggestions:', self.max_days_between_holidays()
        print 'max days between holidays with suggestions:', self.max_days_between_holidays(include_suggestions=True)
        print 'suggested dates:'
        suggestions = [ d for d in self.dates if d.is_suggestion() ]
        for i, s in enumerate(suggestions):
            print '\t%2s.' % (i+1), s.date.strftime(DATE_FORMAT)


def _parse_date_array(config, name):
    '''
        config: RawConfigParser
        name: section name to parse
        returns: DateArray
    '''
    start_date = config.get(name, 'start_date')
    end_date = config.get(name, 'end_date')
    start_date = datetime.datetime.strptime(start_date, DATE_FORMAT)
    end_date = datetime.datetime.strptime(end_date, DATE_FORMAT)
    return DateArray(start_date, end_date)


def parse_config(filename):
    '''
        filename: str - a filename to read config from
        returns: DateArray
    '''
    global DATE_FORMAT
    global ALLOWANCE

    config = ConfigParser.RawConfigParser()
    config.read(filename)

    DATE_FORMAT = config.get('Global', 'DATE_FORMAT')
    ALLOWANCE = config.getint('Global', 'ALLOWANCE')

    all_dates = _parse_date_array( config, 'DateArray' )

    holidays = [ s for s in config.sections() if s.lower().startswith('holiday')]
    for h in holidays:
        holiday = _parse_date_array( config, h)
        all_dates.add_holiday( holiday )

    return all_dates


if __name__ == '__main__':
    all_dates = parse_config('holidays.cfg')

    all_dates.add_sugestions()
    all_dates.print_key()
    all_dates.pretty_print()
