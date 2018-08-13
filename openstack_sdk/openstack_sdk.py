import os
import time
from novaclient import client
from novaclient import exceptions
from keystoneauth1.identity import v2
from keystoneauth1.identity import v3
from keystoneauth1 import session
import requests
# suppress warning
requests.packages.urllib3.disable_warnings()

def shell_source(script):
    """source a shell file."""
    import subprocess, os
    pipe = subprocess.Popen(". %s; env" % script, stdout=subprocess.PIPE,
        shell=True)
    output = pipe.communicate()[0]
    env = dict((line.split("=", 1) for line in output.splitlines()))
    os.environ.update(env)

class nova_client(object):
    """Python Nova SDK implementation"""
    def __init__(self, source_script, version):
        """constructor"""
        shell_source(source_script)
        #Using Keystone session to authenticate nova
        auth_url = os.environ.get('OS_AUTH_URL')
        if auth_url.find('v2') >=0:
            auth = v2.Password(auth_url=os.environ['OS_AUTH_URL'],
                       username=os.environ['OS_USERNAME'],
                       password=os.environ['OS_PASSWORD'],
                       tenant_name=os.environ['OS_TENANT_NAME'])
        elif auth_url.find('v3') >=0:
            auth = v3.Password(auth_url=os.environ['OS_AUTH_URL'],
                       username=os.environ['OS_USERNAME'],
                       password=os.environ['OS_PASSWORD'],
                       project_name=os.environ['OS_PROJECT_NAME'],
                       user_domain_id=os.environ['OS_USER_DOMAIN_NAME'],
                       project_domain_name=os.environ['OS_PROJECT_DOMAIN_NAME'])

        keystone_session = session.Session(auth=auth, verify=False)
        self.nova = client.Client(version, session=keystone_session)

    def list_servers(self):
        """List VMs"""
        s_list = self.nova.servers.list()
        print s_list

    def create_vm(self, vm_data):
        """Create a VM and returns instance object"""
        print "VM DATA : ",vm_data
        if not vm_data.get('name') or not vm_data.get('image') \
            or not vm_data.get('flavor') or not vm_data.get('network'):
            raise Exception("ERROR in provided VM data")
        else:
            name = vm_data.get('name')
            image = self.nova.images.find(name=vm_data.get('image'))
            flavor = self.nova.flavors.find(name=vm_data.get('flavor'))
            network = self.nova.networks.find(label=vm_data.get('network'))

            #Creating VM
            instance = self.nova.servers.create(name=name,
                image=image,
                flavor=flavor,
                nics=[{'net-id': network.id}],
                userdata=open(vm_data.get('user_data_file'), 'rb'),
                key_name=vm_data.get('key_name'))

            #Checking/waiting for VM status to become ACTIVE
            while(True):
                inst = self.nova.servers.find(id=instance.id)
                print "VM Status : ",inst.status
                if inst.status == "ACTIVE":
                    break
                else:
                    time.sleep(5)
            print "VM created with ID : ",instance.id
            return instance

    def get_vm_console_log(self, instance_id, logs_folder):
        instance = self.nova.servers.find(id=instance_id)
        while(True):
            try:
                log = self.nova.servers.get_console_output(instance)
                last_line = log.splitlines()[-1]
            except IndexError:
                time.sleep(10)
                continue
            if last_line.find('Cloud-init') == 0 and \
                        last_line.find('finished') > 10:
                logfile = os.path.join(logs_folder,instance.name+'-'+instance.id)
                with open(logfile, 'w') as file:
                    file.write(log)
                print "Console log for instance ID : %s : %s"%(instance_id, logfile)
                break
            else:
                print "Waiting for server boot to complete ......"
                time.sleep(60)

    def delete_vm(self, instance_id):
        try:
            instance = self.nova.servers.find(id=instance_id)
            self.nova.servers.delete(instance)
            while(True):
                try:
                    inst = self.nova.servers.find(id=instance.id)
                except exceptions.NotFound:
                    print "VM with instance ID : %s Deleted"%instance_id
                    break
                time.sleep(5)
        except exceptions.NotFound:
            print "VM with instance ID : %s not found. Skipping Delete...."%instance_id
