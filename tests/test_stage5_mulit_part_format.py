### Test - stage 5
### Part of: Blivet test collection
### Author: kvalek@redhat.com
### This program is under GPL licence.
import classes
import test_utils

loginst_test = test_utils.init_logging(0, None, True)
test_utils.create_new_alloc_table("vdb")


## Multi partition test
start = 1
finish = 512 + start


## Test partitions
list_of_tests = []
list_of_blivet = []
list_of_ia = []

loginst_test.debug("Setting SystemPartitionFormatted_Scan")
for inc in range(4):
    loginst_test.debug("Setting partition {}".format(inc + 1))
    if inc == 3:
        test_utils.create_new_partition("vdb", "primary", start, -1)
    else:
        test_utils.create_new_partition("vdb", "primary", start, finish)
        start = finish + 1
        finish = start + 512
    loginst_test.debug("Setting partition {} - formatting to {}".format(inc + 1, "ext4"))
    test_utils.format_new_partition("{}{}".format("vdb", inc + 1), "ext4")

    ## init objects
    list_of_tests.append(classes.SystemPartitionFormatted_Scan('vdb', inc + 1))
    list_of_blivet.append(classes.BlivetInitialization('vdb', inc + 1).child)

    ## Store in arrays
    loginst.debug("Comparing SystemPartitionFormatted_Scan - partition {} with Blivet instance.".format(inc + 1))
    list_of_ia.append(test_utils.test(list_of_tests[inc], list_of_blivet[inc]))

    ## Store in file.
    test_utils.write_issues(list_of_ia[inc], "Multi partition - part {}".format(inc + 1), 5)
