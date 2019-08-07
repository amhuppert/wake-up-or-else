import unittest
import os
import wakeup.config as config

class WakeupTests(unittest.TestCase):


    def setUp(self):
        self.opts_without_optional = {
            config.CONSUMER_KEY: 'ck',
            config.CONSUMER_SECRET: 'cs',
            config.ACCESS_TOKEN_KEY: 'atk',
            config.ACCESS_TOKEN_SECRET: 'ats'
            }
        self.opts_all_fields = {
            config.CONSUMER_KEY: 'ck',
            config.CONSUMER_SECRET: 'cs',
            config.ACCESS_TOKEN_KEY: 'atk',
            config.ACCESS_TOKEN_SECRET: 'ats',
            config.UTA: 15
            }
        self.opts_missing_cs = {
            config.CONSUMER_KEY: 'ck',
            # config.CS: 'cs',
            config.ACCESS_TOKEN_KEY: 'atk',
            config.ACCESS_TOKEN_SECRET: 'ats',
            config.UTA: 15
            }
        self.opts_missing_ck = {
            # config.CK: 'ck',
            config.CONSUMER_SECRET: 'cs',
            config.ACCESS_TOKEN_KEY: 'atk',
            config.ACCESS_TOKEN_SECRET: 'ats',
            config.UTA: 15
            }
        self.opts_missing_atk = {
            config.CONSUMER_KEY: 'ck',
            config.CONSUMER_SECRET: 'cs',
            # config.ATK: 'atk',
            config.ACCESS_TOKEN_SECRET: 'ats',
            config.UTA: 15
            }
        self.opts_missing_ats = {
            config.CONSUMER_KEY: 'ck',
            config.CONSUMER_SECRET: 'cs',
            config.ACCESS_TOKEN_KEY: 'atk',
            # config.ATS: 'ats',
            config.UTA: 15
            }

    def test_config_default_values(self):
        opts = {}
        config.load_defaults(opts)
        self.assertEqual(60, opts[config.UTA])
        config.load_defaults(self.opts_without_optional)
        self.assertEqual(60, self.opts_without_optional[config.UTA])
        self.assertTrue(config.TWEET_TEXT in self.opts_without_optional)

    def test_verify_required_fields_set(self):
        self.assertFalse(config.is_valid({}))
        self.assertTrue(config.is_valid(self.opts_without_optional))
        self.assertTrue(config.is_valid(self.opts_all_fields))
        self.assertFalse(config.is_valid(self.opts_missing_cs))
        self.assertFalse(config.is_valid(self.opts_missing_ck))
        self.assertFalse(config.is_valid(self.opts_missing_atk))
        self.assertFalse(config.is_valid(self.opts_missing_ats))
