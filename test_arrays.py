### Test utils
### Part of: Blivet test collection
### Author: kvalek@redhat.com
### This program is under GPL licence.
import classes
import checker_test_utils

print("Basic disk check")
test_system = classes.SystemDisk('vdb')
test_blivet = classes.BlivetDisk('vdb')

ia = checker_test_utils.test_properties_disk(test_system, test_blivet)
checker_test_utils.print_properties(ia)

print("\nFormatted disk check")
test_system_formatted = classes.SystemDiskFormatted('vdb')
test_blivet_formatted = classes.BlivetDiskFormatted('vdb')
ia = checker_test_utils.check_formatting(test_system_formatted, test_blivet_formatted)


print("\nPartitioned disk check - Single partition")
partition_creator = classes.SystemPartitionCreate('vdb', 1, -1, "MiB", "primary")
test_system_partition = classes.SystemPartition('vdb', 1, 1, -1, "MiB", "primary")
test_blivet_partition = classes.BlivetPartition('vdb', 1)
ia = checker_test_utils.test_properties_partition(test_system_partition, test_blivet_partition)
checker_test_utils.print_properties(ia)

print("\nPartitioned disk check - Single Formatted")
partition_formatter = classes.SystemPartitionFormatted('vdb', 1, 1, -1, "MiB", "primary", "ext4")
test_system_partition = classes.SystemPartition('vdb', 1, 1, -1, "MiB", "primary")
test_blivet_partition = classes.BlivetPartition('vdb', 1)
ia = checker_test_utils.test_properties_partition(test_system_partition, test_blivet_partition)
checker_test_utils.print_properties(ia)
