#!/usr/bin/env python3

from defusedxml.ElementTree import parse
import os
import sys
import configparser
import base64
import uuid
import shutil
from shutil import copyfile

POLICY_KEY_FILE = "policykey.txt"
MIME_FILE = "send.mime"

# read user credentials
config = configparser.ConfigParser()
config.read("user.ini")
user = config["User"]["user"]
password = config["User"]["password"]
host = config["User"]["host"]
device_id = config["User"]["device_id"]

# prepare for execution
def create_build():
	try:
		dir = 'build'
		if os.path.exists(dir):
			shutil.rmtree(dir)
		os.makedirs(dir)
	except FileExistsError as e:
		pass

create_build()

def set_policy_key_from_file(file):
	tree = parse(file).getroot()

	policy_key = '0'

	for child in tree:
		found = get_policy_key_from_node(child)
		if found:
			policy_key = found
			break

	set_policy_key(policy_key)

def get_policy_key_from_node(node):
	for child in node.iter():
		if child.tag == "{Provision:}PolicyKey":
			return child.text
	return ""

def set_policy_key(policy_key):
	policy_file = open(POLICY_KEY_FILE, 'w')
	policy_file.write(policy_key)
	policy_file.close()

def get_policy_key():
	try:
		with open(POLICY_KEY_FILE, 'r') as file:
			data = file.read()
			if not data:
				return '0'
			else:
				return data
	except FileNotFoundError as e:
		return '0'

def get_base64_mime():
	with open(MIME_FILE, 'r') as file:
		data = file.read()
		return str(base64.b64encode(data.encode("utf-8")), "utf-8")

def read_command(command):
	policy_key = get_policy_key()
	with open('templates/command.sh', 'r') as file:
		data = file.read().replace('$user$', user)
		data = data.replace('$password$', password)
		data = data.replace('$host$', host)
		data = data.replace('$device_id$', device_id)
		data = data.replace('$policy_key$', policy_key)
		data = data.replace('$command$', command)

		return data

def prepare_request(from_file, to_file, params = {}):
	with open(from_file, 'r') as file:
		to = open(to_file, 'w')
		data = file.read()
		for k, v in params.items():
			data = data.replace(k, v)
		to.write(data)
		to.close()

def provision():
	set_policy_key('0')

	# get policy
	copyfile('templates/provision-1.xml', 'build/Provision.xml')
	os.system(read_command('Provision'))
	set_policy_key_from_file('build/resp.xml')

	# acknowledge
	prepare_request('templates/provision-2.xml', 'build/Provision.xml', {'$policy_key$': get_policy_key()})
	os.system(read_command('Provision'))
	set_policy_key_from_file('build/resp.xml')

def send():
	mime = get_base64_mime()
	prepare_request('templates/sendmail.xml', 'build/SendMail.xml', {'$mime$': mime, '$client_id$': str(uuid.uuid4())})
	os.system(read_command('SendMail'))


if len(sys.argv) > 1:
	if sys.argv[1] == "login":
		provision()
	if sys.argv[1] == "send":
		send()
