#!/usr/bin/zsh
hostname=$(uname -n)
last_letter=""

if [[ $hostname == 'hel' ]];
then
  current_directory=$PWD
  cd ~/ogg/new

  # metaflac --show-total-samples **/*.flac | sed 's/\.flac:/ \/ /' > $current_directory/cd-list-raw-length
  for i in **/*.flac
  do
    a=$( echo ${i%.flac} )
    r=$( grep -F $a $current_directory/cd-list-raw-length )
    current_letter=$i[1,1]
    if [[ $current_letter == $last_letter ]];
    then
    else
      print $current_letter
      last_letter=$current_letter
    fi
    if [[ $r ]];
    then
      # print "found"
    else
      print "adding $a"
      samples=$( metaflac --show-total-samples $i )
      echo "$a / $samples" >> $current_directory/cd-list-raw-length
    fi 
  done
  cd $current_directory
  sort cd-list-raw-length | uniq > sorted 
  mv -f sorted cd-list-raw-length
else
  print "only works on hel"
fi
