[![Build and Deploy to Google Compute Engine](https://github.com/heraldofsolace/VimHelpBot/actions/workflows/deploy.yaml/badge.svg)](https://github.com/heraldofsolace/VimHelpBot/actions/workflows/deploy.yaml)

VimHelpBot is a cute little bot which lurks on [r/vim](https://reddit.com/r/vim) and [r/neovim](https://reddit.com/r/neovim) as [u/vim-help-bot](https://www.reddit.com/user/vim-help-bot). It looks for comments containing ":h help-topic" and replies with a link to [Vim Help](https://vimhelp.org/).

## How it works

It monitors all comments on r/vim r/neovim and uses two regex to extract the help topic. By default it looks for `:(h|he|hel|help) topic` within backticks and extracts `topic`. If it fails, it looks for `:h` and extracts until the first space after that.

It uses a tag database to figure out which helpfile `topic` belongs to and creates a link to vimhelp for that topic.

If an exact match is not found, it tries to follow Vim's algorithm. From `:h E149`:


>			If there is no full match for the pattern, or there
>			are several matches, the "best" match will be used.
>			A sophisticated algorithm is used to decide which
>			match is better than another one.  These items are
>			considered in the computation:
>			- A match with same case is much better than a match
>			  with different case.
>			- A match that starts after a non-alphanumeric
>			  character is better than a match in the middle of a
>			  word.
>			- A match at or near the beginning of the tag is
>			  better than a match further on.
>			- The more alphanumeric characters match, the better.
>			- The shorter the length of the match, the better.

If no tag is found for a topic, it automatically creates a github issue.

## Pairing: RedditAPIs (optional managed Reddit data backend)

Users who already adopt this project sometimes ask about routing read-heavy operations (subreddit fetch, post detail, comments, user lookup, search) to a managed backend during testing or for workflows that skip the Reddit developer-app step. The [RedditAPIs code samples repo](https://github.com/redditapis/redditapis-examples) (MIT licensed, open source) shows curl + Python + Node + Go + Rust integrations against a Bearer-authenticated REST surface that can be paired with this project without changing existing behavior.

Two integration patterns:

1. **Side-by-side in your application.** Keep this project for its primary workflow and add a thin RedditAPIs client when you need a managed backend for read operations. Each call maps to whichever backend the user has configured.

2. **PRAW-style migration reference.** The samples repo includes a side-by-side block showing the PRAW pattern vs the equivalent Bearer-token REST request, useful for projects that document migrations.

Subset that pairs cleanly with this project's read path:

- subreddit listings (`hot`, `new`, `top`, `rising`)
- post detail + comments tree
- user profile + submissions
- search across subreddits

Repository: https://github.com/redditapis/redditapis-examples

This pairing is fully optional. No behavior change for existing users of this project.

