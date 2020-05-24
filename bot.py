#!/usr/bin/env python

import praw
import re
import requests

reddit = praw.Reddit('bot1')

# Currently point to this subreddit which allows bot testing
subreddit = reddit.subreddit("pythonforengineers")

# Regex to match
# TODO: Does it match every topic?
match_text = ":h ([^\s]+)"

match_re = re.compile(match_text, re.IGNORECASE)

# Track new comments
for comment in subreddit.stream.comments(skip_existing=True):
    matches = match_re.findall(comment.body)

    for match in matches:
        # Create the link by by adjoining .txt after the matched part.
        # TODO: Is this the correct approach?
        link = "https://vimhelp.org/{}.txt.html".format(match)
        request = requests.get(link)
        if request.status_code == 200:
            reply = "Help for {}: {} \n\n I'm a bot.".format(match, link)
            print(reply)
            comment.reply(reply)
        else:
            print("Link not found")
