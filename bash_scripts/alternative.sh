#!/bin/bash

while true;
do
    DATE=`date | cut -d' ' -f4`
    echo $DATE
    #if [[ $DATE == "12:00:00" ]]
    then
            echo "this is a test program" >> /tmp/xyz.log
            sleep 1s
    fi
done
