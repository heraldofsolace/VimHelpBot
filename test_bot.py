import unittest
from bot.bot import Bot


class TestBot(unittest.TestCase):
    def test_exact_match(self):
        """
        Test that it can find exact matches
        """

        bot = Bot()

        # TODO Add more tests
        tests = ["options", "E149", ":number", ":nu", "gj", "quickfix"]
        for t in tests:
            for subreddit in ["vim", "neovim"]:
                result = bot.search_tag(t, subreddit)
                self.assertEqual(len(result), 1)

    def test_non_exact_matches(self):
        """
        Test that it can find the best possible matches correctly
        """

        bot = Bot()

        # TODO Add more tests
        tests_vim = {"number": ":number", "usr_01.txt": "usr_01.txt",
                     "num": "+num64", "NUm": "Number", "Num": "Number",
                     "<_": "v_b_<_example", "hl": "'hl'", "\".": "quote.",
                     "\"=": "quote=", ":execute": ":execute", "/\<": "/\<"}
        for k, v in tests_vim.items():
            result = bot.search_tag(k)
            print(k, "=>", result)
            best_tag = next(iter(result.keys()))[1]
            self.assertEqual(best_tag, v)

        tests_nvim = {"num": ":number", "number": ":number", ":li": ":list",
                      "aba": "abandon", "_<": "v_<"}

        for k, v in tests_nvim.items():
            result = bot.search_tag(k, "neovim")
            print(k, "=>", result)
            best_tag = next(iter(result.keys()))[1]
            self.assertEqual(best_tag, v)

    def test_empty_comment(self):
        """
        Test comment is empty if nothing is found
        """
        bot = Bot()
        comment = "Test comment `:h nothingtoseehere`"

        reply = bot.create_comment(comment, "link", "vim")
        self.assertEqual(reply, '')

        reply = bot.create_comment(comment, "link", "neovim")
        self.assertEqual(reply, '')

    def test_normal_comment(self):
        """
        Test that bot can find everything
        """

        bot = Bot()
        tags = [":tab", ":options", ":tjump", "c_CTRL-R_CTRL-W",
                ":execute", "expand()", "<cword>"]

        text = "Test comment: " + \
            ','.join(list(map(lambda t: "`:h {}`".format(t), tags)))

        reply = bot.create_comment(text, "vim")
        self.assertNotEqual(reply, '')
        for tag in tags:
            self.assertIn(tag, reply)

        reply = bot.create_comment(text, "neovim")
        self.assertNotEqual(reply, '')
        for tag in tags:
            self.assertIn(tag, reply)


if __name__ == "__main__":
    unittest.main()
