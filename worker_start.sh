#!/bin/bash

LBIP=$1
LBPORT=$2

screen -S haproxy_worker -d -m bash -c "while : ; do curl -X POST http://$LBIP:$LBPORT/ ; sleep 3; done"

