### Test utils - Blivet
### Part of: Blivet test collection
### Author: kvalek@redhat.com
### This program is under GPL licence.

install_name = "f23"
install_disk = "{}.iso".format(install_name)
mach_name = install_name
full_disk_path_1 = "/home/Libvirt_disks/{}1.img".format(mach_name)
full_disk_path_2 = "/home/Libvirt_disks/{}2.img".format(mach_name)
full_disk_path_3 = "/home/Libvirt_disks/{}3.img".format(mach_name)
full_loc_path = "/home/Libvirt_disks/{}".format(install_disk)
ks_file_path = "http://cobra02/ks/kv/autoInstaller.ks"
ram_size = 2048

import subprocess
import glob
import time

#
scp_source = "/home/kvalek/GitHub/blivet-tests/"


# Destroy the machine if needed
subprocess.call(["virsh", "destroy", "{}".format(mach_name)])
subprocess.call(["virsh", "undefine", "{}".format(mach_name)])

subprocess.call(["virt-install", "--name", "{}".format(mach_name),\
"--disk", "{},size=8".format(full_disk_path_1),\
"--disk", "{},size=2".format(full_disk_path_2),\
"--disk", "{},size=2".format(full_disk_path_3),\
"--location", "{}".format(full_loc_path),\
"--ram", "{}".format(ram_size), "-x", "ks={}".format(ks_file_path), "--noreboot"])


subprocess.call(["virsh", "start", install_name])
time.sleep(20)
file_list = glob.glob("{}*".format(scp_source))
for inc in file_list:
    subprocess.call(["scp", "-i", "/home/kvalek/.ssh/atlas", inc, "192.168.122.2:~"])
subprocess.call(["virsh", "snapshot-create-as", install_name, "--disk-only", "--atomic"])
subprocess.call(["ssh", "-i", "/home/kvalek/.ssh/atlas", "root@192.168.122.2", "'python3'","'test_arrays.py'"])


### virt-log - projdi si manual na zjisteni IP adresy
