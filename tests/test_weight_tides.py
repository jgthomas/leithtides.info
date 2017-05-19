

import unittest
import datetime as dt

from tide_response import weight_tides


class Test(unittest.TestCase):
    def test_first_not_day_second_closer(self):
        tide_times = [dt.datetime(1900, 1, 1, 2, 31), dt.datetime(1900, 1, 1, 15, 5)]
        now = dt.datetime(1900, 1, 1, 13, 58)
        self.assertEqual((0, 1), weight_tides(tide_times, now))

    def test_both_day_first_hour_ago(self):
        tide_times = [dt.datetime(1900, 1, 1, 12, 58), dt.datetime(1900, 1, 1, 21, 55)]
        now = dt.datetime(1900, 1, 1, 13, 58)
        self.assertEqual((1, 0), weight_tides(tide_times, now))

    def test_first_day_closer_over_two_hours_ago(self):
        tide_times = [dt.datetime(1900, 1, 1, 9, 58), dt.datetime(1900, 1, 1, 22, 55)]
        now = dt.datetime(1900, 1, 1, 14, 00)
        self.assertEqual((0, 1), weight_tides(tide_times, now))


if __name__ == '__main__':
    unittest.main()
