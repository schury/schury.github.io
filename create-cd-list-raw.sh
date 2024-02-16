#!/usr/bin/zsh
hostname=$(uname -n)

if [[ $hostname == 'hel' ]];
then
  current_directory=$PWD
  cd ~/ogg/new
  # ls -1 **/*.flac | sed "s/^\'//;s/\'$//;s/.flac//" > $current_directory/cd-list-raw
  # ls -1 * | grep -vE '^mp3s' | sed 's/.flac//;s/:$//' > $current_directory/cd-list-raw

  # metaflac --show-total-samples **/*.flac | sed 's/\.flac:/ \/ /' > $current_directory/cd-list-raw-length
  for i in **/*.flac
  do
    a=$( echo ${i%.flac} )
    parts=(${(s:/:)a})
    b=${parts[1]% - \[*}
    c=${${parts[1]#*\] }%/*}
    d=${parts[2]}
    # print "$b -- $c -- $d"
    r=$( grep "$c/$d" $current_directory/cd-list-raw-length )
    #print $r
    if [[ $r ]];
    then
    else
      #print $a
      #print "$b -- $c -- $d"
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
