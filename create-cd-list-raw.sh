#!/usr/bin/zsh
hostname=$(uname -n)

if [[ $hostname == 'hel' ]];
then
  current_directory=$PWD
  cd ~/ogg/new
  ls -1 * | grep -vE '^mp3s' | sed 's/.flac//;s/:$//' > $current_directory/cd-list-raw
else
  print "only works on hel"
fi
