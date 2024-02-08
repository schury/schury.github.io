#!/usr/bin/zsh
hostname=$(uname -n)

if [[ $hostname == 'hel' ]];
then
  current_directory=$PWD
  cd ~/ogg/new
  # ls -1 **/*.flac | sed "s/^\'//;s/\'$//;s/.flac//" > $current_directory/cd-list-raw
  # ls -1 * | grep -vE '^mp3s' | sed 's/.flac//;s/:$//' > $current_directory/cd-list-raw
  metaflac --show-total-samples **/*.flac | sed 's/\.flac:/ \/ /' > $current_directory/cd-list-raw-length
else
  print "only works on hel"
fi
