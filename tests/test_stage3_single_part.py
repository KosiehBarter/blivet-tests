### Test - stage 3
### Part of: Blivet test collection
### Author: kvalek@redhat.com
### This program is under GPL licence.
import classes
import test_utils

loginst_test = test_utils.init_logging(0, None, True)
test_utils.create_new_alloc_table("vdb")
test_utils.create_new_partition("vdb", "primary", 1, -1)

loginst_test.debug("Setting up classes.SystemPartition_Scan")
test_blivet_partition = classes.BlivetInitialization('vdb', 1).child
test_system_partition = classes.SystemPartition_Scan('vdb', 1)
loginst_test.debug("Comparing object attributes")
ia = test_utils.test(test_system_partition, test_blivet_partition)
test_utils.write_issues(ia, "Partitioned disk", 3)
