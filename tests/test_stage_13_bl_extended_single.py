### Test - stage 13
### Part of: Blivet test collection
### Author: kvalek@redhat.com
### This program is under GPL licence.
import classes
import test_utils
import blivet_utils
import parted

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
        blivet_utils.create_partition(log_stage, bo, bl_disk, 2048000000, type_of_part = parted.PARTITION_EXTENDED) ## TODO: Fix free space

        log_stage.info("Fetching system scan of disk:\t{}".format(disk))
        tsep = classes.SystemExtended_Scan(disk, 1)

        log_stage.info("Fetching blivet scan of disk:\t{}".format(disk))
        tbep = classes.BlivetInitialization(disk, 1).child

        log_stage.info("Comparing objects.")
        ia = test_utils.test(tsep, tbep, log_stage)

        log_stage.info("Writting issues.")
        test_utils.write_issues(ia, "Extended partition test", stage_num)

    except Exception as error_mess:
        log_stage.exception(error_mess)

if __name__ == '__main__':
    main('vdb')
