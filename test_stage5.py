### Test - stage 5
### Part of: Blivet test collection
### Author: kvalek@redhat.com
### This program is under GPL licence.
import classes
import test_utils


test_utils.create_new_alloc_table("vdb")


## Multi partition test
start = 1
finish = 512 + start


## Test partitions
list_of_tests = []
list_of_blivet = []
list_of_ia = []

for inc in range(4):
    if inc == 3:
        test_utils.create_new_partition("vdb", "primary", start, -1)
    else:
        test_utils.create_new_partition("vdb", "primary", start, finish)
        start = finish + 1
        finish = start + 512
    test_utils.format_new_partition("{}{}".format("vdb", inc + 1), "ext4")

    ## init objects
    list_of_tests.append(classes.SystemPartitionFormatted_Scan('vdb', inc + 1))
    list_of_blivet.append(classes.BlivetInitialization('vdb', inc + 1).child)

    ## Store in arrays
    list_of_ia.append(test_utils.test(list_of_tests[inc], list_of_blivet[inc]))

    ## Store in file.
    test_utils.write_issues(list_of_ia[inc], "Multi partition - part {}".format(inc + 1), 5)
