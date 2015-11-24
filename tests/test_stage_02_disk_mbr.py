### Test - stage 2
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

        log_stage.info("Preparing disk:\t{}".format(disk))
        test_utils.create_new_alloc_table(disk)

        log_stage.info("Fetching system scan of disk:\t{}".format(disk))
        test_system_formatted = classes.SystemDiskFormatted_Scan(disk)

        log_stage.info("Fetching blivet scan of disk:\t{}".format(disk))
        test_blivet_formatted = classes.BlivetInitialization(disk).disk

        log_stage.info("Comparing objects.")
        ia = test_utils.test(test_system_formatted, test_blivet_formatted)

        log_stage.info("Writting issues.")
        test_utils.write_issues(ia, "Formatted disk", stage_num)

    except Exception as error_mess:
        log_stage.exception(error_mess)

if __name__ == '__main__':
    main('vdb')
