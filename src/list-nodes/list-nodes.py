#!/usr/bin/env python
# -*- coding: UTF-8 -*-

u'''
This executable prints in several formats information about nodes running in a stack.
'''

# System utilities
import sys 
import os
import argparse

# config parser
from configparser import ConfigParser

from keystoneclient.auth.identity import v2
from keystoneclient               import session
from novaclient.client            import Client

from keystoneclient.openstack.common.apiclient.exceptions import AuthorizationFailure
from keystoneclient.openstack.common.apiclient.exceptions import EndpointNotFound
from keystoneclient.openstack.common.apiclient.exceptions import ConnectionRefused

NOVA_VERSION = '2'

def load_config (config_file_path):
	config_file = ConfigParser()
	config_file.read(config_file_path)

	global USER
	global PASS
	global TENANT_ID
	global TENANT_NAME
	global AUTH_URL

	USER        = config_file.get('TENANT ACCESS CREDENTIALS','os_username')
	PASS        = config_file.get('TENANT ACCESS CREDENTIALS','os_password')
	TENANT_ID   = config_file.get('TENANT INFORMATION','os_tenant_id')
	TENANT_NAME = config_file.get('TENANT INFORMATION','os_tenant_name')
	AUTH_URL    = config_file.get('AUTH SERVER','os_auth_url')

def list_nodes ():
	'''
	This function list all nodes in tenant defined in config file
	'''
	try:

		auth = v2.Password(auth_url    = AUTH_URL,
						   username    = USER,
						   password    = PASS,
						   tenant_name = TENANT_NAME,)

		sess = session.Session(auth=auth, verify=False)
		nova = Client(NOVA_VERSION, session=sess, insecure=True)

		for server in nova.servers.list():
			print 'Server name: ' + server.name + '; server Id: ' + server.id

	except AuthorizationFailure as e:
		print e

	except EndpointNotFound as e:
		print 'No keyston endpoint found: ' + AUTH_URL + ' ' + str(e)

	except ConnectionRefused as e:
		print 'Cannot connect to: ' + AUTH_URL + '. '  + str(e)

	except (KeyboardInterrupt, SystemExit) as e:
		print 'Keyboard interrupt or system exit. ' + str(e)

	except:
		print "Unrecognized exception: ", sys.exc_info()[0]


def parse_cmd_line_arguments():
	cmd_parser = argparse.ArgumentParser(description=__doc__)

	cmd_parser.add_argument('-c',
							'--config',
							dest='config_file',
							action='store',
							metavar='TENANT_CONFIG_FILE',
							default='tenant.conf',
							help='Config file with tenant info an credentials to connect to. \
							Default config file is tenant.conf')

	args = cmd_parser.parse_args()
	return args

def main():
	'''
	This function only calls the functions that list nodes
	'''
	args = parse_cmd_line_arguments()
	load_config(args.config_file)
	list_nodes()

if __name__ == '__main__':
	main()
