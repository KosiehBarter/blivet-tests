### Test utils
### Part of: Blivet test collection
### Author: kvalek@redhat.com
### This program is under GPL licence.
import classes_system
import classes_blivet
import checker_test_utils
import test_utils

## Simple function for writting to file.
def write_issues(action, results):
    f = open("/root/TEST_RESULT", "a+")
    if (ia != []):
        f.write("{}\n".format(action))
        for inc in results:
            f.write("{}\n".format(inc))
    else:
        f.write("{} CHECK OK\n".format(action))
    f.close()

print("Basic disk check\n")
test_system = classes_system.SystemDisk_Exe('vdb')
test_blivet = classes_blivet.BlivetDisk_Scan('vdb')
ia = checker_test_utils.test_properties_disk(test_system, test_blivet)
write_issues("\nBasic disk", ia)

print("Formatted disk check\n")
test_system_formatted = classes_system.SystemDiskFormatted_Exe('vdb')
test_blivet_formatted = classes_blivet.BlivetDiskFormatted_Scan('vdb')
ia = checker_test_utils.check_formatting(test_system_formatted, test_blivet_formatted)
write_issues("\nFormatted disk", ia)

print("Partitioned check\n")
test_utils.create_new_partition('vdb', "primary", "MiB", 1, -1)
test_system_partition = classes_system.SystemPartition_Exe('vdb', 1)
test_blivet_partition = classes_blivet.BlivetPartition_Scan('vdb', 1)
ia = checker_test_utils.test_properties_partition(test_system_partition, test_blivet_partition)
write_issues("\nSingle partition", ia)

"""
print("\nPartitioned disk check - Single Formatted")
partition_formatter = classes.SystemPartitionFormatted('vdb', 1, 1, -1, "MiB", "primary", "ext4")
test_system_partition = classes.SystemPartition('vdb', 1, 1, -1, "MiB", "primary")
test_blivet_partition = classes.BlivetPartition('vdb', 1)
ia = checker_test_utils.test_properties_partition(test_system_partition, test_blivet_partition)
checker_test_utils.print_properties(ia)
"""
