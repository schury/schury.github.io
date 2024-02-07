#!/usr/bin/zsh
current_directory=$PWD
cd ~/ogg/new
ls -1 * | grep -vE '^mp3s' | sed 's/.flac//;s/:$//' > $current_directory/cd-list-raw
