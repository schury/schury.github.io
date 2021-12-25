BEGIN {
  print "<!DOCTYPE html>"
  print "<html lang=\"en\">"
  print "<head>"
  print "  <meta charset=\"UTF-8\">"
  print "  <meta name=\"viewport\" content=\"width=device-width, initial-scale=1.0\">"
  print "  <title>Gallery</title>"
  print "  <link rel=\"stylesheet\" href=\"gallery.css\">"
  print "</head>"
  print "<body>"
  print "  <h1>Picture Gallery</h1>"
  print "  <div class=\"gallery\" id=\"gallery\">"

}

{
  print "    <div class=\"gallery-item\">"
  print "      <div class=\"content\">"
  print "      <img src=\"img/"$0"\" alt=\""$0"\" onclick=\"window.open(this.src, '_blank');\">"
  print "      </div>"
  print "    </div>"
}

END {
  print "  </div>"
  print "</body>"
  print "</html>"
}
