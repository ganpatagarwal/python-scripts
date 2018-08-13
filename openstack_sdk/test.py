import os
from openstack_sdk import nova_client
from ConfigParser import SafeConfigParser

CONFIG_FILE = "/Users/gagarw2/Documents/TestScripts/python-scripts/openstack_sdk/config.ini"
LOGS_FOLDER = "/Users/gagarw2/Documents/TestScripts/python-scripts/openstack_sdk/VM_CONSOLE_LOGS"

if not os.path.isdir(LOGS_FOLDER):
    os.makedirs(LOGS_FOLDER)

#checking for existence of configuration file
if not os.path.isfile(CONFIG_FILE):
    raise Exception("ERROR : Configuration file not found : %s"%CONFIG_FILE)

parser = SafeConfigParser(allow_no_value=False)
parser.read(CONFIG_FILE)

CLOUD_SECTION = 'cloud'
VM_SECTION = 'vm'
for section in [CLOUD_SECTION,VM_SECTION]:
    if not parser.has_section(section):
        raise Exception("ERROR : Missing required section '%s' from config file %s"%(section,CONFIG_FILE))

OPENRC = 'openrc'
NOVA_API_VERSION = 'nova_api_version'
for option in [OPENRC, NOVA_API_VERSION]:
    if not parser.has_option(CLOUD_SECTION, option):
        raise Exception("ERROR : Missing option '%s' from section '%s' in config file %s"%(option,CLOUD_SECTION,CONFIG_FILE))

COUNT = 'count'
USER_DATA_FILE = 'user_data_file'
for option in [COUNT, 'name', 'image', 'flavor', 'network', 'key_name', USER_DATA_FILE]:
    if not parser.has_option(VM_SECTION, option):
        raise Exception("ERROR : Missing option '%s' from section '%s' in config file %s"%(option,VM_SECTION,CONFIG_FILE))

vm_count = parser.getint(VM_SECTION, COUNT)
if vm_count <= 0:
    raise Exception("ERROR : value of '%s' option in '%s' section should be > 0"%(COUNT,VM_SECTION))

user_data_file = parser.get(VM_SECTION, USER_DATA_FILE)
if not os.path.isfile(user_data_file):
    raise Exception("ERROR : User Data file does not exist : %s"%user_data_file)

vm_data = {}
for name, value in parser.items(VM_SECTION):
    vm_data[name] = value

nova_client = nova_client(parser.get(CLOUD_SECTION, OPENRC),
                        parser.get(CLOUD_SECTION, NOVA_API_VERSION))

nova_client.list_servers()

# #Creating VMs
# for vm in xrange(vm_count):
#     temp_vm_data = {}
#     temp_vm_data = vm_data.copy()
#     temp_vm_data['name'] = temp_vm_data['name']+'-'+str(vm+1)
#     nova_client.create_vm(temp_vm_data)
#
# #Checking console logs for VMs
# for vm in xrange(vm_count):
#     temp_vm_data = {}
#     temp_vm_data = vm_data.copy()
#     temp_vm_data['name'] = temp_vm_data['name']+'-'+str(vm+1)
#     logfile = os.path.join(LOGS_FOLDER,temp_vm_data['name'])
#     nova_client.get_vm_console_log(temp_vm_data['name'], logfile)



#source_script = '~/ndc-dev001-v3.sh'
#source_script = '~/ndc-dev001.sh'
#source_script = '~/desktop-demorc.sh'
#source_script = '~/desktop-demorc-v3.sh'
#nova_client = nova_sdk(source_script,'2')
# vm_data = {
#     'name' : 'ganstest',
#     'image': 'UbuntuTrusty',
#     'flavor' : 'm1.small',
#     'network': 'private',
#     'key_name' : 'ubuntu',
#     'user_data_file': 'data.sh'
#     }

# vm_data = {
#     'name' : 'ganstest',
#     'image': 'UbuntuTrusty',
#     'flavor' : 'm1.small',
#     'network': 'Primary2_External_Net',
#     'key_name' : 'sankey',
#     'user_data_file': 'data.sh'
    # }
#nova_client.create_vm(vm_data)
#nova_client.list_servers()
#nova_client.get_vm_console_log(vm_data['name'])

# for vm in vm_list:
#     logfile = os.path.join(LOGS_FOLDER,vm.name+'-'+vm.id)
#     n_client.get_vm_console_log(vm, logfile)

#getting console logs for VMs
# for vm in xrange(vm_count):
#     temp_vm_data = {}
#     temp_vm_data = vm_data.copy()
#     temp_vm_data['name'] = temp_vm_data['name']+'-'+str(vm+1)
#     logfile = os.path.join(LOGS_FOLDER,temp_vm_data['name'])
#     n_client.get_vm_console_log(temp_vm_data['name'], logfile)
