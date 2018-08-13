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
VM_DATA_SECTION = 'vm_data'
for section in [CLOUD_SECTION, VM_DATA_SECTION]:
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

OUTPUT_FILE = 'output_file'
LOGS_FOLDER = 'console_log_folder'
for option in [OUTPUT_FILE, LOGS_FOLDER]:
    if not parser.has_option(VM_DATA_SECTION, option):
        raise Exception("ERROR : Missing option '%s' from section '%s' in \
        config file %s"%(option,VM_DATA_SECTION,CONFIG_FILE))

#Folder to store vm console logs
logs_folder = os.path.join(SCRIPT_FOLDER, parser.get(VM_DATA_SECTION, LOGS_FOLDER))
if not os.path.isdir(logs_folder):
    os.makedirs(logs_folder)

#creating nova client
n_client = nova_client(parser.get(CLOUD_SECTION, OPENRC),
                        parser.get(CLOUD_SECTION, NOVA_API_VERSION))

#Reading output file
output_file = os.path.join(SCRIPT_FOLDER, parser.get(VM_DATA_SECTION, OUTPUT_FILE))
file_r = open(output_file, 'r')

#Getting console logs
for instance_id in file_r:
    n_client.get_vm_console_log(instance_id.strip(), logs_folder)

file_r.close()
