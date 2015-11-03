### Test - stage 2
### Part of: Blivet test collection
### Author: kvalek@redhat.com
### This program is under GPL licence.
import classes
import test_utils

loginst_test = test_utils.init_logging(0, None, True)
test_utils.create_new_alloc_table("vdb")
loginst_test.debug("Setting up classes.SystemDiskFormatted_Scan")
test_system_formatted = classes.SystemDiskFormatted_Scan('vdb')
test_blivet_formatted = classes.BlivetInitialization('vdb').disk
loginst_test.debug("Comparing object attributes")
ia = test_utils.test(test_system_formatted, test_blivet_formatted)
test_utils.write_issues(ia, "Formatted disk", 2)
