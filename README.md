VimHelpBot is a cute little bot which lurks on [r/vim](https://reddit.com/r/vim) as [u/vim-help-bot](https://www.reddit.com/user/vim-help-bot). It looks for comments containing ":h help-topic" and replies with a link to [Vim Help](https://vimhelp.org/).

## How it works

It monitors all comments on r/vim and uses two regex to extract the help topic. By default it looks for `:h topic` within backticks and extracts `topic`. If it fails, it looks for `:h` and extracts until the first space after that.

It uses a tag database to figure out which helpfile `topic` belongs to and creates a link to vimhelp for that topic.
