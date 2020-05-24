#!/usr/bin/env python

import praw
import re

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

        link = "Help for {topic} https://vimhelp.org/{topic}.txt.html \n\n I'm a bot.".format(topic = match)
        comment.reply(link)
