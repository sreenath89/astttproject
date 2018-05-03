#
# Copyright 2017 NephoScale
#

from django.conf import settings
from horizon.exceptions import HorizonException
from horizon.utils import functions as utils
from openstack_dashboard import api
from openstack_dashboard.api import base
from openstack_dashboard.api import keystone

from openstack_dashboard.local.local_settings import \
                                        ADMIN_AUTH_URL, \
                                        ADMIN_USERNAME, \
                                        ADMIN_PASSWORD, \
                                        ADMIN_TENANT, \
                                        ADMIN_DOMAIN, \
                                        ADMIN_REGION, \
                                        KEYSTONE_ADMIN_PROJECT_NAME, \
                                        KEYSTONE_ADMIN_PROJECT_DOMAIN_NAME, \
                                        KEYSTONE_ADMIN_USER_DOMAIN_NAME, \
                                        OPENSTACK_API_VERSIONS

if OPENSTACK_API_VERSIONS['identity'] >= 3:
    from keystoneclient.v3 import client as ksclient
else:
    from keystoneclient.v2_0 import client as ksclient

from urbaneclient import Client as UrbaneClient

#Added for Custom Keystoneclient connection
def get_admin_ksclient():

    if OPENSTACK_API_VERSIONS['identity'] >= 3:
        keystone = ksclient.Client(
            username         = ADMIN_USERNAME,
            password         = ADMIN_PASSWORD,
            auth_url         = ADMIN_AUTH_URL,
            project_name     = KEYSTONE_ADMIN_PROJECT_NAME,
            user_domain_name = KEYSTONE_ADMIN_USER_DOMAIN_NAME
        )
        keystone.tenants = keystone.tenants
    else:
        keystone = ksclient.Client(
            username    = ADMIN_USERNAME,
            password    = ADMIN_PASSWORD,
            tenant_name = ADMIN_TENANT,
            auth_url    = ADMIN_AUTH_URL
        ) 
    return keystone

def get_urbaneclient():

    # urbane client automatically discovers
    # Keystone API version from auth_url
    # and takes required parameter
    urbane = UrbaneClient(
        auth_url = ADMIN_AUTH_URL,
        username = ADMIN_USERNAME,
        password = ADMIN_PASSWORD,
        tenant   = ADMIN_TENANT,
        domain   = ADMIN_DOMAIN,
        region   = ADMIN_REGION
    )
    return urbane

