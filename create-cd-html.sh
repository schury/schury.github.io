#!/usr/bin/zsh


max_cds_for_testing=1000
n=0
num=0

old_album=""

print """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>CD-Liste</title>
  <link rel="stylesheet" href="gallery.css">
</head>
<body>
<table>
<thead><tr><th>#</th><th>Artist</th><th>Album</th><th>Year</th></tr></thead>
<tbody>"""

rm -f songs/*.html

IFS=$'\n'
for i in $(cat cd-list-raw)
do
  # get all the information from the current line
  # and separate into individual variables
  parts=(${(s:/:)i})
  artist_year_album=(${(s/[/)parts[1]})
  songnr_title=(${(s/-/)parts[2]})

  artist=${artist_year_album[1]%???}
  album=${artist_year_album[2]#*]}
  year=${artist_year_album[2]:0:4}

  song_nr=$songnr_title[1]
  song_title=$songnr_title[2]

  if [[ $old_album == $album ]];
  then
    # we still have the same album
  else
    if [[ $n -gt 0 ]];
    then
      echo "</tbody>"   >> songs/$num.html
      echo "</table>"   >> songs/$num.html
      echo "</body>" >> songs/$num.html
    fi
    (( n++ ))
    num=${(l(3)(0))n}
    # new album, so we print the album line
    old_album=$album
    print "<tr><td>$num </td><td>$artist</td><td><a href=\"songs/$num.html\">$album</a></td><td> $year</td></tr>" 

    {
print """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>CD-Liste</title>
  <link rel="stylesheet" href="../gallery.css">
</head>
<body>
<h1>$artist</h1>
<h2>$album - $year</h2>
<table>
<thead><tr><th>#</th><th>Title</th></tr></thead>
<tbody> """
    } >> songs/$num.html
  fi

  print "<tr><td>$song_nr</td><td>$song_title</td></tr>" >> songs/$num.html

  if [ $num -gt $max_cds_for_testing ]
  then
    print "</tbody>"
    print "</table>"
    print "</body>"
    exit
  fi


done

print """
</tbody>
</table>
</body>
"""

exit 
      cp header songs/$num.html
      echo "<body>" >> songs/$num.html
      echo "<h1>$artist</h1>" >> songs/$num.html
      echo "<h2>$album - $year</h2>" >> songs/$num.html
      echo "<table>" >> songs/$num.html
      echo "<thead><tr><th>#</th><th>Title</th></tr></thead>" >> songs/$num.html
      echo "<tbody>" >> songs/$num.html
