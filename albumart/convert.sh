#!/usr/bin/zsh

for i in $(find . -size +1200k)
do
  print $i
  convert -scale 800x800 -quality 85 $i ${i}a
  mv ${i}a $i
done
