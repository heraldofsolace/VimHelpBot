import unittest
from bot.bot import Bot


class TestBot(unittest.TestCase):
    def test_exact_match(self):
        """
        Test that it can find exact matches
        """

        bot = Bot()

        # TODO Add more tests
        tests = ["options", "E149", ":number", ":nu", "gj"]
        for t in tests:
            result = bot.search_tag(t)
            self.assertEqual(len(result), 1)

    def test_non_exact_matches(self):
        """
        Test that it can find the best possible matches correctly
        """

        bot = Bot()

        # TODO Add more tests
        tests = {"num": "+num64", "Num": "Number", "<_": "v_b_<_example", "hl": "'hl'"}
        for k, v in tests.items():
            result = bot.search_tag(k)
            best_tag = next(iter(result.keys()))[1]
            self.assertEqual(best_tag, v)


if __name__ == "__main__":
    unittest.main()
