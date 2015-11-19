### Test - stage 5
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

        ## Perform test
        for inc in range(4):
            log_stage.debug("Creating new partition for disk {}, partition {}".format(disk, inc + 1))
            if inc == 3:
                test_utils.create_new_partition(disk, "primary", start, -1)
            else:
                test_utils.create_new_partition(disk, "primary", start, finish)
                start = finish + 1
                finish = start + 512

            test_utils.format_new_partition("{}{}".format(disk, inc + 1), "ext4")

            ## init objects
            log_stage.info("Fetching system scan of disk:\t{}".format("{}{}".format(disk, inc + 1)))
            list_of_tests.append(classes.SystemPartitionFormatted_Scan(disk, inc + 1))

            log_stage.info("Fetching blivet scan of disk:\t{}".format("{}{}".format(disk, inc + 1)))
            list_of_blivet.append(classes.BlivetInitialization(disk, inc + 1).child)

            ## Store in arrays
            log_stage.info("Saving results to issue array for disk:\t{}".format("{}{}".format(disk, inc + 1)))
            list_of_ia.append(test_utils.test(list_of_tests[inc], list_of_blivet[inc]))

            ## Store in file.
            log_stage.info("Comparing objects for partition {}.".format(inc + 1))
            test_utils.write_issues(list_of_ia[inc], "Multi partition - part {}".format(inc + 1), 5)

    except Exception as error_mess:
        log_stage.error(error_mess)

if __name__ == '__main__':
    main('vdb')
