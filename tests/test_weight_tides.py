

import unittest
import datetime as dt

from leith_tides import weight_tides


class Test(unittest.TestCase):
    def test_first_not_day_second_closer(self):
        """
        Prefer: (closer to now, during day, upcoming unless past very recent)
        First is:
        not closer to now: 0
        not during day: 0
        not under two hours ago: 0
        score = 0

        Second is:
        closer to now: +1
        during day: +1 
        +3 as first over two hours ago
        score = 5
        """
        tide_times = [dt.datetime(1900, 1, 1, 2, 31), dt.datetime(1900, 1, 1, 15, 5)]
        now = dt.datetime(1900, 1, 1, 13, 58)
        self.assertEqual((0, 1), weight_tides(tide_times, now))

    def test_both_day_first_hour_ago(self):
        """ First (1, 1, 1); Second (0, 1, 0) """
        tide_times = [dt.datetime(1900, 1, 1, 12, 58), dt.datetime(1900, 1, 1, 21, 55)]
        now = dt.datetime(1900, 1, 1, 13, 58)
        self.assertEqual((1, 0), weight_tides(tide_times, now))

    def test_first_day_closer_over_two_hours_ago(self):
        """ First (1, 1, 0); Second (0, 0, 3) """
        tide_times = [dt.datetime(1900, 1, 1, 9, 58), dt.datetime(1900, 1, 1, 22, 55)]
        now = dt.datetime(1900, 1, 1, 14, 00)
        self.assertEqual((0, 1), weight_tides(tide_times, now))


if __name__ == '__main__':
    unittest.main()
