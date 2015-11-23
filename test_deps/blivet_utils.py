### Blivet utils
### Part of: Blivet test collection
### Author: kvalek@redhat.com
### This program is under GPL licence.
import blivet

## Init blivet
def init_blivet_basic():
    bo = blivet.Blivet()
    bo.reset()
    return bo

def init_disk(bo, disk):
    return bl_obj.devicetree.getDeviceByName(disk)


## Create a msdos label
def create_disk_label(bo, disk_object, label_type):
    new_format = blivet.formats.getFormat("disklabel", device=disk_object.path,
                                            labelType = label_type)

    bo.formatDevice(disk_object, new_format)
    bo.doIt()

def create_partition(bo, part_size, disk_obj):
    new_part = bo.newPartition(size=int(part_size), parents=[disk_obj])
    bo.createDevice(new_part)
    blivet.partitioning.doPartitioning(bo)
