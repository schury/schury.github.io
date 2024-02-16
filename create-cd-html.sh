#!/usr/bin/zsh


max_cds_for_testing=1000
n=0
num=0
total_length=0

old_album=""

{
print """<!DOCTYPE html>
<html lang=\"en\">
<head>
  <meta charset=\"UTF-8\">
  <meta name=\"viewport\" content=\"width=device-width, initial-scale=1.0\">
  <title>CD list</title>
  <link rel=\"stylesheet\" href=\"gallery.css\">
</head>
<body>
<h1>CD list</h1>
<table>
<thead><tr><th>#</th><th>Artist</th><th>Album</th><th>Year</th></tr></thead>
<tbody>"""
} > cds.html

rm -f songs/*.html

IFS=$'\n'
for i in $(cat cd-list-raw-length)
do
  # get all the information from the current line
  # and separate into individual variables
  parts=(${(s:/:)i})
  artist_year_album=(${(s/[/)parts[1]})
  songnr_title=(${(s/-/)parts[2]})
  length=$( date -d@$(( $parts[3] / 44100 )) -u +%M:%S  )
  total_length=$(( $total_length + $parts[3] ))

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
      echo "<tr><td></td><td></td><td></tr>" >> songs/$num.html
      echo "<tr class=\"last\"><td></td><td>Total:</td><td>$( date -d@$(( $total_length / 44100 )) -u +%M:%S  )</td></tr>" >> songs/$num.html
      echo "</tbody>"   >> songs/$num.html
      echo "</table>"   >> songs/$num.html
      echo "</body>" >> songs/$num.html
      total_length=0
    fi
    (( n++ ))
    num=${(l(3)(0))n}
    # new album, so we print the album line
    old_album=$album
    print "<tr><td>$num </td><td>$artist</td><td><a href=\"songs/$num.html\">$album</a></td><td> $year</td></tr>" >> cds.html
    print "$num -- $artist -- $album"

    {
print """<!DOCTYPE html>
<html lang=\"en\">
<head>
  <meta charset=\"UTF-8\">
  <meta name=\"viewport\" content=\"width=device-width, initial-scale=1.0\">
  <title>CD-Liste</title>
  <link rel=\"stylesheet\" href=\"../gallery.css\">
</head>
<body>
<h1>$artist</h1>
<h2>$album - $year</h2>
<table>
<thead><tr><th>#</th><th>Title</th><th>Length</th></tr></thead>
<tbody> """
    } >> songs/$num.html
  fi

  print "<tr><td>$song_nr</td><td>$song_title</td><td>$length</td></tr>" >> songs/$num.html

  if [ $num -gt $max_cds_for_testing ]
  then
    {
    print "</tbody>"
    print "</table>"
    print "<br>"
    print "Created: $(date +%F)"
    print "</body>"
    } >> cds.html
    exit
  fi


done

{
print """</tbody>
</table>
<br>
Created: $(date +%F)
</body>"""
} >> cds.html
