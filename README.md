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

# Donate

If my program helped you, please consider donating -

<a href="https://liberapay.com/heraldofsolace/donate"><img alt="Donate using Liberapay" src="https://liberapay.com/assets/widgets/donate.svg"></a>

[![ko-fi](https://ko-fi.com/img/githubbutton_sm.svg)](https://ko-fi.com/J3J53WCCI)
