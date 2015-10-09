### Test execution engine
### Part of: Blivet test collection
### Author: kvalek@redhat.com
### This program is under GPL licence.

import virtual_machine
import subprocess

machine_name = "fedora_23"
machine_full_path = "/home/Libvirt_disks/"
machine_ks_full_path = "http://cobra02/ks/kv/autoInstaller.ks"
machine_iso_full_path = "/home/Libvirt_disks/f23.iso"
machine_snap_name = "snap-start"

ssh_full_path = "/home/kvalek/.ssh/atlas"
scp_copy_source = "/home/kvalek/GitHub/blivet-tests/"

if(subprocess.call(["LANG=c virsh list --all | grep {}".format(machine_name)], shell=True) != 0):
    virtual_machine.create_machine(machine_name, 2048, machine_full_path, machine_ks_full_path, machine_iso_full_path, 2)

if(subprocess.call(["LANG=c virsh list --all | grep {} | grep running".format(machine_name)], shell=True) != 0):
    virtual_machine.start_machine(machine_name)

ip_address = virtual_machine.find_ip_address(machine_name)

stage_list = virtual_machine.copy_files(ip_address, scp_copy_source, ssh_full_path, True)

virtual_machine.run_test(ip_address, stage_list, scp_copy_source, ssh_full_path, machine_name, machine_snap_name)
