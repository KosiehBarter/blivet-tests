### Blivet utils
### Part of: Blivet test collection
### Author: kvalek@redhat.com
### This program is under GPL licence.
import blivet

## Create a msdos label
def create_disk_label(blivet_object, disk_object, label_type):
    nev_format = blivet.formats.getFormat("disklabel", device=disk_object.path,
                                            labelType = label_type)
    blivet.formatDevice(disk_object, new_format)
    blivet_object.doIt()
