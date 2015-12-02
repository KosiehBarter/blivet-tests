### Test - stage 10
### Part of: Blivet test collection
### Author: kvalek@redhat.com
### This program is under GPL licence.
import classes
import test_utils
import blivet_utils

def main(disk):

    stage_num = test_utils.get_stage_num(__file__)

    log_bl = test_utils.init_logging("blivet", 0, stage_num)
    log_bl_prg = test_utils.init_logging("blivet", 0, stage_num, "program")
    log_stage = test_utils.init_logging("stage", 0, stage_num)

    log_stage.info("Starting test: {}".format(__file__))
    try:
        log_stage.info("Preparing disk:\t{}".format(disk))
        bo = blivet_utils.init_blivet_basic()
        bl_disk = bo.devicetree.getDeviceByName(disk)
        blivet_utils.create_disk_label(bo, bl_disk, "msdos")

        log_stage.info("Creating and commiting partition creation on {}".format(disk))
        blivet_utils.create_partition(log_stage, bo, bl_disk, 2048000000) ## TODO: Fix free space

        log_stage.info("Fetching system scan of disk:\t{}".format(disk))
        test_system = classes.SystemPartition_Scan(disk, 1)

        log_stage.info("Fetching blivet scan of disk:\t{}".format(disk))
        test_blivet = classes.BlivetInitialization(disk, 1).child

        log_stage.info("Comparing objects.")
        ia = test_utils.test(test_system, test_blivet, log_stage)

        log_stage.info("Writting issues.")
        test_utils.write_issues(ia, "Single partition - Blivet", stage_num)

    except Exception as error_mess:
        log_stage.exception(error_mess)

if __name__ == '__main__':
    main('vdb')
