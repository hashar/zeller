#!/usr/bin/env python
# coding: utf8
"""
Zeller congruence

Usage:
    zeller.py [--country CODE]
    zeller.py [--country CODE] <YYYYmmdd>

Options:
    --help     This help message
    --country CODE  Country code to determine switch from Julian to
                    Gregorian. Default: Papal States

Exit codes:
    0: for a FirstJeudi
    1: otherwise
"""

import datetime
from time import strptime
from sys import exit

from docopt import docopt


class Zeller(object):

    date = None
    country = None

    def __init__(self, country=None):
        self.country = country

    @staticmethod
    def parse_date(string):
        parsed = strptime(string, '%Y%m%d')
        return datetime.date(parsed.tm_year, parsed.tm_mon,
                             parsed.tm_mday)

    def main(self, input_date):
        if input_date is None:
            date = datetime.date.today()
        else:
            date = self.parse_date(input_date)

        z = ZellerCongruence(date, *CalLimits.forCountry(self.country))

        if z.isJeudi():
            if z.algo.m == 13 and z.algo.q == 1:
                print "1er janvier c'est gueule de bois reviens le 8"
            elif z.algo.q < 8 or (z.algo.m == 13 and z.algo.q == 8):
                print "First Jeudi!!!!!! 🍺 "
                return 0
            else:
                print "Mauvais Jeudi"
        else:
            print "Ce n'est pas un Jeudi mais un %s" % z.getName()
        return 1


class ZellerCongruence(object):

    """Day of the month"""
    q = None
    """Month (3: march to 14: february)"""
    m = None
    """year of century"""
    K = None
    """Zero based century"""
    J = None

    days_of_week = (
        'Samedi',
        'Dimanche',
        'Lundi',
        'Mardi',
        'Mercredi',
        'Jeudi',
        'Vendredi',
    )

    def __init__(self, date, julian_end=None, gregorian_start=None):
        self.julian_end = julian_end or datetime.date(1582, 10, 4)
        self.gregorian_start = gregorian_start or datetime.date(1582, 10, 15)

        if date <= self.julian_end:
            self.algo = Julian.fromdate(date)
        elif date >= self.gregorian_start:
            self.algo = Gregorian.fromdate(date)
        else:
            raise Exception('Date %s is neither Julian nor Gregorian' % date)
        self.day_num = self.algo.execute()

        assert -2 % 7 == 5

    def isJeudi(self):
        return True if self.days_of_week[self.day_num] == 'Jeudi' else False

    def getName(self):
        return self.days_of_week[self.day_num]

    @classmethod
    def fromdate(cls, date):
        algo = cls()
        algo.q = date.day

        # January -> 13
        if date.month == 1:
            algo.m = 13
        # February -> 14
        elif date.month == 2:
            algo.m = 14
        else:
            algo.m = date.month

        if algo.m > 12:
            year = date.year - 1
        else:
            year = date.year

        algo.K = year % 100
        algo.J = year / 100
        return algo

    def execute(self):
        return (self._part1() + self._part2()) % 7

    def _part1(self):
        return self.q + (13 * (self.m + 1) / 5) + self.K + self.K / 4

    def _part2(self):
        raise NotImplemented()


class CalLimits(object):

    # Adjustement length depends on the century
    country_dates = {
        # XXX
        # Alsace: 1648
        # Strasbourg: 1682
        # Lorraine: 1582-1735 (yeah they have been slow)
        'fr': ((1582, 12, 9), (1582, 12, 20)),
        'uk': ((1752, 9, 2), (1752, 9, 14)),
        'ie': ((1752, 9, 2), (1752, 9, 14)),
    }

    default_julian_end = (1582, 10, 4)
    default_gregorian_start = (1582, 10, 15)

    @staticmethod
    def forCountry(country=None):
        limits = CalLimits.country_dates.get(
            country,
            (CalLimits.default_julian_end,
             CalLimits.default_gregorian_start)
        )
        return [datetime.date(*d) for d in limits]


class Gregorian(ZellerCongruence):

    def __init__(self):
        pass

    def _part2(self):
        return self.J / 4 - 2 * self.J


class Julian(ZellerCongruence):

    def __init__(self):
        pass

    def _part2(self):
        return 5 - self.J


if __name__ == '__main__':
    args = docopt(__doc__)
    z = Zeller(country=args['--country'])

    exit(z.main(args['<YYYYmmdd>']))
