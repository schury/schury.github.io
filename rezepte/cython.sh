#!/usr/bin/zsh
cp create-rezepte.sh test.sh
cython3 --embed -o test.c test.sh
gcc -I/usr/include/python3.11 -lpython3.11 test.c -o test
rm test.c test.sh
