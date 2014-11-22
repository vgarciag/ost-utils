#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import sys
from keystoneclient.auth.identity import v2
from keystoneclient               import session
from novaclient.client            import Client

from keystoneclient.openstack.common.apiclient.exceptions import AuthorizationFailure
from keystoneclient.openstack.common.apiclient.exceptions import EndpointNotFound

USER        = ''
PASS        = ''
TENANT_ID   = ''
TENANT_NAME = ''
AUTH_URL    = ''

NOVA_VERSION = '2'

def list_nodes ():
	'''
	This function list all nodes in tenant
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
		print 'No keyston endpoint found: ' + AUTH_URL + str(e)

	except (KeyboardInterrupt, SystemExit) as e:
		print 'Keyboard interruptionor system exit. ' + str(e)

	except:
		print "Unrecognized exception: ", sys.exc_info()[0]


def main():
	'''
	This function only calls the functions that list nodes
	'''
	list_nodes()

if __name__ == '__main__':
	main()
