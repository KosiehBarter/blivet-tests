### Test - stage 4
### Part of: Blivet test collection
### Author: kvalek@redhat.com
### This program is under GPL licence.
import classes
import test_utils

test_utils.create_new_alloc_table("vdb")
test_utils.create_new_partition("vdb", "primary", 1, -1)
test_utils.format_new_partition("{}{}".format("vdb", 1), "ext4")

tspf = classes.SystemPartitionFormatted_Scan('vdb', 1)
tbpf = classes.BlivetInitialization('vdb', 1).child
ia = test_utils.test(tspf, tbpf)
test_utils.write_issues(ia, "Single partition formatted")
