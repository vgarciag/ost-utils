#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from keystoneclient.auth.identity import v2
from keystoneclient               import session
from novaclient.client            import Client

USER        = ''
PASS        = ''
TENANT_ID   = ''
TENANT_NAME = ''
AUTH_URL    = ''

NOVA_VERSION = '2'

auth = v2.Password(auth_url    = AUTH_URL,
				   username    = USER,
				   password    = PASS,
				   tenant_name = TENANT_NAME,)

sess = session.Session(auth=auth, verify=False)
nova = Client(NOVA_VERSION, session=sess, insecure=True)

for server in nova.servers.list():
	print "Server name: " + Server.name + "; server Id: " + server.id

