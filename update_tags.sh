#!/bin/bash

[ -d ~/vim ] || git clone https://github.com/vim/vim.git ~/
[ -d ~/neovim ] || git clone https://github.com/neovim/neovim.git

cd ~/vim && git pull
cd ~/neovim && git pull

cd ~/VimHelpBot && python help_tag_extractor.py
