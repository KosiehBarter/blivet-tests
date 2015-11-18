### Test utils - Virtual machines
### Part of: Blivet test collection
### Author: kvalek@redhat.com
### This program is under GPL licence.

import subprocess
import glob
import time
import sys

TEST_LIMIT = 10


## Create array of disk arguments
def create_disks(additional_disks, machine_full_path, machine_name, loginst):
    disk_list = []
    letter_counter = 98
    for inc in range(additional_disks):
        disk_list.append("--disk \"{}{}_vd{},size=2\"".format(
            machine_full_path, machine_name, chr(letter_counter)))
        letter_counter = letter_counter + 1
    disk_arg = " ".join(disk_list)
    return disk_arg


## Create and install machine
def create_machine(
        machine_name, machine_full_path, disk_arg, machine_iso_full_path,
        machine_ram, machine_ks_full_path, machine_snap_name, loginst):
    loginst.info("Attempting to create virtual machine.")
    out = subprocess.call([
            "virt-install --name {} "
             "--disk \"{}{}_vda,size=8\" {} "
             "--location {} "
             "--graphics vnc,listen=0.0.0.0 "
             "--noautoconsole --ram {} -x ks={}".format(
                 machine_name, machine_full_path,
                 machine_name, disk_arg, machine_iso_full_path,
                 machine_ram, machine_ks_full_path)], shell = True)
    if out == 0:
        loginst.info("Machine created successfully.")
    else:
        loginst.error("Machine failed to create. Maybe it already exists?")
        sys.exit(1)

    out = 0
    while out != 0:
        time.sleep(1)
        out = subprocess.call([
            "virsh list | grep {} > /dev/null".format(machine_name)], shell=True)

    while (subprocess.call([
            "virsh list | grep {} > /dev/null".format(machine_name)], shell=True) != 1):
        time.sleep(1)

    subprocess.call([
        "virsh snapshot-create-as {} {}".format(
            machine_name, machine_snap_name)], shell=True)
    subprocess.call([
        "virsh shutdown {}".format(machine_name)], shell=True)


## Start, and wait for the machine
def start_machine(machine_name):
    subprocess.call(["virsh start {}".format(machine_name)], shell = True)


## Revert back machine
def revert_machine(machine_name, machine_snap_name, loginst):
    out = subprocess.call(["virsh snapshot-revert {} {}".format(
        machine_name, machine_snap_name)], shell=True)
    if out != 0:
        loginst.error("Snapshot \"{}\" for machine \"{}\" "
            "failed to revert.".format(machine_snap_name, machine_name))
    else:
        loginst.info("Machine \"{}\" successfully "
            "reverted to snapshot \"{}\".".format(machine_name, machine_snap_name))


def get_files(machine_copy_path, loginst):
    test_list = sorted(glob.glob("{}tests/*.py".format(machine_copy_path)))
    deps_list = sorted(glob.glob("{}test_deps/*.py".format(machine_copy_path)))
    ## Special append for run_test.sh
    deps_list.append("{}test_deps/run_test.sh".format(machine_copy_path))
    if test_list == [] and deps_list == []:
        loginst.error("No files in {}: - tests/ OR test_deps/".format(machine_copy_path))
    else:
        loginst.info("Files successfully gathered.")
        return (test_list, deps_list)


def copy_files(
    files_to_copy, machine_name, machine_copy_path,
    loginst, direction = False, copyback_dir = "test_results"):

    if direction == True:
        command = "virt-copy-in -d {}".format(machine_name)
    else:
        command = "virt-copy-out -d {} /root/".format(machine_name)

    action_array = []
    if type(files_to_copy) == str:
        action_array.append(files_to_copy)
    else:
        action_array = files_to_copy

    for inc in action_array:
        if direction == True:
            out = subprocess.call(["{} {} /root/".format(command, inc)], shell=True)
            loginst.debug("Copied: {} {} /root/".format(command, inc))
        else:
            out = subprocess.call(["{}{} {}{}".format(
                command, inc, machine_copy_path, copyback_dir)], shell=True)

    return out


def wait_for_copyback(counter, machine_name, machine_copy_path, loginst, copyback_files):
    enc = 1
    wait_time = 0

    for inc in range(len(copyback_files)):
        status = 1
        while status != 0:
            status = copy_files(copyback_files[inc], machine_name, machine_copy_path, loginst, False)
            if status == 0:
                wait_time = 0
                loginst.debug("Copied:\t{}\tat time: {}".format(copyback_files[inc], wait_time))
            else:
                wait_time = wait_time + 1
                if wait_time >= TEST_LIMIT:
                    loginst.error("File failed to copy:\t\"{}\"".format(copyback_files[inc]))
                    break
