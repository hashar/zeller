#!/usr/bin/env python
# coding: utf8
"""
Zeller congruence

Usage:
    zeller.py
    zeller.py <YYYYmmdd>

Options:
    --help  This help message

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
        z = ZellerCongruence(date)

        if z.isJeudi():
            if z.m == 1 and z.q == 1:
                print "1er janvier c'est gueule de bois reviens le 8"
            elif z.q < 8 or (z.m == 1 and z.q == 8):
                print "First Jeudi!!!!!! 🍺 "
                return 0
            else:
                print "Mauvais Jeudi"
        else:
            print "Ce n'est pas un Jeudi"
        return 1


class ZellerCongruence(object):

    julian_end = datetime.date(1582, 10, 4)
    gregorian_start = datetime.date(1582, 10, 15)

    """day of the month"""
    q = None
    """month"""
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

    def __init__(self, date):
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

    @classmethod
    def fromdate(cls, date):
        algo = cls()
        algo.q = date.day

        # January -> 13
        if date.month == 1:
            algo.m = 13
        # Febuary -> 14
        elif date.month == 2:
            algo.m = 14
        else:
            algo.m = date.month

        algo.K = date.year % 100
        algo.J = date.year / 100
        return algo

    def execute(self):
        return (self._part1() + self._part2()) % 7

    def _part1(self):
        return self.q + (13 * (self.m + 1) / 5) + self.K + self.K / 4

    def _part2(self):
        raise NotImplemented()


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
    z = Zeller()
    exit(z.main(args['<YYYYmmdd>']))
