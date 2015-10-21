### Test utils
### Part of: Blivet test collection
### Author: kvalek@redhat.com
### This program is under GPL licence.

import sys
import subprocess
from random import randint


def make_kickstart(machine_full_path, machine_name, ks_repo, ks_keyboard, ks_timezone, ks_rootpass, ks_sshkey, ks_additionalrepo):
    print("{}/{}.ks".format(machine_full_path, machine_name))
    f = open("{}/{}.ks".format(machine_full_path, machine_name), "w")

    f.write("url={}\ninstall\nnetwork --bootproto=dhcp\nbootloader --timeout=1\nzerombr\ncleanpart --all --initlabel --drives=vda\nautopart\nkeyboard --xlayouts={}\ntimezone={}\nrootpw={}\nssh-key --username=root \"{}\"\nrepo --name fedora --baseurl=\"\"\nshutdown\n%packages\npython3-blivet\npython3-ipython\n@core\n%end\n%post\n%end".format(ks_repo, ks_keyboard, ks_timezone, ks_rootpass, ks_sshkey, ks_additionalrepo))
    f.close()
    return "{}/{}.ks".format(machine_full_path, machine_name)


## Write issues to file
def write_issues(ia, action, stage):
    f = open("/root/TEST_RESULT_{}".format(stage), "w")

    if ia != []:
        for inc in ia:
            f.write("{}\n".format(inc))
    else:
        f.write("{} CHECK OK\n".format(action))
    f.close()


#### Main test
def test(sys_scan, blv_scan):
    ia = []

    for inc in sys_scan.get_attributes():
        if  (type(inc) == str):
            if(getattr(sys_scan, inc) != getattr(blv_scan, inc)):
                ia.append("FAIL:\t{} != {}".format(getattr(sys_scan, inc), getattr(blv_scan, inc)))

        elif(type(inc) == tuple):
            if(getattr(sys_scan, inc[0]) != getdeepattr(blv_scan, inc[1])):
                ia.append("FAIL: {}:\t\t{} != {}".format(inc[0], getattr(sys_scan, inc[0]), getdeepattr(blv_scan, inc[1])))
    return ia


## Copied from /pyanaconda/iutil.py
def getdeepattr(obj, name):
    """This behaves as the standard getattr, but supports
       composite (containing dots) attribute names.

       As an example:

       >>> import os
       >>> from os.path import split
       >>> getdeepattr(os, "path.split") == split
       True
    """

    for attr in name.split("."):
        obj = getattr(obj, attr)
    return obj



## Get information with cat
def cat_data(fp): # fp = full path
    return subprocess.getoutput("cat {}".format(fp))


## Boolean method of cat_data
def cat_data_boolean(fp, pp = None):
    if pp == None:
        if int(subprocess.getoutput("cat {}".format(fp))) == 0:
            return False
        else:
            return True


## Get head of data
def get_data_head(data):
    return subprocess.getoutput("find /sys/devices/ | grep {} | head -1".format(data))


## Get partition's mount point
def get_part_mount_point(part_name):
    return subprocess.getoutput("LANG=c tune2fs /dev/{} -l | grep Last\ mounted\ on | sed 's/Last\ mounted\ on:\s*//'".format(part_name))


## Get disk's properties with blkid
def get_disk_props(disk, prop_ind):
    return subprocess.getoutput("blkid /dev/{}".format(disk)).split("\"")[prop_ind]


## Get path with ls
def ls_path(fp, grep = None):
    if grep != None:
        return subprocess.getoutput("ls -l {} | grep {}".format(fp, grep))
    else:
        return subprocess.getoutput("ls {}".format(fp))


## Get alloc type
def get_alloc_type(disk):
    result = subprocess.getoutput("LANG=c parted -m -s --list 2>/dev/null | grep /dev/{}".format(disk))
    return result.split(":")[5]


## Check partition size
def get_part_size(disk, part_number, lvm = False):
    if lvm == False:
        return int(subprocess.getoutput("cat /sys/block/{}/{}{}/size".format(disk, disk, part_number)))
    else:
        return int(subprocess.getoutput("cat /sys/block/{}{}/size".format(disk, part_number)))


## Create a new MBR (for new disks)
# table_type = msdos or gpt
def create_new_alloc_table(disk, table_type = "msdos"):
    out = subprocess.call(["parted --script /dev/{} mklabel {}".format(disk, table_type)], shell=True)
    if out != 0:
        sys.exit(out)
    else:
        return


## Create a new partition
# disk = disk to be scanned
# type_of_part = type of partition - primary, extended, logical
# type of sizing = what type of size to use, if MB or MiB, etc.
# part_start, part_end = where partition starts and ends, respectively. 1 and -1 is whole "disk"
def create_new_partition(disk, type_of_part, part_start, part_end, type_of_size = "MiB"):
    out = subprocess.call(["parted --script /dev/{} unit {} 'mkpart {} {} {}'".format(disk, type_of_size, type_of_part, part_start, part_end)], shell=True)
    if out != 0:
        sys.exit(out)


## Format the partition
# partition = self explanatory
# format = ext4, ext3 and so on
def format_new_partition(partition, filesystem):
    out = subprocess.call(["LANG=c mkfs.{} /dev/{} -F".format(filesystem, partition)], shell=True)
    if out != 0:
        sys.exit(out)
    else:
        return

def rand_part_size(mds): # max disk size
    return randint(16, mds)


## Logical functions
def assign_logical_number(d_name, part_num):
    return subprocess.getoutput("LANG=c parted --script /dev/{} print | grep logical | sed -e 's/Sector\ .*//'".format(d_name)).split("\n")[part_num].split(" ")[1]


## LVM ###############################################################################
## Create physical volume
def create_lphys_vol(disk, disk_number):
    out = subprocess.call(["pvcreate", "/dev/{}{}".format(disk, disk_number)])
    if out != 0:
        sys.exit(out)
    else:
        return

## Create volume group
def create_lvol_grp(vgname, disk_array):
    if disk_array[0] != None:
        out = subprocess.call(["vgcreate", "{}".format(vgname), "/dev/{}1".format(disk_array[0])])
        if out != 0:
            sys.exit(out)

    for inc in range(1, len(disk_array)):
        out = subprocess.call(["vgextend", "{}".format(vgname), "/dev/{}1".format(disk_array[inc])])
        if out != 0:
            sys.exit(out)
    return

## Create logical volume
def create_lvol_lvl(lvname, lvsize, vgname, fixed = True):
    if fixed == True:
        out = subprocess.call(["lvcreate", "-L", "{}".format(lvsize), "-n", "{}".format(lvname), "{}".format(vgname)])
        if out != 0:
            sys.exit(out)
        else:
            return
    else:
        pass
