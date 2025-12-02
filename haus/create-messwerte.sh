#!/usr/bin/zsh
# set für messwerte anlegen
curl -d "messwerte" -X PUT http://192.168.178.26:8080/user/vars/messwerte


# einzelne messwerte hinzufügen
typeset -a werte
werte=("264/10201/0/0/12015" \
       "264/10891/0/0/12011" \
       "120/10221/0/11139/0" \
       "120/10221/0/0/12197" \
       "120/10221/0/0/12183" \
       "120/10601/0/11327/0" \
       "120/10601/0/11328/0" \
       "120/10601/0/11329/0" \
       "120/10601/0/11330/0" \
       "264/10891/0/0/12013" \
       "264/10891/0/0/19402" \
       "264/10201/0/11029/2102" \
       "264/10891/0/0/14560" )
for i in $werte; do
  curl -d "user/var/$i" -X PUT http://192.168.178.26:8080/user/vars/messwerte/$i
done
