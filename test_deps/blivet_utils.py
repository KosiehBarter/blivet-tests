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
    return bo.devicetree.getDeviceByName(disk)


## Create a msdos label
def create_disk_label(bo, disk_object, label_type):
    new_format = blivet.formats.getFormat("disklabel", device=disk_object.path,
                                            labelType = label_type)

    bo.formatDevice(disk_object, new_format)
    bo.doIt()


## Create a partition
def create_partition(log_stage, bo, disk_obj, size = None, disk_format = None, type_of_part = None):

    if size == None:
        part_size = int(bo.getFreeSpace([disk_obj]).get(disk_obj.name)[0]) - 1
        log_stage.debug("part_size = {}".format(part_size))
    else:
        part_size = size

    if disk_format == None:
        new_part = bo.newPartition(size=part_size, parents=[disk_obj], partType = type_of_part)
    else:
        new_part = bo.newPartition(size=part_size, parents=[disk_obj], fmt_type = disk_format, partType = type_of_part)
    log_stage.debug("new_part: {}".format(new_part))
    bo.createDevice(new_part)
    blivet.partitioning.doPartitioning(bo)
    bo.doIt()

def get_disk_size(log_stage, bo, disk_obj):
    pass
