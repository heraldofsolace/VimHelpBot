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
        tests = {"usr_01.txt": "usr_01.txt", "num": "+num64", "NUm": "Number",
                "Num": "Number", "<_": "v_b_<_example", "hl": "'hl'", "\".": "quote.", "\"=": "quote=", ":execute": ":execute"}
        for k, v in tests.items():
            result = bot.search_tag(k)
            best_tag = next(iter(result.keys()))[1]
            self.assertEqual(best_tag, v)
    
    def test_empty_comment(self):
        """
        Test comment is empty if nothing is found
        """
        bot = Bot()
        comment = "Test comment `:h nothingtoseehere`"

        reply = bot.create_comment(comment)
        self.assertEqual(reply, '')

    def test_normal_comment(self):
        """
        Test that bot can find everything
        """

        bot = Bot()
        tags = [":tab", ":options", ":tjump", "c_CTRL-R_CTRL-W", ":execute", "expand()", "<cword>"]

        text = "Test comment: " + ','.join(list(map(lambda t: "`:h {}`".format(t), tags)))

        reply = bot.create_comment(text)
        self.assertNotEqual(reply, '')
        for tag in tags:
            self.assertIn(tag, reply)

if __name__ == "__main__":
    unittest.main()
