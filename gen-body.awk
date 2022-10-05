BEGIN {
  print "<!DOCTYPE html>"
  print "<html lang=\"en\">"
  print "<head>"
  print "  <meta charset=\"UTF-8\" />"
  print "  <meta name=\"viewport\" content=\"width=device-width, initial-scale=1.0\">"
  print "  <title>Gallery</title>"
  print "  <link rel=\"stylesheet\" href=\"gallery.css\" />"
  print "</head>"
  print "<body>"
  print "  <div class=\"navbar\" id=\"navbar\">"
  print "    <div class=\"navbar-item\"><a href="index.html">Übersicht<a/></div>"
  print "    <div class=\"navbar-item\"><a href="morgens.html">Morgens<a/></div>"
  print "    <div class=\"navbar-item\">Mittags</div>"
  print "    <div class=\"navbar-item\">Abends</div>"
  print "    <div class=\"navbar-item\">Fotobox</div>"
  print "  </div>"

  print "  <h1>Picture Gallery</h1>"
  print "  <div class=\"gallery\" id=\"gallery\">"

}

{
  # print "      <div class=\"content\"> <img src=\"img/"$0"\" alt=\""$0"\" onclick=\"window.open(this.src, '_blank');\" /> </div>"
  print "    <div class=\"gallery-item\"> <img src=\"img/"$0"\" alt=\""$0"\" onclick=\"window.open(this.src, '_blank');\" /> </div>"
}

END {
  print "  </div>"
  print "</body>"
  print "</html>"
}
