

import unittest
import datetime as dt

from tide_response import tide_message


class Test(unittest.TestCase):
    def test_one_low_tide(self):
        low_tides = [dt.datetime(1900, 1, 1, 2, 31)]
        high_tides = [dt.datetime(1900, 1, 1, 8, 31), dt.datetime(1900, 1, 1, 20, 5)]
        tides = [low_tides, high_tides]
        now = dt.datetime(1900, 1, 1, 13, 58)
        output = 'Low tide in leith was at 02:31. High tide will be at 20:05'
        self.assertEqual(output, tide_message(tides, now=now))

    def test_both_only_one(self):
        low_tides = [dt.datetime(1900, 1, 1, 2, 31)]
        high_tides = [dt.datetime(1900, 1, 1, 20, 5)]
        tides = [low_tides, high_tides]
        now = dt.datetime(1900, 1, 1, 13, 58)
        output = 'Low tide in leith was at 02:31. High tide will be at 20:05'
        self.assertEqual(output, tide_message(tides, now=now))

    def test_first_low_upcoming_first_high_well_past(self):
        low_tides = [dt.datetime(1900, 1, 1, 16, 31), dt.datetime(1900, 1, 1, 23, 51)]
        high_tides = [dt.datetime(1900, 1, 1, 2, 31), dt.datetime(1900, 1, 1, 20, 5)]
        tides = [low_tides, high_tides]
        now = dt.datetime(1900, 1, 1, 13, 58)
        output = 'Low tide in leith will be at 16:31. High tide will be at 20:05'
        self.assertEqual(output, tide_message(tides, now=now))

    def test_both_first_well_past(self):
        low_tides = [dt.datetime(1900, 1, 1, 2, 31), dt.datetime(1900, 1, 1, 14, 51)]
        high_tides = [dt.datetime(1900, 1, 1, 8, 31), dt.datetime(1900, 1, 1, 20, 5)]
        tides = [low_tides, high_tides]
        now = dt.datetime(1900, 1, 1, 13, 58)
        output = 'Low tide in leith will be at 14:51. High tide will be at 20:05'
        self.assertEqual(output, tide_message(tides, now=now))

    def test_both_first_upcoming(self):
        low_tides = [dt.datetime(1900, 1, 1, 14, 31), dt.datetime(1900, 1, 1, 22, 51)]
        high_tides = [dt.datetime(1900, 1, 1, 18, 31), dt.datetime(1900, 1, 1, 23, 5)]
        tides = [low_tides, high_tides]
        now = dt.datetime(1900, 1, 1, 13, 58)
        output = 'Low tide in leith will be at 14:31. High tide will be at 18:31'
        self.assertEqual(output, tide_message(tides, now=now))

    def test_all_times_well_past(self):
        low_tides = [dt.datetime(1900, 1, 1, 4, 31), dt.datetime(1900, 1, 1, 20, 51)]
        high_tides = [dt.datetime(1900, 1, 1, 8, 31), dt.datetime(1900, 1, 1, 19, 5)]
        tides = [low_tides, high_tides]
        now = dt.datetime(1900, 1, 1, 23, 58)
        output = 'Low tide in leith was at 20:51. High tide was at 19:05'
        self.assertEqual(output, tide_message(tides, now=now))

    def test_low_tide_only_past(self):
        low_tides = [dt.datetime(1900, 1, 1, 4, 31), dt.datetime(1900, 1, 1, 20, 51)]
        now = dt.datetime(1900, 1, 1, 23, 58)
        output = 'Low tide in leith was at 20:51'
        self.assertEqual(output, tide_message(low_tides, specific_tide="low", now=now))

    def test_low_tide_only_future(self):
        low_tides = [dt.datetime(1900, 1, 1, 16, 31), dt.datetime(1900, 1, 1, 23, 51)]
        now = dt.datetime(1900, 1, 1, 13, 58)
        output = 'Low tide in leith will be at 16:31'
        self.assertEqual(output, tide_message(low_tides, specific_tide="low", now=now))

    def test_low_tide_only_just_one(self):
        low_tides = [dt.datetime(1900, 1, 1, 2, 31)]
        now = dt.datetime(1900, 1, 1, 13, 58)
        output = 'Low tide in leith was at 02:31'
        self.assertEqual(output, tide_message(low_tides, specific_tide="low", now=now))

    def test_high_tide_only_past(self):
        high_tides = [dt.datetime(1900, 1, 1, 8, 31), dt.datetime(1900, 1, 1, 19, 5)]
        now = dt.datetime(1900, 1, 1, 23, 58)
        output = 'High tide in leith was at 19:05'
        self.assertEqual(output, tide_message(high_tides, specific_tide="high", now=now))

    def test_high_tide_only_future(self):
        high_tides = [dt.datetime(1900, 1, 1, 18, 31), dt.datetime(1900, 1, 1, 23, 5)]
        now = dt.datetime(1900, 1, 1, 13, 58)
        output = 'High tide in leith will be at 18:31'
        self.assertEqual(output, tide_message(high_tides, specific_tide="high", now=now))

    def test_high_tide_only_just_one(self):
        high_tides = [dt.datetime(1900, 1, 1, 20, 5)]
        now = dt.datetime(1900, 1, 1, 13, 58)
        output = 'High tide in leith will be at 20:05'
        self.assertEqual(output, tide_message(high_tides, specific_tide="high", now=now))


if __name__ == '__main__':
    unittest.main()
