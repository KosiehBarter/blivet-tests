### Test - stage 4
### Part of: Blivet test collection
### Author: kvalek@redhat.com
### This program is under GPL licence.
import classes
import test_utils

loginst_test = test_utils.init_logging(0, None, True)

test_utils.create_new_alloc_table("vdb")
test_utils.create_new_partition("vdb", "primary", 1, -1)
test_utils.format_new_partition("{}{}".format("vdb", 1), "ext4")

loginst_test.debug("Setting up SystemPartitionFormatted_Scan")
tspf = classes.SystemPartitionFormatted_Scan('vdb', 1)
tbpf = classes.BlivetInitialization('vdb', 1).child
loginst_test.debug("Comparing object attributes")
ia = test_utils.test(tspf, tbpf)
test_utils.write_issues(ia, "Single partition formatted", 4)
