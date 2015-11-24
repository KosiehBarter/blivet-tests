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

def create_partition(log_stage, bo, disk_obj):
    log_stage.debug("Calling: blivet.partitioning.get_free_regions on {}, align=True".format(disk_obj.name))
    part_size = blivet.partitioning.getFreeRegions([disk_obj], align=True)
    log_stage.debug("part_size = {}".format(part_size))

    new_part = bo.newPartition(size=part_size[0].getSize(), parents=[disk_obj])
    bo.createDevice(new_part)
    blivet.partitioning.doPartitioning(bo)
