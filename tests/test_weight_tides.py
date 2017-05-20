

import unittest
import datetime as dt

from tide_response import weight_tides


class Test(unittest.TestCase):
    def test_first_long_past(self):
        tide_times = [dt.datetime(1900, 1, 1, 2, 31), dt.datetime(1900, 1, 1, 15, 5)]
        now = dt.datetime(1900, 1, 1, 13, 58)
        self.assertEqual((0, 1), weight_tides(tide_times, now))

    def test_first_hour_ago(self):
        tide_times = [dt.datetime(1900, 1, 1, 12, 58), dt.datetime(1900, 1, 1, 21, 55)]
        now = dt.datetime(1900, 1, 1, 13, 58)
        self.assertEqual((1, 0), weight_tides(tide_times, now))

    def test_first_over_two_hours_ago(self):
        tide_times = [dt.datetime(1900, 1, 1, 9, 58), dt.datetime(1900, 1, 1, 22, 55)]
        now = dt.datetime(1900, 1, 1, 13, 58)
        self.assertEqual((0, 1), weight_tides(tide_times, now))
        
    def test_first_in_future_long(self):
        tide_times = [dt.datetime(1900, 1, 1, 19, 58), dt.datetime(1900, 1, 1, 22, 55)]
        now = dt.datetime(1900, 1, 1, 13, 58)
        self.assertEqual((1, 0), weight_tides(tide_times, now))

    def test_first_in_future_very_close(self):
        tide_times = [dt.datetime(1900, 1, 1, 13, 59), dt.datetime(1900, 1, 1, 22, 55)]
        now = dt.datetime(1900, 1, 1, 13, 58)
        self.assertEqual((1, 0), weight_tides(tide_times, now))

    def test_first_now(self):
        tide_times = [dt.datetime(1900, 1, 1, 13, 58), dt.datetime(1900, 1, 1, 22, 55)]
        now = dt.datetime(1900, 1, 1, 13, 58)
        self.assertEqual((1, 0), weight_tides(tide_times, now))

    def test_second_in_past(self):
        tide_times = [dt.datetime(1900, 1, 1, 1, 58), dt.datetime(1900, 1, 1, 12, 55)]
        now = dt.datetime(1900, 1, 1, 13, 58)
        self.assertEqual((0, 1), weight_tides(tide_times, now))

    def test_second_long_past(self):
        tide_times = [dt.datetime(1900, 1, 1, 1, 58), dt.datetime(1900, 1, 1, 2, 55)]
        now = dt.datetime(1900, 1, 1, 13, 58)
        self.assertEqual((0, 1), weight_tides(tide_times, now))


if __name__ == '__main__':
    unittest.main()
