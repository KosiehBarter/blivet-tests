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


## Create & start virtual machine
if(subprocess.call(["LANG=c virsh list --all | grep {}".format(machine_name)], shell=True) != 0):
    #subprocess.call(["ssh-keygen -t rsa -N \"\" -f {}SSH/{}".format(machine_full_path, machine_name)], shell=True)
    #ks_sshkey = subprocess.getoutput("cat {}/SSH/{}.pub".format(machine_full_path, machine_name))
    #ks_full_path = test_utils.make_kickstart(machine_full_path, machine_name, ks_repo, ks_keyboard, ks_timezone, ks_rootpass, ks_sshkey, ks_additionalrepo)
    virtual_machine.create_machine(machine_name, machine_ram, machine_full_path, machine_ks_full_path, machine_iso_full_path, machine_snap_name, machine_no_of_disks)

if(subprocess.call(["LANG=c virsh list --all | grep {} | grep running".format(machine_name)], shell=True) != 0):
    virtual_machine.start_machine(machine_name)

ip_address = virtual_machine.find_ip_address(machine_name)

stage_list = virtual_machine.copy_files(ip_address, scp_copy_source, ssh_full_path, True)

virtual_machine.run_test(ip_address, stage_list, scp_copy_source, ssh_full_path, machine_name, machine_snap_name)
