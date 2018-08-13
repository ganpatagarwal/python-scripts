import os
from openstack_sdk import nova_client
from ConfigParser import SafeConfigParser

#config file
SCRIPT_FOLDER = os.getcwd()
CONFIG_FILE = os.path.join(SCRIPT_FOLDER, "config.ini")

#checking for existence of configuration file
if not os.path.isfile(CONFIG_FILE):
    raise Exception("ERROR : Configuration file not found : %s"%CONFIG_FILE)

#parsing config file
parser = SafeConfigParser()
parser.read(CONFIG_FILE)

#Looking for pre-defined sections
CLOUD_SECTION = 'cloud'
VM_SECTION = 'vm'
VM_DATA_SECTION = 'vm_data'
for section in [CLOUD_SECTION,VM_SECTION, VM_DATA_SECTION]:
    if not parser.has_section(section):
        raise Exception("ERROR : Missing required section '%s' \
        from config file %s"%(section,CONFIG_FILE))

#Checking for required options
OPENRC = 'openrc'
NOVA_API_VERSION = 'nova_api_version'
for option in [OPENRC, NOVA_API_VERSION]:
    if not parser.has_option(CLOUD_SECTION, option):
        raise Exception("ERROR : Missing option '%s' from section '%s' \
        in config file %s"%(option,CLOUD_SECTION,CONFIG_FILE))

#checking for existence of openrc file
openrc_file = parser.get(CLOUD_SECTION, OPENRC)
if not os.path.isfile(openrc_file):
    raise Exception("ERROR : Openrc file does not exist : %s"%openrc_file)

COUNT = 'count'
OUTPUT_FILE = 'output_file'
LOGS_FOLDER = 'console_log_folder'
for option in [COUNT, OUTPUT_FILE, LOGS_FOLDER]:
    if not parser.has_option(VM_DATA_SECTION, option):
        raise Exception("ERROR : Missing option '%s' from section '%s' in \
        config file %s"%(option,VM_DATA_SECTION,CONFIG_FILE))

USER_DATA_FILE = 'user_data_file'
for option in ['name', 'image', 'flavor', 'network', 'key_name',USER_DATA_FILE]:
    if not parser.has_option(VM_SECTION, option):
        raise Exception("ERROR : Missing option '%s' from section '%s' in \
        config file %s"%(option,VM_SECTION,CONFIG_FILE))

#checking for VM count
vm_count = parser.getint(VM_DATA_SECTION, COUNT)
if vm_count <= 0:
    raise Exception("ERROR : value of '%s' option in '%s' section \
    should be > 0"%(COUNT,VM_SECTION))

#checking for existence of user data file
user_data_file = os.path.join(SCRIPT_FOLDER, parser.get(VM_SECTION, USER_DATA_FILE))
if not os.path.isfile(user_data_file):
    raise Exception("ERROR : User Data file does not exist : %s"%user_data_file)

#generating VM data from config
vm_data = {}
for name, value in parser.items(VM_SECTION):
    vm_data[name] = value

#creating nova client
n_client = nova_client(parser.get(CLOUD_SECTION, OPENRC),
                        parser.get(CLOUD_SECTION, NOVA_API_VERSION))

output_file = os.path.join(SCRIPT_FOLDER, parser.get(VM_DATA_SECTION, OUTPUT_FILE))
file_w = open(output_file, 'w')

vm_list = []

#creating VMs
for vm in xrange(vm_count):
    temp_vm_data = {}
    temp_vm_data = vm_data.copy()
    temp_vm_data['name'] = temp_vm_data['name']+'-'+str(vm+1)
    inst = n_client.create_vm(temp_vm_data)
    file_w.write(inst.id+'\n')
    vm_list.append(inst)

file_w.close()
