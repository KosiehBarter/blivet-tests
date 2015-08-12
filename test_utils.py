### Test utils
### Part of: Blivet test collection
### Author: kvalek@redhat.com
### All programs I create are under GPL license.

import sys
import subprocess
from random import randint

## GET section
"""def get_sector_size(disk):
    return int(subprocess.getoutput("cat /sys/block/{}/queue/hw_sector_size".format(disk)))

def get_num_of_sectors(disk):
    return int(subprocess.getoutput("cat /sys/block/{}/size".format(disk)))

def get_real_disk_size(disk):
    return ((get_sect_size(disk) * get_disk_size(disk)) / (1024 * 1024))

def get_disk_uuid(disk):
    return 

def get_removable(disk):
    return int(subprocess.getoutput("cat /sys/block/{}"""

## Get information with cat
def cat_data(fp, pp = None): # fp = full path, pp = partition path
    if pp == None:
        return subprocess.getoutput("cat {}".format(fp))

def ls_path(fp):
    return subprocess.getoutput("ls {}".format(fp))


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
def create_new_partition(disk, type_of_part, type_of_sizing, part_start, part_end):
    out = subprocess.call(["parted", "--script", "/dev/{}".format(disk), "unit", "{}".format(type_of_sizing), "mkpart {} {} {}".format(type_of_part, part_start, part_end)])
    if out != 0:
        sys.exit(out)
    else:
        return

## Format the partition
# partition = self explanatory
# format = ext4, ext3 and so on
def format_new_partition(partition, filesystem = "ext4"):
    out = subprocess.call(["mkfs.{}".format(filesystem), "/dev/{}".format(partition)])
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
