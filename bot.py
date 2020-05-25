#!/usr/bin/env python3

import praw
import re
import requests
import sqlite3
from urllib.parse import quote

reddit = praw.Reddit('bot1')

# Currently point to this subreddit which allows bot testing
subreddit = reddit.subreddit("pythonforengineers")

conn = sqlite3.connect("tags.db")
c = conn.cursor()
# Regex to match
# First match inside backticks. If that fails fallback to match until first space.
# TODO: Does it match every topic?
match_text_with_backtick = r"`:(h|he|hel|help) (.*?)`"
match_text_with_space = r":(h|he|hel|help) ([^\s]+)"

match_re_space = re.compile(match_text_with_space, re.IGNORECASE)
match_re_backtick = re.compile(match_text_with_backtick, re.IGNORECASE)

# Track new comments
for comment in subreddit.stream.comments(skip_existing=True):
    # Don't reply to own comment, although it is highly unlikely to contain the trigger terms.
    #if comment.author.name == 'vim-help-bot':
     #   continue
    matches = match_re_backtick.findall(comment.body)
    if len(matches) == 0:
        matches = match_re_space.findall(comment.body)
    if len(matches) == 0:
        continue
    text = ""
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
        t = (topic,)

        # Search in DB
        result = c.execute('select * from tags where tag=?', t).fetchone()
        print(result)
        if result is None:
            print("Tag not found")
        else:
            doc = result[0]
            link = "https://vimhelp.org/{}.txt.html#{}".format(quote(doc),quote(topic))

            request = requests.head(link)
            if not request.ok:
                topic_single_quotes = "'" + topic + "'"
                link = "https://vimhelp.org/{}.txt.html#{}".format(quote(doc),quote(topic_single_quotes))
                request = requests.head(link)
                print("Link not found with the base topic")

            if request.ok:
                reply = "Help for `{}`: {} \n\n".format(topic, link)
                text += reply
                replied_topics.append(topic)
            else:
                print("Link not found with surrounding single quotes")

    # Link not found for all the topics
    if len(text) == 0:
        continue

    text += "I'm a bot. Check out my pinned post for more information"
    comment.reply(text)
