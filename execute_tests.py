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
        machine_iso_full_path, machine_copy_path, start_only = False, machine_update = False):
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
            virtual_machine.create_snapshot(machine_name, machine_snap_name, loginst)

        ## Special condition for -startonly switch
        if start_only == True:
            loginst.debug("MACHINE IN INTERACTIVE / MANUAL MODE - REVERTING TO SNAPSHOT BEFORE START")
            virtual_machine.revert_machine(machine_name, machine_snap_name, loginst)

        ## Special condition for machine update
        if machine_update == True:
            loginst.info("Test suite ran with -update switch - BEGINING UPDATE PROCEDURE. REVERTING to {}".format(machine_snap_name))
            virtual_machine.revert_machine(machine_name, machine_snap_name, loginst)
            virtual_machine.remove_snapshot(machine_name, machine_snap_name, loginst)

        loginst.info("Beginning to copy files using virt-copy-in.")
        virtual_machine.copy_files(test_list[counter - 1], machine_name, machine_copy_path, loginst, True)
        virtual_machine.copy_files(deps_list, machine_name, machine_copy_path, loginst, True)
        loginst.info("Starting virtual machine.")
        virtual_machine.start_machine(machine_name)

        if start_only == False and machine_update == False:
            loginst.info("Machine started, tests will be executed on start.")

            loginst.info("Waiting for file copyback.")
            stage_num = int(test_list[counter - 1].split("_")[2])
            virtual_machine.wait_for_copyback(counter, machine_name, machine_copy_path, loginst, ["TEST_RESULT_{}".format(stage_num), "blivet_{}_blivet.log".format(stage_num), "blivet_{}_program.log".format(stage_num), "stage_{}.log".format(stage_num)])

            loginst.info("Results copied, reverting machine to {}".format(machine_snap_name))
            virtual_machine.revert_machine(machine_name, machine_snap_name, loginst)
            counter = counter + 1

        elif machine_update == True:
            loginst.info("Machine started, begining update procedure. Machine will be shut down automatically")
            virtual_machine.wait_for_shutdown(machine_name)
            virtual_machine.create_snapshot(machine_name, machine_snap_name, loginst)

        else:
            loginst.info("Machine started in interactive mode. Enter it with VNC.")


## Parse INI
CONF_OBJECT = configparser.ConfigParser()
MACHINE_UPDATE = False
MACHINE_START_ONLY = False
TEST_NUM = 0

## Load file from command line.
arg_array = sys.argv
if len(arg_array) != 1:
    if arg_array[1] == "-i":
        try:
            CONFIG_FILE = arg_array[2]
        except:
            print("ERROR:\tNo config file specified.")
            sys.exit(1)
    try:
        if arg_array[3] == "-st":
            try:
                TEST_NUM = int(arg_array[4])
            except:
                print("ERROR:\tNo stage number specified, enter 0 for all tests or number for specific test.")
                sys.exit(1)
        if arg_array[3] == "-startonly":
            MACHINE_START_ONLY = True
            try:
                TEST_NUM = arg_array[4]
                if TEST_NUM == 0:
                    print("ERROR:\tCannot run all tests in interactive mode. Enter specific stage number.")
                    sys.exit(1)
            except:
                print("ERROR:\tNo stage number specified. ")
        if arg_array[3] == "-update":
            MACHINE_UPDATE = True
    except:
        print("No additional parameters set, will run all tests.")
else:
    print("USAGE:\tsudo python3 Execute_test.py -i <config_file> -st <num>\n\t"
            "Enter -st 0 to test all stages, any above for specific stage.")


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

## Special - start only
if MACHINE_START_ONLY == True:
    loginst.debug("RUNNING MACHINE IN INTERACTIVE MODE")
loginst.info("PATHS section complete")

## Create (if does not exist) and start the machine.
loginst.info("Gathering test stages and test dependencies")
TEST_LIST, DEPS_LIST = virtual_machine.get_files(MACHINE_COPY_PATH, loginst, MACHINE_START_ONLY, MACHINE_UPDATE)

if TEST_NUM > 0:
    TEST_LIST = [TEST_LIST[TEST_NUM - 1]]

## Check, if folder for machine exists, if not, create it
if subprocess.call(["ls {} > /dev/null".format(MACHINE_FULL_PATH)], shell=True) != 0:
    subprocess.call(["mkdir {}".format(MACHINE_FULL_PATH)], shell=True)

## If all is complete, try to start.
if MACHINE_KS_FULL_PATH != "":
    loginst.info("Starting main instance.")
    main_execution(
        MACHINE_NAME, TEST_LIST, DEPS_LIST, MACHINE_RAM, MACHINE_NO_OF_DISKS,
        MACHINE_SNAP_NAME, MACHINE_FULL_PATH, MACHINE_KS_FULL_PATH,
        MACHINE_ISO_FULL_PATH, MACHINE_COPY_PATH, MACHINE_START_ONLY, MACHINE_UPDATE)
else:
    loginst.error("Missing parameter - kickstart URL")
    print("Please make your own kickstart file, upload it to "
        "reachable server and specify its URL in INI file.")
