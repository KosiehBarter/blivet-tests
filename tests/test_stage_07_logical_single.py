### Test - stage 7
### Part of: Blivet test collection
### Author: kvalek@redhat.com
### This program is under GPL licence.
import classes
import test_utils

def main(disk):

    stage_num = test_utils.get_stage_num(__file__)

    log_bl = test_utils.init_logging("blivet", 0, stage_num)
    log_bl_prg = test_utils.init_logging("blivet", 0, stage_num, "program")
    log_stage = test_utils.init_logging("stage", 0, stage_num)

    log_stage.info("Starting test: {}".format(__file__))
    try:
        test_utils.create_new_alloc_table(disk)

        ## Multi partition test
        start = 1
        finish = 512 + start

        ## Test partitions
        list_of_tests = []
        list_of_blivet = []
        list_of_ia = []

        log_stage.info("Preparing disk {}".format(disk))
        test_utils.create_new_partition(disk, "extended", start, -1)
        test_utils.create_new_partition(disk, "logical", start + 1, -1)

        log_stage.info("Fetching system scan for logical partition on disk {}".format(disk))
        test_system = classes.SystemLogical_Scan(disk, 1, 5)

        log_stage.info("Fetching Blivet scan for logical partition on disk {}".format(disk))
        test_blivet = classes.BlivetInitialization(disk, 2).child

        log_stage.info("Comparing objects.")
        ia = test_utils.test(test_system, test_blivet, stage_num)

        log_stage.info("Writting issues.")
        test_utils.write_issues(ia, "Single logical partition", stage_num)

    except Exception as error_mess:
        log_stage.exception(error_mess)

if __name__ == '__main__':
    main('vdb')
