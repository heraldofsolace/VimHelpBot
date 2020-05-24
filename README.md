VimHelpBot is a cute little bot which lurks on [r/vim](https://reddit.com/r/vim) as [u/vim-help-bot](https://www.reddit.com/user/vim-help-bot). It looks for comments containing ":h help-topic" and replies with a link to (Vim Help)[https://vimhelp.org/].

Currently it works very naively. It looks for ":h" and extracts until the first space and links to https://vimhelp.org/{match}.txt.html
