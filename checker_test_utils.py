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
    lt = ["NAME", "PATH", "PART_FORMAT", "PART_SIZE", "PART_START", "PART_END", "UUID"]
    ia = []
    ss = [sys_scan.part_name, sys_scan.part_system_path, sys_scan.part_format, sys_scan.part_size, sys_scan.part_start, sys_scan.part_end, sys_scan.part_uuid]
    bs = [blv_scan.b_part_name, blv_scan.b_part_system_path, blv_scan.b_part_format, blv_scan.b_part_size, blv_scan.b_part_start, blv_scan.b_part_end, blv_scan.b_part_uuid]

    for inc in range(len(ss)):
        if (ss[inc] == bs[inc]):
            ia.append("PASS: {}\t\t: {} == {}".format(lt[inc], ss[inc], bs[inc]))
        else:
            ia.append("FAIL: {}\t\t: {} != {}".format(lt[inc], ss[inc], bs[inc]))
    return ia
