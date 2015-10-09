### Test utils - Virtual machines
### Part of: Blivet test collection
### Author: kvalek@redhat.com
### This program is under GPL licence.

import subprocess
import glob
import time
import re

## Create a machine function.
def create_machine(install_name, ram_size, disk_path, kickstart, iso_file, additional_disks = 1):
    if(install_name == "" or ram_size == 0, disk_path == "" or iso_file == ""):
        print("Please specify all parameters:\n\
\tinstall_name - name of the machine to perform a test on\n\
\tadditional_disks - Number of additional disks. 1 added automatically, size is set to 2 G for others.\n\
\tram_size - amount of RAM for the machine\n\
\tdisk_path - full path for disks and isos\n\
\t\tNOTE: Specify full path, eg. /home/Libvirt_disks/, including ending slash.\n\
\tkickstart - kickstart path or URL.\n\
\tiso_file - used with disk_path, specifies iso for install. Specify full name.")

    # undefine domain if needed
    subprocess.call(["virsh destroy {}".format(install_name)], shell=True)
    subprocess.call(["virsh undefine {}".format(install_name)], shell=True)

    ## Determine number of disks
    disk_list = []
    letter_counter = 98
    for inc in range(additional_disks):
        disk_list.append("--disk \"{}{}_vd{},size=2\"".format(disk_path, install_name, chr(letter_counter)))
        letter_counter = letter_counter + 1
    disk_arg = " ".join(disk_list)

    # begin creation and installation
    subprocess.call(["virt-install --name {}\
    --disk \"{}{}_vda,size=8\" \
    {}\
    --location {}{} \
    --graphics vnc,listen=0.0.0.0 --noautoconsole \
    --ram {} -x ks={} --noreboot\
    ".format(install_name, disk_path, install_name, disk_arg, disk_path, iso_file, ram_size, kickstart)], shell=True)

    ### Wait until the machine is powered off. Try to ssh if installed.
    while (subprocess.call(["virsh list | grep {} > /dev/null".format(install_name)], shell=True) != 1):
        time.sleep(10)

    start_machine(install_name)

    ## Create a snapshot of the machine.
    subprocess.call(["virsh snapshot-create-as {} snap-start".format(install_name)], shell=True)
    subprocess.call(["virsh shutdown {}".format(install_name)], shell=True)


## Start the machine.
def start_machine(install_name):
    subprocess.call(["virsh", "start", install_name])
    while (subprocess.call(["virt-log -d {} | grep bound > /dev/null".format(install_name)], shell=True) != 0):
        time.sleep(5)

## Find IP address of the machine and return it.
def find_ip_address(install_name):
    ## Regex the IP address from log and store it to variable
    ip_address = subprocess.getoutput("LANG=c virt-log -d {} | grep bound | tail -n 1".format(install_name))
    vystup = re.search(r'.*to\ ([0-9]*.[0-9]*.[0-9*]*.[0-9]*).*', ip_address)
    if vystup:
        return vystup.group(1)


## Copy files to machine
def copy_files(ip_address, copy_path, ssh_cred, return_bool = False):
    file_list = glob.glob("{}*".format(copy_path))
    for inc in file_list:
        subprocess.call(["scp -o UserKnownHostsFile=/dev/null -o StrictHostKeyChecking=no -i {} {} root@{}:/root/".format(ssh_cred, inc, ip_address)], shell=True)
    if return_bool == True:
        return file_list


## Run specified test on a machine with specified IP
def run_test(ip_address, stage_list, scp_copy_source, ssh_full_path, install_name, machine_snap_name):
    if subprocess.call(["ls {}Test_Output".format(scp_copy_source)], shell=True) != 0:
        subprocess.call(["mkdir {}Test_Output".format(scp_copy_source)], shell=True)

    counter = 1
    for inc in stage_list:
        start_machine(install_name)
        copy_files(ip_address, scp_copy_source, ssh_full_path)

        if subprocess.call(["ssh -o StrictHostKeyChecking=no -i {} root@{} 'ls ~/test_stage{}.py'".format(ssh_full_path, ip_address, counter)], shell=True) == 0:
            subprocess.call(["ssh -o StrictHostKeyChecking=no -i {} root@{} 'python3 test_stage{}.py'".format(ssh_full_path, ip_address, counter)], shell=True)
            subprocess.call(["scp -o StrictHostKeyChecking=no -i {} root@{}:~/TEST_RESULT_{} {}Test_Output/".format(ssh_full_path, ip_address, counter, scp_copy_source)], shell=True)
            subprocess.call(["virsh shutdown {}".format(install_name)], shell=True)
            counter = counter + 1
            out = subprocess.call(["virsh snapshot-revert {} {}".format(install_name, machine_snap_name)], shell=True)
            if out != 0:
                return "FAIL:\tVIRSH FAILED TO REVERT TO \"{}\"".format(machine_snap_name)
        else:
            break
    return
