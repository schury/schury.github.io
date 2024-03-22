#!/usr/bin/zsh

for i in $(find ./albumart -size +1100k)
do
  print $i
  convert -scale 800x800 -quality 85 $i tmp.jpg
  mv tmp.jpg $i
done
