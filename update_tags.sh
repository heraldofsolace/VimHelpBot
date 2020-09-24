#!/bin/bash

# clone (Neo)Vim if it doesn't exist
[ -d third_party/vim ] || git clone https://github.com/vim/vim.git third_party/vim
[ -d third_party/neovim ] || git clone https://github.com/neovim/neovim.git third_party/neovim

# make sure (Neo)Vim are up to date
git -C third_party/vim pull
git -C third_party/neovim pull

# build helptags for Neovim (Vim repo comes with 'tags' file)
vim --clean -e --cmd 'helptags third_party/neovim/runtime/doc | quit'

python help_tag_extractor.py
