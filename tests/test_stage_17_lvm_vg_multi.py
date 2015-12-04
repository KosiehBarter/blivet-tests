### Test - stage 3
### Part of: Blivet test collection
### Author: kvalek@redhat.com
### This program is under GPL licence.
import classes
import test_utils

def main(disk_array):

    stage_num = test_utils.get_stage_num(__file__)

    log_bl = test_utils.init_logging("blivet", 0, stage_num)
    log_bl_prg = test_utils.init_logging("blivet", 0, stage_num, "program")
    log_stage = test_utils.init_logging("stage", 0, stage_num)
    ia = []

    log_stage.info("Starting test: {}".format(__file__))
    try:
        for inc in disk_array:
            log_stage.info("Preparing disk:\t{}".format(inc))
            test_utils.create_new_alloc_table(inc)
            test_utils.create_new_partition(inc, "primary", 1, -1)

        test_utils.create_lphys_vol(disk_array, 1)

        for inc in range(len(disk_array)):
            log_stage.info("Fetching system scan of disk:\t{}".format(disk_array[inc]))
            test_system_partition = classes.SystemPartition_Scan(disk_array[inc], 1)

            log_stage.info("Fetching blivet scan of disk:\t{}".format(disk_array[inc]))
            test_blivet_partition = classes.BlivetInitialization(disk_array[inc], 1).child

            log_stage.info("Comparing objects.")
            ia.append(test_utils.test(test_system_partition, test_blivet_partition, log_stage))

            log_stage.info("Writting issues.")
            test_utils.write_issues(ia, "LVM disk", stage_num)

    except Exception as error_mess:
        log_stage.exception(error_mess)

if __name__ == '__main__':
    main(['vdb', 'vdc'])
