#!/bin/bash
while true;
BASEDIR=/home/cm/coffeegrinder
do 
	fbi -1 -T 2 -d /dev/fb1 -noverbose -a $BASEDIR/display/`cat $BASEDIR/display/target`;
       	pkill fbi;
       	sleep 1;
done;
