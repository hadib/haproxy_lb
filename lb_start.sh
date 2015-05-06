#!/bin/bash

if [ ! -f /etc/haproxy/haproxy_base.cfg ]; then
   echo "setting up load balancer"
   sudo apt-get install -y build-essential python python-dev python-virtualenv supervisor haproxy python-pip
   sudo pip install flask
   sed -i 's/ENABLED=0/ENABLED=1/' /etc/default/haproxy
   cp /etc/haproxy/haproxy.cfg /etc/haproxy/haproxy_base.cfg
   
cat >/etc/haproxy/servers.json <<EOF
[]
EOF

fi

service haproxy restart
screen -S haproxy_lb -d -m bash -c "cd /home/ubuntu/haproxy_lb; python ./manager.py -p 80 -c 5000"

