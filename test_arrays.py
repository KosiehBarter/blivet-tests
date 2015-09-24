### Test utils
### Part of: Blivet test collection
### Author: kvalek@redhat.com
### This program is under GPL licence.
import classes
import checker_test_utils

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

## Zero any file @ start
f = open("/root/TEST_RESULT", "w")
f.close()

print("Basic disk check\n")
test_system = classes.SystemDisk('vdb')
test_blivet = classes.BlivetDisk('vdb')
ia = checker_test_utils.test_properties_disk(test_system, test_blivet)
write_issues("Basic disk", ia)

print("Formatted disk check\n")
test_system_formatted = classes.SystemDiskFormatted('vdb')
test_blivet_formatted = classes.BlivetDiskFormatted('vdb')
ia = checker_test_utils.check_formatting(test_system_formatted, test_blivet_formatted)
write_issues("Formatted disk", ia)

"""print("Partitioned check")
test_system_partition = classes.SystemPartition('vdb', 1, 1, -1, 'MiB', 'primary')
test_blivet_partition = classes.BlivetPartition('vdb', 1)
ia = checker_test_utils.test_properties_partition(test_system_partition, test_blivet_partition)
write_issues("Single partition", ia)"""

"""
print("\nPartitioned disk check - Single partition")

ia = checker_test_utils.test_properties_partition(test_system_partition, test_blivet_partition)
checker_test_utils.print_properties(ia)
soubor = open("TEST_RESULT", "a+")
soubor.write("Partitioned disk check - Single partition")
if(ia != None):
    soubor.write(ia)
soubor.close()

print("\nPartitioned disk check - Single Formatted")
partition_formatter = classes.SystemPartitionFormatted('vdb', 1, 1, -1, "MiB", "primary", "ext4")
test_system_partition = classes.SystemPartition('vdb', 1, 1, -1, "MiB", "primary")
test_blivet_partition = classes.BlivetPartition('vdb', 1)
ia = checker_test_utils.test_properties_partition(test_system_partition, test_blivet_partition)
checker_test_utils.print_properties(ia)
"""
