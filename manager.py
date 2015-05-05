#!/usr/bin/python

from flask import Flask
from flask import request
import threading
import json
import update
import time
import sys, getopt

app = Flask(__name__)


servers_file='/etc/haproxy/servers.json'

lb_port = 80
SECONDS_TO_EXPIRE = 30
serversi = {}

def read_servers_json_file():
	global servers
	s = json.loads(open(servers_file).read())
        servers = {}
	for srv in s:
		servers[srv] = SECONDS_TO_EXPIRE * 3
        print "servers read %s" %servers

def write_json_servers_file():
	global servers
	s = []
	for srv in servers:
		s.append(srv)
	open(servers_file, 'wt').write(json.dumps(s))
        print "servers write %s" %servers

@app.route('/', methods=['POST'])
def hello_world():
        global servers
	worker_ip = request.remote_addr
	if worker_ip not in servers:
		print "new server %s" %worker_ip
		servers[worker_ip]=SECONDS_TO_EXPIRE
		write_json_servers_file()
		update.update_haproxy(lb_port)
	servers[worker_ip]=SECONDS_TO_EXPIRE
	return 'Welcome To Pool %s!' %worker_ip

def timer_thread_func():
        global servers
	while True:
		time.sleep(1)
		remove_server = []
		for server in servers:
                        print 'server %s = %s' %(server, servers[server])
			if servers[server] > 0:
				servers[server] = servers[server] - 1
				if servers[server] == 0:
					remove_server.append(server)
		for srv in remove_server:
			print "server removed %s" %srv
			servers.pop(srv)
		if len(remove_server) > 0:
			write_json_servers_file()
			update.update_haproxy(lb_port)

def main(argv):
        global lb_port
        checkport = 5000
	try:
		opts, args = getopt.getopt(sys.argv[1:],"hp:c:",["port=","checkport="])
	except getopt.GetoptError:
		print 'test.py -p <load balanced port=80> -c <check port=5000>'
		opts = []
                pass
	for opt, arg in opts:
		if opt == '-h':
			print 'test.py -p <load balanced port=80> -c <check port=5000>'
			sys.exit()
		elif opt in ("-p", "--port"):
			try:
				lb_port = int(arg)
                        except:
				pass
		elif opt in ("-c", "--checkport"):
			try:
				checkport = int(arg)
                        except:
				pass
        print "load balanced port : %s" %lb_port
        print "health checking port : %s" %checkport
	read_servers_json_file()
	update.update_haproxy(lb_port)
        t = threading.Thread(target=timer_thread_func)
        t.daemon = True
        t.start()
        print "flask starting"
	app.run(host='0.0.0.0', port=checkport)

if __name__ == '__main__':
	main(sys.argv[1:])
