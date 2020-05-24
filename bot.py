#!/usr/bin/env python

import praw
import re
import requests

reddit = praw.Reddit('bot1')

# Currently point to this subreddit which allows bot testing
subreddit = reddit.subreddit("pythonforengineers")

# Regex to match
# First match inside backticks. If that fails fallback to match until first space.
# TODO: Does it match every topic?
match_text_with_backtick = "\`:(h|he|hel|help) (.*?)\`"
match_text_with_space = ":(h|he|hel|help) ([^\s]+)"

match_re_space = re.compile(match_text_with_space, re.IGNORECASE)
match_re_backtick = re.compile(match_text_with_backtick, re.IGNORECASE)

# Track new comments
for comment in subreddit.stream.comments(skip_existing=True):
    matches = match_re_backtick.findall(comment.body)
    if len(matches) == 0:
        matches = match_re_space.findall(comment.body)
    for match in matches:
        topic = match[1]
        # Create the link by by adjoining .txt after the matched part.
        # TODO: Is this the correct approach?
        link = "https://vimhelp.org/{}.txt.html".format(topic)
        request = requests.get(link)
        if request.status_code == 200:
            reply = "Help for {}: {} \n\n I'm a bot.".format(topic, link)
            print(reply)
            comment.reply(reply)
        else:
            print("Link not found")
