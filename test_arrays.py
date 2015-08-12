### Test utils
### Part of: Blivet test collection
### Author: kvalek@redhat.com
### This program is under GPL licence.
import classes
import checker_test_utils

test_system = classes.SystemDisk('vdb')
test_blivet = classes.BlivetDisk('vdb')

ia = checker_test_utils.test_properties(test_system, test_blivet)
checker_test_utils.print_properties(ia)

test_mbr_dos = classes.SystemDiskFormatted(disk) ## TODO: FIX
test_mbr_blv = classes.BlivetDiskFormatted()

if test_mbr_dos.alloc_type == test_mbr_blv.b_alloc_type:
    print("PASS")
else:
    print("FAIL")
