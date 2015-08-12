### Test utils - Blivet
### Part of: Blivet test collection
### Author: kvalek@redhat.com
### All programs I create are under GPL license.
import test_utils
import sys
import blivet

## Init blivet
def init_blivet():
    return blivet.Blivet()

## Get device by name
def get_dev_by_name(blivet_object, disk):
    return blivet_object.devicetree.getDeviceByName(disk)
    

## Scan disk kids
def get_dev_kids(blivet_object, scanned_disk):
    return blivet_object.devicetree.getChildren(scanned_disk)
