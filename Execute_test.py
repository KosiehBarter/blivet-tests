### Test execution engine
### Part of: Blivet test collection
### Author: kvalek@redhat.com
### This program is under GPL licence.

### COBRA02 IP 10.34.39.2

import sys
import subprocess
import virtual_machine
import configparser
import test_deps.test_utils


def main_execution(machine_name, test_list, deps_list, machine_ram, machine_no_of_disks, machine_snap_name, machine_full_path, machine_ks_full_path, machine_iso_full_path, ssh_key, ssh_full_path, scp_copy_source):
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


## Parse INI
conf_object = configparser.ConfigParser()

## Load file from command line.
if len(sys.argv) < 3:
    print ("USAGE:\tsudo python3 Execute_test.py -i <config_file>")
    sys.exit(0)
else:
    if sys.argv[1] == "-i":
        try:
            config_file = sys.argv[2]
        except:
            print("ERROR: No config INI file specified")
            sys.exit(1)

conf_object.read(config_file)

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

## Create (if does not exist) and start the machine.
test_list, deps_list = virtual_machine.get_scp_files(scp_copy_source)

if subprocess.call(["ls {} > /dev/null".format(ssh_full_path)], shell=True) != 0:
    print("Creating SSH key pair.")
    subprocess.call(["ssh-keygen -t rsa -N \"\" -f {}".format(ssh_full_path)], shell = True)

## Check, if folder for machine exists, if not, create it
if subprocess.call(["ls {} > /dev/null".format(machine_full_path)], shell=True) != 0:
    subprocess.call(["mkdir {}".format(machine_full_path)], shell=True)

## Create a kickstart file.
if subprocess.call(["ls {}{}.ks".format(machine_full_path, machine_name)], shell=True) != 0:
    subprocess.call(["cat ./example.ks > {}{}.ks".format(machine_full_path, machine_name)], shell=True)
    ssh_public_cat = subprocess.getoutput("cat {}.pub".format(ssh_full_path))
    kickstart = open("{}{}.ks".format(machine_full_path, machine_name), "a+")
    kickstart.write("sshkey --username=root \"{}\"".format(ssh_public_cat))
    kickstart.close()
    print("Created {}{}.ks, please upload it to a reachable HTTP / FTP server and specify its url in INI file.".format(machine_full_path, machine_name))
else:
    ## If all is complete, try to start.
    if (machine_ks_full_path != ""):
        main_execution(machine_name, test_list, deps_list, machine_ram, machine_no_of_disks, machine_snap_name, machine_full_path, machine_ks_full_path, machine_iso_full_path, ssh_key, ssh_full_path, scp_copy_source)
    else:
        print("Please specify a kickstart URL in INI file, rows SSHKeyName and SSHFullPath, under SSH.")
