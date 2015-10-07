### Test utils
### Part of: Blivet test collection
### Author: kvalek@redhat.com
### This program is under GPL licence.

import sys
import subprocess
from random import randint


## Write issues to file
def write_issues(ia, action):
    f = open("/root/TEST_RESULT", "a+")
    if ia == []:
        f.write("{} CHECK OK\n".format(action))
    else:
        for inc in ia:
            f.write("{}\n".format(inc))
    f.close()


#### Main test
def test(sys_scan, blv_scan):
    ia = []

    for inc in sys_scan.get_attributes():
        if (type(sys_scan) == str):
            # print("{}\t{}".format((getattr(sys_scan, inc)), getattr(blv_scan, inc))) ## Debug: print
            if (getattr(sys_scan, inc) != getattr(blv_scan, inc)):
                ia.append("FAIL:\t{} != {}".format(getattr(sys_scan, inc), getattr(blv_scan, inc)))

        elif(type(sys_scan) == tuple):
            # print("{}\t{}".format((getattr(sys_scan, inc[0]), (getattr(blv_scan, inc[1]))))) ## Debug: print
            if (getattr(sys_scan, inc[0]) != getattr(blv_scan, inc[1])):
                ia.append("FAIL:\t{} != {}".format(getattr(sys_scan[0], inc), getattr(blv_scan, inc[1])))
    return ia


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
    out = subprocess.call(["parted", "--script", "/dev/{}".format(disk), "mklabel", "{}".format(table_type)])
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
    else:
        return


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
