#!/usr/bin/zsh

convert -scale 800x800 $1 ${1}a
mv ${1}a $1
