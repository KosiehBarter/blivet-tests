### Test - stage 1
### Part of: Blivet test collection
### Author: kvalek@redhat.com
### This program is under GPL licence.
import classes
import test_utils

log_bl = test_utils.init_logging("blivet", 0, 1)

test_system = classes.SystemDisk_Scan('vdb')
test_blivet = classes.BlivetInitialization('vdb').disk
ia = test_utils.test(test_system, test_blivet)
test_utils.write_issues(ia, "Basic disk", 1)
