#!/bin/bash

# clone Vim if it doesn't exist, else pull most recent version
if [ ! -d third_party/vim ]; then
    git clone https://github.com/vim/vim.git third_party/vim
else
    git -C third_party/vim pull
fi

# clone Neovim if it doesn't exist, else pull most recent version
if [ ! -d third_party/neovim ]; then
    git clone https://github.com/neovim/neovim.git third_party/neovim
else
    # store output of git pull
    nvim_status=$(git -C third_party/neovim pull | tee /dev/tty)
fi

# build helptags for Neovim, if needed (Vim repo comes with 'tags' file)
if [ "$nvim_status" != "Already up to date." ]; then
    vim --clean -e --cmd 'helptags third_party/neovim/runtime/doc | quit'
fi

# Directory for storing data
mkdir -p data

python help_tag_extractor.py
