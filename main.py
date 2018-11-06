import ConfigParser
import datetime
import copy
import math

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

    def __init__(self, dates=None, start_date=None, end_date=None, allowance=None):
        if dates is not None:
            self.dates = dates
        elif start_date is not None and end_date is not None:
            self.dates = [ Day(start_date + datetime.timedelta(days=n)) for n in range((end_date - start_date).days + 1) ]
        else:
            raise TypeError('invalid DateArray')

        if allowance is None:
            self.remaining_days = ALLOWANCE
        else:
            self.remaining_days = allowance

    def __contains__(self, item):
        if not isinstance(item, Day):
            return False
        return item.date in [d.date for d in self.dates]

    def __iter__(self):
        return iter(self.dates)

    def __len__(self):
        return len(self.dates)

    def __getitem__(self, i):
        return self.dates[i]

    def __setitem__(self, i, item):
        self.dates[i] = item

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

    def add_sugestions_iter(self):
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

    def add_sugestions_naive(self):
        ''' distribute days evenly over working days. Ignores where holidays
        are but guarenteed to use all days '''

        all_working_days = [d for d in self.dates if d.is_workday()]
        num_working_days = len(all_working_days)
        # take floor
        partition_size = int(num_working_days / self.remaining_days)
        remainder = num_working_days - (partition_size * self.remaining_days)
        while remainder + self.remaining_days < partition_size:
            partition_size -= 1
            remainder = num_working_days - (partition_size * self.remaining_days)
        for i in range(partition_size, num_working_days, partition_size):
            all_working_days[i].set_suggestion()
            self.remaining_days -= 1

    def add_sugestions_partitions(self):
        ''' add suggestions by partitioning working days by holidays '''

        # determine min possible partition size
        all_working_days = [d for d in self.dates if d.is_workday()]
        num_working_days = len(all_working_days)
        num_partitions = self.remaining_days
        # take floor
        max_partition_size = int(num_working_days / num_partitions)

        # break year into partitions by holidays
        partitions = list()
        partition = list()
        for date in self.dates:
            if date.is_holiday():
                if partition:
                    allowance = int(len(partition)/max_partition_size)
                    array = DateArray(dates=partition, allowance=allowance)
                    partitions.append(array)
                    partition = list()
            elif date.is_workday():
                partition.append(date)

        days_remainder = self.remaining_days - sum(d.remaining_days for d in partitions)

        # if any days left ofter, put in the largest partition
        if days_remainder > 0:
            _max = partitions[0]
            for p in partitions:
                if len(p) > len(_max):
                    _max = p
            _max.remaining_days += days_remainder

        # recurse
        for p in partitions:
            p.add_sugestions_naive()

    def add_sugestions(self):
        self.add_sugestions_partitions()

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


def _parse_date_array(config, name, allowance=0):
    '''
        config: RawConfigParser
        name: section name to parse
        returns: DateArray
    '''
    start_date = config.get(name, 'start_date')
    end_date = config.get(name, 'end_date')
    start_date = datetime.datetime.strptime(start_date, DATE_FORMAT)
    end_date = datetime.datetime.strptime(end_date, DATE_FORMAT)
    return DateArray(start_date=start_date, end_date=end_date, allowance=allowance)


def parse_config(filename):
    '''
        filename: str - a filename to read config from
        returns: DateArray
    '''
    global DATE_FORMAT

    config = ConfigParser.RawConfigParser()
    config.read(filename)

    DATE_FORMAT = config.get('Global', 'DATE_FORMAT')
    allowance = config.getint('Global', 'ALLOWANCE')

    all_dates = _parse_date_array( config, 'DateArray', allowance=allowance )

    holidays = [ s for s in config.sections() if s.lower().startswith('holiday')]
    for h in holidays:
        holiday = _parse_date_array( config, h )
        all_dates.add_holiday( holiday )

    return all_dates


if __name__ == '__main__':
    all_dates = parse_config('holidays.cfg')

    all_dates.add_sugestions()
    all_dates.print_key()
    all_dates.pretty_print()
