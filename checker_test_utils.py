### Test utils - Checking tool
### Part of: Blivet test collection
### Author: kvalek@redhat.com
### This program is under GPL licence.

def test_properties_disk(sys_scan, blv_scan):
    lt = ["NAME", "PATH", "REMOVABLE", "VENDOR", "SIZE"]
    ia = []
    ss = [sys_scan.name, sys_scan.system_path, sys_scan.removable, sys_scan.vendor, sys_scan.space]
    bs = [blv_scan.b_name, blv_scan.b_system_path, blv_scan.b_removable, blv_scan.b_vendor, blv_scan.b_space]

    for inc in range(len(ss)):
        if (ss[inc] == bs[inc]):
            ia.append("PASS: {}\t: {} == {}".format(lt[inc], ss[inc], bs[inc]))
        else:
            ia.append("FAIL: {}\t {} != {}".format(lt[inc], ss[inc], bs[inc]))
    return ia

def print_properties(ia):
    for inc in range(len(ia)):
        print(ia[inc])

def test_properties_partition(sys_scan, blv_scan):
    lt = ["NAME", "PATH", "num_of_sectors", "PART_TYPE", "PART_START", "PART_END"]
    ia = []
    ss = [sys_scan.name, sys_scan.system_path, sys_scan.num_of_sectors, sys_scan.part_type, sys_scan.part_start, sys_scan.part_end]
    bs = [blv_scan.name, blv_scan.system_path, blv_scan.num_of_sectors, blv_scan.part_type, blv_scan.part_start, blv_scan.part_end]

    for inc in range(len(ss)):
        if (ss[inc] == bs[inc]):
            ia.append("PASS: {}\t: {} == {}".format(lt[inc], ss[inc], bs[inc]))
        else:
            ia.append("FAIL: {}\t: {} != {}".format(lt[inc], ss[inc], bs[inc]))
    return ia
