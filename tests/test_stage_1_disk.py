### Test - stage 1
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
        log_stage.info("Fetching system scan of disk:\t{}".format(disk))
        test_system = classes.SystemDisk_Scan(disk)

        log_stage.info("Fetching blivet scan of disk:\t{}".format(disk))
        test_blivet = classes.BlivetInitialization(disk).disk

        log_stage.info("Comparing objects.")
        ia = test_utils.test(test_system, test_blivet)

        log_stage.info("Writting issues.")
        test_utils.write_issues(ia, "Basic disk", 1)
    except Exception as error_mess:
        log_stage.error(error_mess)

if __name__ == '__main__':
    main('vdb')
