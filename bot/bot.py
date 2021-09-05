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

        self.env = os.environ.get("BOT_ENV")
        # Test at r/pythonforengineers
        self.SUBREDDIT = "pythonforengineers" if self.env == "test" else "vim+neovim"
        print("Monitoring r/" + self.SUBREDDIT)

        self.conn = sqlite3.connect("tags.db") if self.env == "test" else sqlite3.connect("data/tags.db")
        self.cursor = self.conn.cursor()
        
        self.user_conn = sqlite3.connect("users.db") if self.env == "test" else sqlite3.connect("data/users.db")
        self.user_cursor = self.user_conn.cursor()
        self.user_cursor.execute("""CREATE TABLE IF NOT EXISTS "users" (
	        "username"	TEXT,
	        "stopped"	INTEGER DEFAULT 0,
	        PRIMARY KEY("username")
            )""")
        self.user_conn.commit()
        # Regex to match
        # First match inside backticks. If that fails fallback to match until first space.
        # TODO: Does it match every topic?
        match_text_with_backtick = r"`:(h|he|hel|help) (.*?)`"
        match_text_with_space = r":(h|he|hel|help) ([^\s]+)"

        self.match_re_space = re.compile(match_text_with_space, re.IGNORECASE)
        self.match_re_backtick = re.compile(
            match_text_with_backtick, re.IGNORECASE)

    def create_github_issue(self, tag, link):
        token = os.environ.get("GITHUB_TOKEN")
        issue = {
            "title": "Tag `{}` not found".format(tag),
            "body": "Tag `{}` not found as seen [here](https://reddit.com/{})".format(tag, link),
            "assignees": ["Herald-Of-Solace"],
            "labels": ["bug"]
        }
        print(issue)
        if self.env == "test":
            print("Testing. Not making an issue")
        else:
            response = requests.post("https://api.github.com/repos/heraldofsolace/VimHelpBot/issues",
                      json=issue, headers={"Authorization": "token {}".format(token)})
            print(response.json())

    def search_tag(self, text, subreddit="vim"):
        if subreddit not in ["vim", "neovim"]:
            subreddit = "vim"

        text_escaped = text.replace("\\", "\\\\").replace("%", "\\%").replace("_", "\\_")
        text_escaped = text_escaped.replace('"', "quote")

        # Get all possible matches
        possible_matches = self.cursor.execute(
            """SELECT * FROM tags WHERE tag LIKE (?) ESCAPE '\\' AND software=(?)""", ('%'+text_escaped+'%', subreddit)).fetchall()
        # print(text, "=>", possible_matches)

        # Nothing found
        if len(possible_matches) == 0:
            return None
        possible_matches.sort(key=lambda t: len(t[1]))  # Sort by length
        
        # If there is an exact match, it might not be the first one due to case
        # We keep checking as long as the lengths match
        for match in possible_matches:
            if len(match[1]) != len(text):
                break
            if match[1] == text:
                return {match: 100}

        # Score of all the matches
        match_scores = {i: 0 for i in possible_matches}
        for doc, tag, software in possible_matches:
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
            match_index_percentage = match_index #/ len(tag)
            score += (1 / match_index_percentage) if match_index_percentage != 0 else 1

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
            match_scores[(doc, tag, software)] = score

        # Sort by descending score
        match_scores = {k: v for k, v in sorted(
            match_scores.items(), key=lambda item: item[1], reverse=True)}
        print(text, " => ", match_scores)
        return match_scores

    def create_link_for_tag(self, tag, possible_matches, subreddit="vim"):
        if subreddit not in ["vim", "neovim"]:
            subreddit = "vim"

        text = ""

        # Only care about the best match

        match = next(iter(possible_matches.keys()))
        doc = match[0]
        topic = match[1]

        link = ""
        if subreddit == "vim":
            link = "https://vimhelp.org/{}.txt.html#{}".format(
                quote(doc), quote(topic, safe=''))
        else:
            link = "https://neovim.io/doc/user/{}.html#{}".format(
                quote(doc), quote(topic, safe=''))
        request = requests.head(link)

        if request.ok:
            text += "* [`{}`]({}) in _{}.txt_\n".format(topic, link, doc)
        return text

    def start(self):

        reddit = praw.Reddit('bot1')
        subreddit = reddit.subreddit(self.SUBREDDIT)
        comment_stream = subreddit.stream.comments(skip_existing=True, pause_after=-1)
        inbox_stream = praw.models.util.stream_generator(reddit.inbox.comment_replies, pause_after=-1, skip_existing=True) 

        while True:
            # Track new comments
            for comment in comment_stream:
                if comment is None:
                    break
                
                username = comment.author.name
                # Don't reply to own comment, although it is highly unlikely to contain the trigger terms.
                if username == 'vim-help-bot':
                   continue
                user_preference = self.user_cursor.execute(
                    """SELECT * FROM users WHERE username = (?)""", (username, )).fetchone()
                if user_preference and user_preference[1] == 1:
                    continue
                text = self.create_comment(
                    comment.body, comment.permalink, comment.subreddit.display_name)
                if text != '':
                    comment.reply(text)
            
            # Track replies
            for reply in inbox_stream:
                if reply is None:
                    break
                comment = reply.parent()

                # Is it possible to get inbox message for a comment that is not a reply to own comment?
                if comment.author == 'vim-help-bot':

                    # Rescan
                    if reply.body == 'rescan':
                        print(comment)
                        parent = comment.parent()
                        text = self.create_comment(
                            parent.body, parent.permalink, parent.subreddit.display_name)
                        if text != '':
                            comment.edit(text)
                    # stop ;-;
                    if reply.body == 'stop':
                        username = reply.author.name
                        
                        self.user_cursor.execute("INSERT INTO users VALUES(?, ?)", (username, 1))
                        comment = "I will not reply to your comments anymore!!"
                        comment += "\n\n---\n\n^\`:\(h|help\)&nbsp;<query>\`&nbsp;| [^(about)](https://github.com/heraldofsolace/VimHelpBot)"
                        self.user_conn.commit()
                        reply.reply(comment)
                        
                
    def create_comment(self, comment, link, subreddit="vim"):
        print("Comment in ", subreddit)
        if subreddit not in ["vim", "neovim"]:
            subreddit = "vim"

        matches = self.match_re_backtick.findall(comment)
        matches = matches + self.match_re_space.findall(comment)
        if len(matches) == 0:
            return ''
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
            result = self.search_tag(topic, subreddit)
            print(result)
            if result is None:
                print("Tag not found")
                self.create_github_issue(topic, link)
            else:
                text += self.create_link_for_tag(topic, result, subreddit)
                replied_topics.append(topic)

        # Link not found for all the topics
        if len(replied_topics) == 0:
            return ''

        text += "\n\n---\n\n^\`:\(h|help\)&nbsp;<query>\`&nbsp;| [^(about)](https://github.com/heraldofsolace/VimHelpBot) ^(|) [^(mistake?)](https://github.com/heraldofsolace/VimHelpBot/issues/new/choose) ^(|) [^(donate)](https://liberapay.com/heraldofsolace/donate)"
        text += " ^(|) ^Reply&nbsp;'rescan'&nbsp;to&nbsp;check&nbsp;the&nbsp;comment&nbsp;again"
        text += " ^(|) ^Reply&nbsp;'stop'&nbsp;to&nbsp;stop&nbsp;getting&nbsp;replies&nbsp;to&nbsp;your&nbsp;comments"
        return text


if __name__ == "__main__":
    bot = Bot()
    bot.start()
