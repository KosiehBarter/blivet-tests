### Test utils - Virtual machines
### Part of: Blivet test collection
### Author: kvalek@redhat.com
### This program is under GPL licence.

import subprocess
import glob
import time
import re


## Create array of disk arguments
def create_disks(additional_disks, machine_full_path, machine_name):
    disk_list = []
    letter_counter = 98
    for inc in range(additional_disks):
        disk_list.append("--disk \"{}{}_vd{},size=2\"".format(machine_full_path, machine_name, chr(letter_counter)))
        letter_counter = letter_counter + 1
    disk_arg = " ".join(disk_list)
    return disk_arg


## Create and install machine
def create_machine(machine_name, machine_full_path, disk_arg, machine_iso_full_path, machine_ram, machine_ks_full_path, machine_snap_name):
    subprocess.call(["virt-install --name {} --disk \"{}{}_vda,size=8\" {} --location {} --graphics vnc,listen=0.0.0.0 --noautoconsole --ram {} -x ks={}".format(machine_name, machine_full_path, machine_name, disk_arg, machine_iso_full_path, machine_ram, machine_ks_full_path)], shell = True)

    out = 0
    while out != 0:
        time.sleep(1)
        out = subprocess.call(["virsh list | grep {} > /dev/null".format(machine_name)], shell=True)

    while (subprocess.call(["virsh list | grep {} > /dev/null".format(machine_name)], shell=True) != 1):
        time.sleep(1)

    subprocess.call(["virsh snapshot-create-as {} {}".format(machine_name, machine_snap_name)], shell=True)
    subprocess.call(["virsh shutdown {}".format(machine_name)], shell=True)


## Start, and wait for the machine
def start_machine(machine_name):
    subprocess.call(["virsh start {}".format(machine_name)], shell = True)

    hang_iter = 1
    while hang_iter == 1:
        out = subprocess.call(["virt-log -d {} | grep bound\ to".format(machine_name)], shell = True)
        if out == 0:
            hang_iter = 0
        else:
            time.sleep(1)


## Get machine's IP address.
def find_ip_address(machine_name):
    ## Regex the IP address from log and store it to variable
    ip_address = subprocess.getoutput("LANG=c virt-log -d {} | grep bound | tail -n 1".format(machine_name))
    print(ip_address)
    vystup = re.search(r'.*to\ ([0-9]*.[0-9]*.[0-9*]*.[0-9]*).*', ip_address)
    if vystup:
        return vystup.group(1)


## Revert back machine
def revert_machine(machine_name, machine_snap_name):
    out = subprocess.call(["virsh snapshot-revert {} {}".format(machine_name, machine_snap_name)], shell=True)
    if out != 0:
        print("ERROR:\tSnapshot \"{}\" for machine \"{}\" failed to revert.".format(machine_snap_name, machine_name))
    else:
        print("Machine \"{}\" successfully reverted to snapshot \"{}\".".format(machine_name, machine_snap_name))


## Return tuple of lists, test stages and deps
def get_scp_files(scp_copy_source):
    test_list = glob.glob("{}tests/*.py".format(scp_copy_source))
    deps_list = glob.glob("{}test_deps/*.py".format(scp_copy_source))
    return (test_list, deps_list)


## Copy files to machine
def scp_copy_files(ip_address, ssh_full_path, scp_copy_source, test_list, deps_list, copy_result = False):
    if copy_result == True:
        if (subprocess.call(["ls {}test_results".format(scp_copy_source)], shell=True) != 0):
            subprocess.call(["mkdir {}test_results".format(scp_copy_source)], shell=True)

        subprocess.call(["scp -o StrictHostKeyChecking=no -i {} root@{}:/root/TEST_RESULT* {}test_results/".format(ssh_full_path, ip_address, scp_copy_source)], shell=True)
    ## If copy_result == False
    else:
        subprocess.call(["ssh -o StrictHostKeyChecking=no -i {} root@{} 'mkdir ~/tests && mkdir ~/test_teps'".format(ssh_full_path, ip_address)], shell=True)
        subprocess.call(["scp -o StrictHostKeyChecking=no -i {} {} root@{}:~/tests/".format(ssh_full_path, " ".join(test_list), ip_address)], shell=True)
        subprocess.call(["scp -o StrictHostKeyChecking=no -i {} {} root@{}:~/tests/".format(ssh_full_path, " ".join(deps_list), ip_address)], shell=True)


## Initiate test stage
def initiate_test(ip_address, ssh_full_path, test_num):
    subprocess.call(["ssh -o StrictHostKeyChecking=no -i {} root@{} 'python3 /root/tests/test_stage{}*'".format(ssh_full_path, ip_address, test_num)], shell=True)
