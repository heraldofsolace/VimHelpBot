import unittest
from bot.bot import Bot


class TestBot(unittest.TestCase):
    def test_exact_match(self):
        """
        Test that it can find exact matches
        """

        bot = Bot()

        # TODO Add more tests
        tests = ["options", "E149", ":number", ":nu", "gj", "quickfix", "%:.", "o_v", "gh", "index"]
        for t in tests:
            for subreddit in ["vim", "neovim"]:
                result = bot.search_tag(t, subreddit)
                print(result)
                self.assertEqual(len(result), 1)
                self.assertEqual(list(result.keys())[0][1], t)

    def test_non_exact_matches(self):
        """
        Test that it can find the best possible matches correctly
        """

        bot = Bot()

        # TODO Add more tests
        tests_vim = {"number": ":number", "usr_01.txt": "usr_01.txt", "num": "+num64", "NUm": "Number",
                "Num": "Number", "<_": "v_b_<_example", "hl": "'hl'", "\".": "quote.", "\"=": "quote=", ":execute": ":execute", "%": "%", "/\\<": "/\\<"}
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

        reply = bot.create_comment(comment, None, "vim")
        self.assertEqual(reply, '')

        reply = bot.create_comment(comment, None, "neovim")
        self.assertEqual(reply, '')

    def test_backtick_comment(self):
        """
        Test that bot can find all backtick-style queries
        """

        bot = Bot()
        tags = [":tab", ":options", ":tjump", "c_CTRL-R_CTRL-W",
                ":execute", "expand()"]

        text = "Test comment: " + \
            ','.join(list(map(lambda t: "`:h {}`".format(t), tags)))

        reply = bot.create_comment(text, None, "vim")
        self.assertNotEqual(reply, '')
        for tag in tags:
            self.assertIn(tag, reply)

        reply = bot.create_comment(text, None, "neovim")
        self.assertNotEqual(reply, '')
        for tag in tags:
            self.assertIn(tag, reply)
    
    def test_double_backtick_comment(self):
        """
        Test that bot can find all backtick-style queries
        """

        bot = Bot()
        tags = [":tab", ":options", ":tjump", "c_CTRL-R_CTRL-W",
                ":execute", "expand()"]

        text = "Test comment: " + \
            ','.join(list(map(lambda t: "``:h {}``".format(t), tags)))

        reply = bot.create_comment(text, None, "vim")
        self.assertNotEqual(reply, '')
        for tag in tags:
            self.assertIn(tag, reply)

        reply = bot.create_comment(text, None, "neovim")
        self.assertNotEqual(reply, '')
        for tag in tags:
            self.assertIn(tag, reply)

    def test_space_comment(self):
        """
        Test that bot can find all space-style queries
        """

        bot = Bot()
        tags = [":tab", ":options", ":tjump", "c_CTRL-R_CTRL-W",
                ":execute", "expand()"]

        text = "Test comment: " + \
            ' '.join(list(map(lambda t: ":h {}".format(t), tags)))

        reply = bot.create_comment(text, None, "vim")
        self.assertNotEqual(reply, '')
        for tag in tags:
            self.assertIn(tag, reply)

        reply = bot.create_comment(text, None, "neovim")
        self.assertNotEqual(reply, '')
        for tag in tags:
            self.assertIn(tag, reply)


    def test_mixed_style_comment(self):
        """
        Test that bot can find all backtick-
        and space- style queries when mixed
        """

        bot = Bot()
        backtick_tags = [":,", "'formatlistpat'", "augroup"]
        space_tags = ["l:var", "substitute()", "'updatetime'"]
        text = "Test comment: " + \
            ','.join(list(map(lambda t: "`:h {}`".format(t), backtick_tags))) + \
            '\n' + \
            ' '.join(list(map(lambda t: ":h {}".format(t), space_tags)))

        reply = bot.create_comment(text, None, "vim")
        self.assertNotEqual(reply, '')
        for tag in backtick_tags + space_tags:
            self.assertIn(tag, reply)

        reply = bot.create_comment(text, None, "neovim")
        self.assertNotEqual(reply, '')
        for tag in backtick_tags + space_tags:
            self.assertIn(tag, reply);

    def test_punctuation_retry(self):
        """
        Test that bot finds tags that don't
        match because of punctuation, but would
        match otherwise.

        e.g. In the string, "You should look at :h help."
        """

        bot = Bot()
        tags = ["'formatlistpat'", "g:var",
                ":lhelpgrep", ":viusage", "quote."]
        punct = [',', '.', ';', ':']*2
        text = "Test comment: "
        for tag, punct in zip(tags, punct):
            text = text + " :h " + tag + punct

        reply = bot.create_comment(text, None, "vim")
        self.assertNotEqual(reply, '')
        for tag in tags:
            self.assertIn(tag, reply)

        reply = bot.create_comment(text, None, "neovim")
        self.assertNotEqual(reply, '')
        for tag in tags:
            self.assertIn(tag, reply);

    def test_url_encoding(self):
        """
        Test that bot url encodes /
        """

        bot = Bot()
        reply = bot.create_comment("`:h s/\\0`", None, "vim")
        self.assertIn("https://vimhelp.org/change.txt.html#s%2F%5C0", reply)

    def test_neovim_index(self):
        """
        Test that index links to vimindex.html for neovim. See issue #40
        """
        bot = Bot()
        reply = bot.create_comment(":h index", None, "neovim")
        self.assertIn("https://neovim.io/doc/user/vimindex.html", reply)

    def test_square_brackets(self):
        """
        Test that square brackets are handled correctly
        """

        bot = Bot()
        reply = bot.create_comment("`:h ]p`", None, "vim")
        self.assertIn("］", reply)

if __name__ == "__main__":
    unittest.main()
