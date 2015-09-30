### Test execution engine
### Part of: Blivet test collection
### Author: kvalek@redhat.com
### This program is under GPL licence.

import virtual_machine
import subprocess

machine_name = "fedora_23"

if(subprocess.call(["LANG=c virsh list --all | grep {}".format(machine_name)], shell=True) != 0):
    virtual_machine.create_machine(machine_name, 2048, "/home/Libvirt_disks/", "http://cobra02/ks/kv/autoInstaller.ks", "f23.iso", 2)

if(subprocess.call(["LANG=c virsh list --all | grep {} | grep running".format(machine_name)], shell=True) != 0):
    virtual_machine.start_machine(machine_name)

ip_address = virtual_machine.find_ip_address(machine_name)

virtual_machine.copy_files(ip_address, "/home/kvalek/GitHub/blivet-tests/", "/home/kvalek/.ssh/atlas")
