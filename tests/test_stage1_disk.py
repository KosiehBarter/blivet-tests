### Test - stage 1
### Part of: Blivet test collection
### Author: kvalek@redhat.com
### This program is under GPL licence.
import classes
import test_utils

loginst_test = test_utils.init_logging(0, None, True)
loginst_test.debug("Setting up classes.SystemDisk_Scan")
test_system = classes.SystemDisk_Scan('vdb')
test_blivet = classes.BlivetInitialization('vdb').disk
loginst_test.debug("Comparing object attributes")
ia = test_utils.test(test_system, test_blivet)
test_utils.write_issues(ia, "Basic disk", 1)
