### Test execution engine
### Part of: Blivet test collection
### Author: kvalek@redhat.com
### This program is under GPL licence.

import sys
import subprocess
import virtual_machine
import configparser
import time
from test_deps import test_utils

def main_execution(
        machine_name, test_list, deps_list, machine_ram, machine_no_of_disks,
        machine_snap_name, machine_full_path, machine_ks_full_path,
        machine_iso_full_path, machine_copy_path):
    counter = 1
    for inc in test_list:

        if (subprocess.call(["virsh list --all | grep {}".format(machine_name)], shell=True) != 0):
            loginst.info("Creating virtual machine - creating disk array")
            disk_arg = virtual_machine.create_disks(
                machine_no_of_disks, machine_full_path, machine_name, loginst)
            loginst.info("Creating virtual machine - starting installation")
            virtual_machine.create_machine(
                machine_name, machine_full_path, disk_arg, machine_iso_full_path,
                machine_ram, machine_ks_full_path, machine_snap_name, loginst)

        loginst.info("Beginning to copy files using virt-copy-in.")
        virtual_machine.copy_files(test_list[counter - 1], machine_name, machine_copy_path, loginst, True)
        virtual_machine.copy_files(deps_list, machine_name, machine_copy_path, loginst, True)
        loginst.info("Starting virtual machine.")
        virtual_machine.start_machine(machine_name, loginst)
        loginst.info("Machine started, tests will be executed on start.")
        loginst.info("Waiting for file copyback.")
        virtual_machine.wait_for_copyback(counter, machine_name, machine_copy_path, loginst, False)

        loginst.info("Results copied, reverting machine to {}".format(machine_snap_name))
        virtual_machine.revert_machine(machine_name, machine_snap_name, loginst)
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

loginst = test_utils.init_logging(0, config_file.split(".")[0], None, True)

loginst.info("\nStarting testing instance using: {}".format(config_file))
conf_object.read(config_file)
loginst.info("Reading {} to parse data.".format(config_file))
machine_name = conf_object['MACHINE']['MachineName']
machine_ram = conf_object['MACHINE']['MachineRAM']
machine_no_of_disks = int(conf_object['MACHINE']['MachineNoOfDisks'])
machine_snap_name = conf_object['MACHINE']['MachineSnapshotName']
loginst.info("MACHINE section complete")

machine_full_path = conf_object['PATHS']['MachineInstallPath']
machine_ks_full_path = conf_object['PATHS']['MachinePathToKickstart']
machine_iso_full_path = conf_object['PATHS']['MachinePathToIso']
machine_copy_path = conf_object['PATHS']['MachineCopySource']
loginst.info("PATHS section complete")

## Create (if does not exist) and start the machine.
loginst.info("Gathering test stages and test dependencies")
test_list, deps_list = virtual_machine.get_files(machine_copy_path, loginst)

## Check, if folder for machine exists, if not, create it
if subprocess.call(["ls {} > /dev/null".format(machine_full_path)], shell=True) != 0:
    subprocess.call(["mkdir {}".format(machine_full_path)], shell=True)

## If all is complete, try to start.
if (machine_ks_full_path != ""):
    loginst.info("Starting main instance.")
    main_execution(
        machine_name, test_list, deps_list, machine_ram, machine_no_of_disks,
        machine_snap_name, machine_full_path, machine_ks_full_path,
        machine_iso_full_path, machine_copy_path)
else:
    loginst.error("Missing parameter - kickstart URL")
    print("Please make your own kickstart file, upload it to "
        "reachable server and specify its URL in INI file.")
