#!/bin/bash

LBIP=$1
LBPORT=$2

while :
do 
    curl -X POST http://$LBIP:$LBPORT/
    sleep 3
done
