### Test execution engine
### Part of: Blivet test collection
### Author: kvalek@redhat.com
### This program is under GPL licence.
import sys
sys.path.append("./Test_Deps/")


import subprocess
import virtual_machine
import configparser
import test_utils

## Parse INI
conf_object = configparser.ConfigParser()
conf_object.read('blivet-tests.ini')

machine_name = conf_object['MACHINE']['MachineName']
machine_ram = conf_object['MACHINE']['MachineRAM']
machine_no_of_disks = int(conf_object['MACHINE']['MachineNoOfDisks'])
machine_snap_name = conf_object['MACHINE']['MachineSnapshotName']

machine_full_path = conf_object['PATHS']['MachineInstallPath']
machine_ks_full_path = conf_object['PATHS']['MachinePathToKickstart']
machine_iso_full_path = conf_object['PATHS']['MachinePathToIso']

ssh_key = conf_object['SSH']['SSHKeyName']
ssh_full_path = "{}{}".format(conf_object['SSH']['SSHFullPath'], ssh_key)
scp_copy_source = conf_object['SSH']['SCPCopySource']

ks_repo = conf_object['KICKSTART']['Repository']
ks_additionalrepo = conf_object['KICKSTART']['AdditionalRepository']
ks_keyboard = conf_object['KICKSTART']['Keyboard']
ks_timezone = conf_object['KICKSTART']['Timezone']
ks_rootpass = conf_object['KICKSTART']['RootPassword']


## Create (if does not exist) and start the machine.


test_list, deps_list = virtual_machine.get_scp_files(scp_copy_source)

counter = 1
for inc in test_list:

    if (subprocess.call(["virsh list --all | grep {}".format(machine_name)],shell=True) == 0):
        virtual_machine.start_machine(machine_name)
    else:
        disk_arg = virtual_machine.create_disks(machine_no_of_disks, machine_full_path, machine_name)
        virtual_machine.create_machine(machine_name, machine_full_path, disk_arg, machine_iso_full_path, machine_ram, machine_ks_full_path, machine_snap_name)

    ip_address = virtual_machine.find_ip_address(machine_name)                                   ## Get IP address
    virtual_machine.scp_copy_files(ip_address, ssh_full_path, scp_copy_source, test_list, deps_list, False)     ## Copy files to machine
    virtual_machine.initiate_test(ip_address, ssh_full_path, counter)
    virtual_machine.scp_copy_files(ip_address, ssh_full_path, scp_copy_source, test_list, deps_list, True)
    virtual_machine.revert_machine(machine_name, machine_snap_name)                             ## Revert back machine
    counter = counter + 1
