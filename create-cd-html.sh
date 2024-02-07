#!/usr/bin/zsh


max_cds_for_testing=1000

rm -f songs/*.html

print """
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>CD-Liste</title>
  <link rel="stylesheet" href="gallery.css" />
</head>
<body>
"""

n=0

print "<table>"
print "<thead><tr><th>#</th><th>Artist</th><th>Album</th><th>Year</th></tr></thead>"
print "<tbody>"
for i in ../new/* 
do
  if [[ "../new/mp3s" != "$i" ]] 
  then
    (( n++ ))
    num=${(l(3)(0))n}
    parts=(${(s/[/)${${i#*/}#*/}})
    band=${parts[1]%???}
    album=${parts[2]#*]}
    year=${parts[2]:0:4}

    {
      cp header songs/$num.html
      echo "<body>" >> songs/$num.html
      echo "<h1>$band</h1>" >> songs/$num.html
      echo "<h2>$album - $year</h2>" >> songs/$num.html
      echo "<table>" >> songs/$num.html
      echo "<thead><tr><th>#</th><th>Title</th></tr></thead>" >> songs/$num.html
      echo "<tbody>" >> songs/$num.html
      cd $i
      for s in *.*
      do 
        l=(${(s/-/)${s%.flac}})
        echo "<tr><td>${l[1]}</td></td><td>${l[2]}</tr>" >> ../../web/songs/$num.html
      done
      cd ../../web
      echo "</tbody>"   >> songs/$num.html
      echo "</table>"   >> songs/$num.html
      echo "</body>" >> songs/$num.html
    }

    print "<tr><td>$num </td><td>$band </td><td><a href=\"songs/$num.html\">$album</a></td><td> $year</td></tr>" 
    if [ $num -gt $max_cds_for_testing ]
    then
      print "</tbody>"
      print "</table>"
      print "</body>"
      exit
    fi
  fi
done
print "</tbody>"
print "</table>"
print "</body>"
