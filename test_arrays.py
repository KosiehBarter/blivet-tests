### Test utils
### Part of: Blivet test collection
### Author: kvalek@redhat.com
### This program is under GPL licence.
import classes
import checker_test_utils

test_system = classes.SystemDisk('vdb')
test_blivet = classes.BlivetDisk('vdb')

ia = checker_test_utils.test_properties_disk(test_system, test_blivet)
checker_test_utils.print_properties(ia)

test_system_formatted = classes.SystemDiskFormatted('vdb')
test_blivet_formatted = classes.BlivetDiskFormatted('vdb')
print(test_system_formatted.alloc_type)
print(test_blivet_formatted.b_alloc_type)

test_system_partition = classes.SystemPartition('vda', 1)
test_blivet_partition = classes.BlivetPartition('vda', 1)

ia = checker_test_utils.test_properties_partition(test_system_partition, test_blivet_partition)
