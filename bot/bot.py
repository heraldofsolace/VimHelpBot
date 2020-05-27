#!/usr/bin/env python3

import praw
import re
import requests
import sqlite3
from urllib.parse import quote
import os


class Bot:

    def __init__(self):
        super().__init__()

        # Test at r/pythonforengineers
        self.SUBREDDIT = "pythonforengineers" if os.environ.get(
            "BOT_ENV") == "test" else "vim"
        print("Monitoring r/" + self.SUBREDDIT)

        self.conn = sqlite3.connect("tags.db")
        self.cursor = self.conn.cursor()

        # Regex to match
        # First match inside backticks. If that fails fallback to match until first space.
        # TODO: Does it match every topic?
        match_text_with_backtick = r"`:(h|he|hel|help) (.*?)`"
        match_text_with_space = r":(h|he|hel|help) ([^\s]+)"

        self.match_re_space = re.compile(match_text_with_space, re.IGNORECASE)
        self.match_re_backtick = re.compile(
            match_text_with_backtick, re.IGNORECASE)

    def search_tag(self, text):
        text_escaped = text.replace("%", "\\%").replace("_", "\\_")

        # Get all possible matches
        possible_matches = self.cursor.execute(
            """SELECT * FROM tags WHERE tag LIKE (?) ESCAPE '\\'""", ('%'+text_escaped+'%', )).fetchall()

        # Nothing found
        if len(possible_matches) == 0:
            return None
        possible_matches.sort(key=lambda t: len(t[1]))  # Sort by length

        # If there is an exact match, it must be the first one
        # Exact match is the best match
        if len(possible_matches[0][1]) == len(text):
            return {possible_matches[0]: 100}

        # Score of all the matches
        match_scores = {i: 0 for i in possible_matches}
        for doc, tag in possible_matches:
            score = 0.0
            match_index = tag.find(text)
            if match_index != -1:  # Same case match is better
                score += 1.0

            # Case insensitive match index
            match_index = tag.lower().find(text.lower())
            if match_index != 0:
                if not tag[match_index - 1].isalnum():

                    # A match that starts after a non alphanumeric character is better
                    # than a match in the middle of a word.
                    score += 0.5

            # How much near to the beginning the match is.
            # The smaller the better. But we are ranking based on score.
            # So we need to have a higher score if match is near beginning.

            score += (1 / match_index) if match_index != 0 else 1

            # Extract the matched part
            matched_string = tag[match_index: match_index + len(text)]

            # How many alphanumeric characters matched exactly.
            matched_alpha_numeric_characters = 0
            for i in range(len(text)):
                t = text[i]
                if t.isalnum() and t == matched_string[i]:
                    matched_alpha_numeric_characters += 1

            # The more alphanumeric characters matched the better
            score += matched_alpha_numeric_characters

            # The shorter the length of the match, the better
            score += (1 / len(tag))
            match_scores[(doc, tag)] = score

        # Sort by descending score
        match_scores = {k: v for k, v in sorted(
            match_scores.items(), key=lambda item: item[1], reverse=True)}
        return match_scores

    def create_link_for_tag(self, tag, possible_matches):
        text = ""

        # Only care about the best match

        match = next(iter(possible_matches.keys()))
        doc = match[0]
        topic = match[1]
        link = "https://vimhelp.org/{}.txt.html#{}".format(
            quote(doc), quote(topic))
        request = requests.head(link)

        if request.ok:
            text += "* [`{}`]({}) \n".format(topic, link)
        return text

    def start(self):

        reddit = praw.Reddit('bot1')
        subreddit = reddit.subreddit(self.SUBREDDIT)
        # Track new comments
        for comment in subreddit.stream.comments(skip_existing=True):

            # Don't reply to own comment, although it is highly unlikely to contain the trigger terms.
            # if comment.author.name == 'vim-help-bot':
            #   continue
            matches = self.match_re_backtick.findall(comment.body)
            if len(matches) == 0:
                matches = self.match_re_space.findall(comment.body)
            if len(matches) == 0:
                continue

            text = "Help pages for:\n\n"
            replied_topics = []
            for match in matches:
                topic = match[1].strip()
                if topic == '':
                    # Called with no argument
                    topic = "help.txt"

                # Already replied. Skip
                if topic in replied_topics:
                    continue

                # Create the link by by adjoining .txt after the matched part.
                # TODO: Is this the correct approach?

                # Search in DB
                result = self.search_tag(topic)
                print(result)
                if result is None:
                    print("Tag not found")
                else:
                    text += self.create_link_for_tag(topic, result)

            # Link not found for all the topics
            if len(text) == 0:
                continue

            text += "\n\n---\n\n^(\`:\(h|help\) <query>\` |) [^(source)](https://github.com/Herald-Of-Solace/VimHelpBot) ^(|) [^(mistake?)](https://github.com/Herald-Of-Solace/VimHelpBot/issues/new/choose)"
            comment.reply(text)


if __name__ == "__main__":
    bot = Bot()
    bot.start()
