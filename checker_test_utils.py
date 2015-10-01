### Test utils - Checking tool
### Part of: Blivet test collection
### Author: kvalek@redhat.com
### This program is under GPL licence.

## Basic disk test
def test_properties_disk(sys_scan, blv_scan):
    lt = ["NAME", "PATH", "REMOVABLE", "VENDOR", "SIZE"]
    ia = []
    ## ss = sys_scan.test_attributes()
    ## for attr in ss:
        ## sys_scan.getattr(attr) == blv_scan.getattr(attr) 
    ss = [sys_scan.name, sys_scan.system_path, sys_scan.removable, sys_scan.vendor, sys_scan.space]
    bs = [blv_scan.b_name, blv_scan.b_system_path, blv_scan.b_removable, blv_scan.b_vendor, blv_scan.b_space]
    for inc in range(len(ss)):
        if (ss[inc] != bs[inc]):
            ia.append("FAIL: {}\t {} != {}".format(lt[inc], ss[inc], bs[inc]))
    return ia

## Check formatting with fdisk / parted
def check_formatting(sys_scan, blv_scan):
    ia = []
    if(sys_scan.alloc_type != blv_scan.b_alloc_type):
        ia.append("FAIL:\tALLOC_TYPE\t{} != {}".format(sys_scan.alloc_type, blv_scan.b_alloc_type))
    if(sys_scan.disk_uuid != blv_scan.b_disk_uuid):
        ia.append("FAIL:\tDISK_UUID\t{} != {}".format(sys_scan.disk_uuid, blv_scan.b_disk_uuid))
    return ia

## Check partitions
def test_properties_partition(sys_scan, blv_scan):
    lt = ["PART_NAME", "PART_UUID", "PART_SIZE", "PART_SEC_START", "PART_SEC_END"]
    ia = []
    ss = [sys_scan.sd_part_name, sys_scan.sd_part_uuid, sys_scan.sd_part_size, sys_scan.sd_part_start, sys_scan.sd_part_end]
    bs = [blv_scan.bd_part_name, blv_scan.bd_part_uuid, blv_scan.bd_part_size, blv_scan.bd_part_start, blv_scan.bd_part_end]

    for inc in range(len(ss)):
        if (ss[inc] != bs[inc]):
            ia.append("FAIL: {}\t\t: {} != {}".format(lt[inc], ss[inc], bs[inc]))
    return ia

## Print function
def print_properties(ia):
    for inc in range(len(ia)):
        print(ia[inc])
