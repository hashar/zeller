#!/usr/bin/env python
# coding: utf8

import unittest
import datetime
import sys

import zeller

parse_date = zeller.Zeller.parse_date


def congruence(date_string):
    return zeller.ZellerCongruence(parse_date(date_string))


class FakeCalendar(zeller.ZellerCongruence):

    def __init__(self):
        pass


class TestZellerCongruence(unittest.TestCase):

    # Assertions helpers

    def assertIsJulian(self, z):
        self.assertIsInstance(z.algo, zeller.Julian)

    def assertIsGregorian(self, z):
        self.assertIsInstance(z.algo, zeller.Gregorian)

    # Tests

    def test_julian_date(self):
        # Début de la bataille de Marignan
        self.assertIsJulian(congruence('15150913'))

    def test_gregorian_date(self):
        self.assertIsGregorian(congruence('20150101'))

    def test_julian_last_day(self):
        self.assertIsJulian(congruence('15821004'))

    def test_gregorian_first_day(self):
        self.assertIsGregorian(congruence('15821015'))

    def test_inter_gravissimas_begin(self):
        with self.assertRaises(Exception):
            self.assertIsGregorian(congruence('15821005'))

    def test_inter_gravissimas_end(self):
        with self.assertRaises(Exception):
            self.assertIsGregorian(congruence('15821014'))

    # ZellerCongruence.fromdate()

    def test_fromdate_now(self):
        c = FakeCalendar.fromdate(datetime.date(2015, 9, 3))
        self.assertEquals(
            (3, 9, 15, 20),
            (c.q, c.m, c.K, c.J)
        )

    def test_fromdate_january(self):
        c = FakeCalendar.fromdate(datetime.date(2015, 1, 1))
        self.assertEquals(
            (1, 13, 14, 20),
            (c.q, c.m, c.K, c.J)
        )

    def test_fromdate_february(self):
        c = FakeCalendar.fromdate(datetime.date(2015, 2, 1))
        self.assertEquals(
            (1, 14, 14, 20),
            (c.q, c.m, c.K, c.J)
        )

    def test_from_date_jan_1_2000(self):
        c = FakeCalendar.fromdate(datetime.date(2000, 1, 1))
        self.assertEquals(
            (1, 13, 99, 19),
            (c.q, c.m, c.K, c.J)
        )

    def test_from_date_mar_1_2000(self):
        c = FakeCalendar.fromdate(datetime.date(2000, 3, 1))
        self.assertEquals(
            (1, 3, 0, 20),
            (c.q, c.m, c.K, c.J)
        )

    def test_from_date_mar_1_2015(self):
        c = FakeCalendar.fromdate(datetime.date(2000, 3, 15))
        self.assertEquals(
            (15, 3, 0, 20),
            (c.q, c.m, c.K, c.J)
        )

    # Test the actual algorithm result

    # Year 2015
    def test_sep_3_2015_is_jeudi(self):
        self.assertEquals('Jeudi', congruence('20150903').getName())

    def test_sep_1_2015_is_mardi(self):
        self.assertEquals('Mardi', congruence('20150901').getName())

    def test_mar_1_2015_is_dimanche(self):
        self.assertEquals('Dimanche', congruence('20150301').getName())

    def test_jan_1_2015_is_mardi(self):
        self.assertEquals('Jeudi', congruence('20150101').getName())

    # Year 2000

    def test_jan_1_2000_is_samedi(self):
        self.assertEquals('Samedi', congruence('20000101').getName())

    def test_mar_1_2000_is_mercredi(self):
        self.assertEquals('Mercredi', congruence('20000301').getName())

    # Julian era
    def test_sep_13_1515_is_jeudi(self):
        self.assertEquals('Jeudi', congruence('15150913').getName())

    def test_inter_gravissimas_last_julian_is_jeudi(self):
        self.assertEquals('Jeudi', congruence('15821004').getName())

    def test_inter_gravissimas_first_gregorian_is_friday(self):
        self.assertEquals('Vendredi', congruence('15821015').getName())


class TestZellerCommand(unittest.TestCase):

    def test_today(self):
        self.assertEquals(0, zeller.Zeller().main('20150903'))
        out = sys.stdout.getvalue().strip()
        self.assertEquals(out, 'First Jeudi!!!!!! 🍺')

    def test_next_jeudi(self):
        self.assertEquals(1, zeller.Zeller().main('20150910'))
        out = sys.stdout.getvalue().strip()
        self.assertEquals(out, 'Mauvais Jeudi')

    def test_january_first(self):
        self.assertEquals(1, zeller.Zeller().main('20150101'))
        out = sys.stdout.getvalue().strip()
        self.assertEquals(out,
                          '1er janvier c\'est gueule de bois reviens le 8')

    def test_january_postponed(self):
        self.assertEquals(0, zeller.Zeller().main('20150108'))
        out = sys.stdout.getvalue().strip()
        self.assertEquals(out, 'First Jeudi!!!!!! 🍺')


if __name__ == '__main__':
    print "testing"
    unittest.main(buffer=True)
