### Test - stage 6
### Part of: Blivet test collection
### Author: kvalek@redhat.com
### This program is under GPL licence.
import classes
import test_utils
log_bl = test_utils.init_logging("blivet", 0, 6)

test_utils.create_new_alloc_table("vdb")
test_utils.create_new_partition("vdb", "extended", 1, -1)

tsep = classes.SystemExtended_Scan('vdb', 1)
tbep = classes.BlivetInitialization('vdb', 1).child
ia = test_utils.test(tsep, tbep)
test_utils.write_issues(ia, "Extended partition test", 6)
