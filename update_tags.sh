#!/bin/bash

# clone (Neo)Vim if it doesn't exist
[ -d third_party/vim ] || git clone https://github.com/vim/vim.git third_party/vim
[ -d third_party/neovim ] || git clone https://github.com/neovim/neovim.git third_party/neovim

# make sure (Neo)Vim are up to date
git -C third_party/vim pull
git -C third_party/neovim pull

# build helptags for (Neo)Vim
vim --clean -E --cmd 'helptags third_party/vim/runtime/doc | quit'
nvim --clean --headless --cmd 'helptags third_party/neovim/runtime/doc | quit'

python3 help_tag_extractor.py
