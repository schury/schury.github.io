#!/usr/bin/zsh


max_cds_for_testing=1000
n_real=0
num_real=0
n_disp=0
num_disp=0
total_length=0
old_song_nr=""

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

  artist=${artist_year_album[1]%???}
  album=${artist_year_album[2]#*]}
  year=${artist_year_album[2]:0:4}

  song_nr=$songnr_title[1]
  song_title=${(j:-:)songnr_title[2,-1]}

  if [[ $song_nr == "01 " ]];
  then
    # we have a new album!
    if [[ $n_real -gt 0 ]];
    then 
      # finish the song from last time, with the old num
      # PROBLEM: if album has only one song, we need to do something as well!
      {
      echo "<tr><td></td><td></td><td></tr>"
      echo "<tr class=\"last\"><td></td><td>Total:</td><td>${(l(2)(0))$(( $total_length/60 ))}:${(l(2)(0))$(( $total_length%60 ))}</td></tr>"
      echo "</tbody>"
      echo "</table>"
      echo "</body>" 
      } >> songs/$num_real.html
    fi

    # new album, new total length
    total_length=$(( $parts[3] / 44100 ))

    (( n_real++ ))
    num_real=${(l(3)(0))n_real}
    # counter up for new album, initally this is 0
    if [[ $album =~ "\(Bonus\)" || $album =~ "\(CD 2\)" || $album =~  "\(Bonus Instrumental\)"  ]];
    then
      print "<tr><td></td><td>$artist</td><td><a href=\"songs/$num_real.html\">$album</a></td><td> $year</td></tr>" >> cds.html
    else
      (( n_disp++ ))
      num_disp=${(l(3)(0))n_disp}
      print "<tr><td>$num_disp</td><td>$artist</td><td><a href=\"songs/$num_real.html\">$album</a></td><td> $year</td></tr>" >> cds.html
    fi
    print "$num_disp -- $artist -- $album"
 

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
    } >> songs/$num_real.html
  else
    total_length=$(( $total_length + $parts[3] / 44100 ))
  fi

  # remember old song_nr
  old_song_nr=$song_nr
  print "<tr><td>$song_nr</td><td>$song_title</td><td>$length</td></tr>" >> songs/$num_real.html

  if [ $num_real -gt $max_cds_for_testing ]
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

# finish the last song html file 
{
echo "<tr><td></td><td></td><td></tr>"
echo "<tr class=\"last\"><td></td><td>Total:</td><td>${(l(2)(0))$(( $total_length/60 ))}:${(l(2)(0))$(( $total_length%60 ))}</td></tr>"
echo "</tbody>"
echo "</table>"
echo "</body>" 
} >> songs/$num_real.html

{
print """</tbody>
</table>
<br>
Created: $(date +%F)
</body>"""
} >> cds.html
