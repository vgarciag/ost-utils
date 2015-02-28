#!/usr/bin/env python
# -*- coding: UTF-8 -*-

u'''
This executable prints in several formats information about nodes and VIPs running in a stack.
'''

# System utilities
import sys 
import os
import argparse
import json

# config parser
from configparser import ConfigParser

from keystoneclient.auth.identity    import v2
from keystoneclient                  import session
from novaclient.client               import Client
from neutronclient.neutron           import client

# some exceptions
from keystoneclient.openstack.common.apiclient import exceptions as keyston_except
from neutronclient.common                      import exceptions as neutron_except

NOVA_API_VERSION    = '2'
NEUTRON_API_VERSION = '2.0'

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

def session_and_auth():
	auth = v2.Password(auth_url    = AUTH_URL,
					   username    = USER,
					   password    = PASS,
					   tenant_name = TENANT_NAME,)

	sess = session.Session(auth=auth, verify=False)
	return sess, auth

def list_nodes(session):
	u'''
	This function list all nodes in tenant defined in config file
	'''
	try:

		nova = Client(NOVA_API_VERSION, session=session, insecure=True)

		formating_data={}
		formating_data['servers']=[]

		for server in nova.servers.list():
			# print 'Server name: ' + server.name + '; server Id: ' + server.id
			formating_data['servers'].append({'server_name' : server.name, 'server_id': server.id, 'networks':[]})
			for net_name in server.networks:
				# print '\t'+net_name + ' IP\'s: '
				formating_data['servers'][-1]['networks'].append({net_name:[]})
				for idx, ip in enumerate(server.networks[net_name]):
					# print '\t\t' + str(idx) + ': ' + ip
					formating_data['servers'][-1]['networks'][-1][net_name].append(ip)

		print json.dumps(formating_data, indent=4, separators=(',', ': '))
		return True

	except keyston_except.AuthorizationFailure as e:
		print e

	except keyston_except.EndpointNotFound as e:
		print 'No keyston endpoint found: ' + AUTH_URL + ' ' + str(e)

	except keyston_except.ConnectionRefused as e:
		print 'Cannot connect to: ' + AUTH_URL + '. '  + str(e)

	except (KeyboardInterrupt, SystemExit) as e:
		print 'Keyboard interrupt or system exit. ' + str(e)

	except:
		print "Unrecognized exception: ", sys.exc_info()[0]

	return False

def list_vips(session):
	u'''
	List all floating ips 
	'''
	try:
		neutron = client.Client(NEUTRON_API_VERSION, session=session, insecure=True)

		# for floating in neutron.list_floatingips()['floatingips']:
		# 	print "Floating: " + str(floating)
		print json.dumps(neutron.list_floatingips(), indent=4, separators=(',', ': '))
		return True
	except keyston_except.AuthorizationFailure as e:
		print e

	except keyston_except.Unauthorized as e:
		print 'Unauthorized: ' + str(e)

	except keyston_except.EndpointNotFound as e:
		print 'No keyston endpoint found: ' + AUTH_URL + ' ' + str(e)

	except keyston_except.ConnectionRefused as e:
		print 'Cannot connect to: ' + AUTH_URL + '. '  + str(e)

	except (KeyboardInterrupt, SystemExit) as e:
		print 'Keyboard interrupt or system exit. ' + str(e)

	except:
		print "Unrecognized exception: ", sys.exc_info()[0]

	return False

def parse_cmd_line_arguments():
	cmd_parser = argparse.ArgumentParser(description=__doc__)

	cmd_parser.add_argument('-c',
							'--config',
							dest='config_file',
							action='store',
							metavar='TENANT_CONFIG_FILE',
							default='tenant.conf',
							help='Config file with tenant info and credentials to connect to. \
							Default config file is tenant.conf looked for itin CWD.')

	args = cmd_parser.parse_args()
	return args

def main():
	u'''
	This function only calls the functions that list nodes
	'''
	args = parse_cmd_line_arguments()
	load_config(args.config_file)

	session,auth = session_and_auth()

	list_nodes(session)
	list_vips(session)

	return 0

if __name__ == '__main__':
	main()
