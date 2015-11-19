### Test execution engine
### Part of: Blivet test collection
### Author: kvalek@redhat.com
### This program is under GPL licence.

import sys
import subprocess
import virtual_machine
import configparser
from test_deps import test_utils

def main_execution(
        machine_name, test_list, deps_list, machine_ram, machine_no_of_disks,
        machine_snap_name, machine_full_path, machine_ks_full_path,
        machine_iso_full_path, machine_copy_path):
    """
        param str machine_name: Machine's name.
        param list test_list: list of test_stage_X* with full path
        param list deps_list: same as test_list, but test deps
        param int machine_ram: amount of memory in MB.
        param int machine_no_of_disks: amount of disks.
        param str machine_snap_name: Machine's snapshot name.
        param str machine_full_path: Full path, where is machine installed
        param str machine_ks_full_path: Full path to kickstart file.
        param str machine_iso_full_path: Full path to installation ISO.
        param str machine_copy_path: Full path to folder where tests and deps reside
    """
    counter = 1
    for inc in test_list:

        if subprocess.call(["virsh list --all | grep {}".format(machine_name)], shell=True) != 0:
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
        virtual_machine.start_machine(machine_name)
        loginst.info("Machine started, tests will be executed on start.")
        loginst.info("Waiting for file copyback.")
        virtual_machine.wait_for_copyback(counter, machine_name, machine_copy_path, loginst, ["TEST_RESULT_{}".format(counter), "blivet_{}_blivet.log".format(counter), "blivet_{}_program.log".format(counter), "stage_{}.log".format(counter)])

        loginst.info("Results copied, reverting machine to {}".format(machine_snap_name))
        virtual_machine.revert_machine(machine_name, machine_snap_name, loginst)
        counter = counter + 1


## Parse INI
CONF_OBJECT = configparser.ConfigParser()

## Load file from command line.
if len(sys.argv) < 3:
    print("USAGE:\tsudo python3 Execute_test.py -i <config_file>")
    sys.exit(0)
else:
    if sys.argv[1] == "-i":
        try:
            CONFIG_FILE = sys.argv[2]
        except:
            print("ERROR: No config INI file specified")
            sys.exit(1)

loginst = test_utils.init_logging(CONFIG_FILE.split(".")[0], 0)

loginst.info("\nStarting testing instance using: {}".format(CONFIG_FILE))
CONF_OBJECT.read(CONFIG_FILE)
loginst.info("Reading {} to parse data.".format(CONFIG_FILE))
MACHINE_NAME = CONF_OBJECT['MACHINE']['MachineName']
MACHINE_RAM = CONF_OBJECT['MACHINE']['MachineRAM']
MACHINE_NO_OF_DISKS = int(CONF_OBJECT['MACHINE']['MachineNoOfDisks'])
MACHINE_SNAP_NAME = CONF_OBJECT['MACHINE']['MachineSnapshotName']
loginst.info("MACHINE section complete")

MACHINE_FULL_PATH = CONF_OBJECT['PATHS']['MachineInstallPath']
MACHINE_KS_FULL_PATH = CONF_OBJECT['PATHS']['MachinePathToKickstart']
MACHINE_ISO_FULL_PATH = CONF_OBJECT['PATHS']['MachinePathToIso']
MACHINE_COPY_PATH = CONF_OBJECT['PATHS']['MachineCopySource']
loginst.info("PATHS section complete")

## Create (if does not exist) and start the machine.
loginst.info("Gathering test stages and test dependencies")
TEST_LIST, DEPS_LIST = virtual_machine.get_files(MACHINE_COPY_PATH, loginst)

## Check, if folder for machine exists, if not, create it
if subprocess.call(["ls {} > /dev/null".format(MACHINE_FULL_PATH)], shell=True) != 0:
    subprocess.call(["mkdir {}".format(MACHINE_FULL_PATH)], shell=True)

## If all is complete, try to start.
if MACHINE_KS_FULL_PATH != "":
    loginst.info("Starting main instance.")
    main_execution(
        MACHINE_NAME, TEST_LIST, DEPS_LIST, MACHINE_RAM, MACHINE_NO_OF_DISKS,
        MACHINE_SNAP_NAME, MACHINE_FULL_PATH, MACHINE_KS_FULL_PATH,
        MACHINE_ISO_FULL_PATH, MACHINE_COPY_PATH)
else:
    loginst.error("Missing parameter - kickstart URL")
    print("Please make your own kickstart file, upload it to "
        "reachable server and specify its URL in INI file.")
