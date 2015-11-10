### Test - stage 2
### Part of: Blivet test collection
### Author: kvalek@redhat.com
### This program is under GPL licence.
import classes
import test_utils


test_utils.create_new_alloc_table("vdb")

test_system_formatted = classes.SystemDiskFormatted_Scan('vdb')
test_blivet_formatted = classes.BlivetInitialization('vdb').disk
ia = test_utils.test(test_system_formatted, test_blivet_formatted)
test_utils.write_issues(ia, "Formatted disk", 2)
