import os
from cinderclient.v2 import client as cinder_client

class sdk_cinder(object):
    def source_credentials(self, source_script):
        os.system('source %s'%source_script)
        
        auth_username = os.environ.get('OS_USERNAME')
        auth_password = os.environ.get('OS_PASSWORD')
        auth_tenant = os.environ.get('OS_TENANT_NAME')
        auth_url = os.environ.get('OS_AUTH_URL')

        cinderclient = cinder_client.Client(
            username=auth_username,
            api_key=auth_password, project_id=auth_tenant,
            auth_url=auth_url
        )
        
        return cindercslient
        
    def list_volumes(self, source_script):
        cc = self.source_credentials(source_script)
        volumes = cc.volumes.list()
        print volumes
        
source_script = '/home/stack/admin-openrc.sh'
size = 1
sc = sdk_cinder()
sc.list_volumes(source_script)
