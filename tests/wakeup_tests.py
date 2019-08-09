import unittest
import os
import wakeup.config as config
from wakeup.errors import InvalidScheduleError
from wakeup.schedule import Schedule, parse_schedule

schedule_0630_daily = Schedule(6, 30)
schedule_0630_mon = Schedule(6, 30, {"mon"})
schedule_1330_daily = Schedule(13, 30)
schedule_0630_mon_tues_fri = Schedule(6, 30, {"mon", "tue", "fri"})


class WakeupTests(unittest.TestCase):
    def setUp(self):
        self.opts_without_optional = {
            config.CONSUMER_KEY: "ck",
            config.CONSUMER_SECRET: "cs",
            config.ACCESS_TOKEN_KEY: "atk",
            config.ACCESS_TOKEN_SECRET: "ats",
        }
        self.opts_all_fields = {
            config.CONSUMER_KEY: "ck",
            config.CONSUMER_SECRET: "cs",
            config.ACCESS_TOKEN_KEY: "atk",
            config.ACCESS_TOKEN_SECRET: "ats",
            config.USER_ACTIVITY_TIMEOUT: 15,
        }
        self.opts_missing_cs = {
            config.CONSUMER_KEY: "ck",
            # config.CS: 'cs',
            config.ACCESS_TOKEN_KEY: "atk",
            config.ACCESS_TOKEN_SECRET: "ats",
            config.USER_ACTIVITY_TIMEOUT: 15,
        }
        self.opts_missing_ck = {
            # config.CK: 'ck',
            config.CONSUMER_SECRET: "cs",
            config.ACCESS_TOKEN_KEY: "atk",
            config.ACCESS_TOKEN_SECRET: "ats",
            config.USER_ACTIVITY_TIMEOUT: 15,
        }
        self.opts_missing_atk = {
            config.CONSUMER_KEY: "ck",
            config.CONSUMER_SECRET: "cs",
            # config.ATK: 'atk',
            config.ACCESS_TOKEN_SECRET: "ats",
            config.USER_ACTIVITY_TIMEOUT: 15,
        }
        self.opts_missing_ats = {
            config.CONSUMER_KEY: "ck",
            config.CONSUMER_SECRET: "cs",
            config.ACCESS_TOKEN_KEY: "atk",
            # config.ATS: 'ats',
            config.USER_ACTIVITY_TIMEOUT: 15,
        }

    def test_config_default_values(self):
        opts = {}
        config.load_defaults(opts)
        self.assertEqual(60, opts[config.USER_ACTIVITY_TIMEOUT])
        config.load_defaults(self.opts_without_optional)
        self.assertEqual(60, self.opts_without_optional[config.USER_ACTIVITY_TIMEOUT])
        self.assertTrue(config.TWEET_TEXT in self.opts_without_optional)

    def test_verify_required_fields_set(self):
        self.assertFalse(config.is_valid({}))
        self.assertTrue(config.is_valid(self.opts_without_optional))
        self.assertTrue(config.is_valid(self.opts_all_fields))
        self.assertFalse(config.is_valid(self.opts_missing_cs))
        self.assertFalse(config.is_valid(self.opts_missing_ck))
        self.assertFalse(config.is_valid(self.opts_missing_atk))
        self.assertFalse(config.is_valid(self.opts_missing_ats))

    def test_parse_daily_schedule(self):
        schedule = parse_schedule("6:30am")
        self.assertEqual(schedule_0630_daily, schedule)

    def test_parse_schedule_military_time(self):
        schedule = parse_schedule("6:30")
        self.assertEqual(schedule_0630_daily, schedule)

        pm_schedule = parse_schedule("13:30")
        self.assertEqual(schedule_1330_daily, pm_schedule)

    def test_schedule_equality(self):
        s1 = Schedule(5, 30)
        s2 = Schedule(5, 30)
        self.assertEqual(s1, s2)
        # Hours are different
        s3 = Schedule(6, 30)
        self.assertNotEqual(s1, s3)
        # Minutes are different
        s4 = Schedule(5, 45)
        self.assertNotEqual(s1, s4)
        # Days of week are different
        s5 = Schedule(5, 30, {"mon"})
        self.assertNotEqual(s1, s5)

    def test_parse_schedule_pm(self):
        s = parse_schedule("1:30pm")
        self.assertEqual(schedule_1330_daily, s)

    def test_parse_schedule_ignore_case_of_period(self):
        s1 = parse_schedule("1:30PM")
        s2 = parse_schedule("1:30pm")
        self.assertEqual(s1, s2)

    def test_parse_schedule_one_weekday(self):
        s = parse_schedule("6:30am mon")
        self.assertEqual(schedule_0630_mon, s)

    def test_parse_schedule_multiple_weekdays(self):
        s = parse_schedule("6:30am mon,tue,fri")
        self.assertEqual(schedule_0630_mon_tues_fri, s)

    def test_parse_schedule_partial_time_raises_error(self):
        with self.assertRaises(InvalidScheduleError):
            parse_schedule("6")

    def test_parse_schedule_non_numeric_time_raises_error(self):
        with self.assertRaises(InvalidScheduleError):
            parse_schedule("6:ab")
        with self.assertRaises(InvalidScheduleError):
            parse_schedule("a:30")

    def test_parse_schedule_invalid_day_raises_error(self):
        with self.assertRaises(InvalidScheduleError):
            parse_schedule("6:30 mon,feus,wed")

    def test_parse_schedule_hour_out_of_range_raises_error(self):
        with self.assertRaises(InvalidScheduleError):
            parse_schedule("24:30")

    def test_parse_schedule_hour_out_of_range_raises_error(self):
        with self.assertRaises(InvalidScheduleError):
            parse_schedule("6:70")
