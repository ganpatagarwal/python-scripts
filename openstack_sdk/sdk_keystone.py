import os
import logging

from keystoneauth1.identity import v3
from keystoneauth1 import session

import requests
# suppress warning
requests.packages.urllib3.disable_warnings()

# logging.basicConfig(level=logging.DEBUG)
logging.basicConfig(level=logging.INFO)

LOG = logging.getLogger(__name__)

if os.environ.get('http_proxy') or os.environ.get('https_proxy'):
    LOG.WARN("Proxy env vars set")

# TODO howto pass internalURL
auth = v3.Password(auth_url=os.environ['OS_AUTH_URL'],
                   username=os.environ['OS_USERNAME'],
                   password=os.environ['OS_PASSWORD'],
                   project_name=os.environ['OS_PROJECT_NAME'],
                   user_domain_id=os.environ['OS_USER_DOMAIN_NAME'],
                   project_domain_name=os.environ['OS_PROJECT_DOMAIN_NAME'])

# sess = session.Session(auth=auth, verify='/path/to/ca.cert')
sess = session.Session(auth=auth, verify=False)


import novaclient.client
novac = novaclient.client.Client(2, session=sess)
print novac.servers.list()

import neutronclient.neutron.client
neutc = neutronclient.neutron.client.Client('2.0', session=sess)
neutc.list_networks()
