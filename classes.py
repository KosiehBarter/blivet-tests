### Classes definition
### Part of: Blivet test collection
### Author: kvalek@redhat.com
### This program is under GPL licence.
import test_utils
import blivet_test_utils

class SystemDisk(object):
    """ Contains all data regarding to a disk.
        At start, a "disk" parameter is received. Based on this parameter,
        all required data are gathered."""
    def __init__(self, disk):
        """
            :param str disk: disk's name
        """
        self.name = disk
        self.sector_size = int(test_utils.cat_data("/sys/block/{}/queue/hw_sector_size".format(disk)))
        self.system_path = test_utils.ls_path("/dev/{}".format(disk))
        self.num_of_sectors = int(test_utils.cat_data("/sys/block/{}/size".format(disk)))
        self.removable = test_utils.cat_data_boolean("/sys/block/{}/removable".format(disk))
        self.vendor = test_utils.cat_data("/sys/block/{}/device/vendor".format(disk))
        self.space = self.sector_size * self.num_of_sectors
        self.children = []


class SystemDiskFormatted(SystemDisk):
    """ Contains formatted disk object as well as data related to this
        object"""
    def __init__(self, disk):
        test_utils.create_new_alloc_table(disk)
        self.alloc_type = test_utils.get_alloc_type(disk)


class SystemPartition(object):
    """ Contains data regarding to a partition.
        This object defines what is a partition and what kind of data are
        related to a partition."""
    def __init__(self, disk, part_num):
        """
            :param str disk: disk's name
            :param int part_num: partition number
        """
        self.name = "{}{}".format(disk, part_num)
        self.system_path = test_utils.ls_path("/dev/{}{}".format(disk, part_num))
        self.part_num_of_sectors = int(test_utils.cat_data("/sys/block/{}/{}{}/size".format(disk, disk, part_num)))
        self.part_type = None
        self.part_start = None
        self.part_end = None
        self.parent = disk


class BlivetDisk(object):
    """ Contains data related to a disk,
        how Blivet recognizes it."""
    def __init__(self, disk):
        """
            :param str disk: disk's name
        """
        self.b_object = blivet_test_utils.init_blivet()
        self.b_object.reset()
        self.b_disk = blivet_test_utils.get_dev_by_name(self.b_object, disk)
        self.b_name = self.b_disk.name
        self.b_system_path = self.b_disk.path
        self.b_removable = self.b_disk.removable
        self.b_vendor = self.b_disk.vendor
        self.b_model = self.b_disk.model
        self.b_space = int(self.b_disk.size)
        self.b_children = []


class BlivetDiskFormatted(BlivetDisk):
    """ Contains gathered information by Blivet related to formatted
        disk."""
    def __init__(self):
        self.b_alloc_type = self.b_disk.format.partedDisk.type

class BlivetPartition(object):
    """ Contains data related to partitions, as Blivet recognizes it."""
    def __init__(self, disk):
        """
            :param str disk: disk's name
        """
        ## TODO: Complete
        self.b_name = None
        self.b_system_path = None
        self.b_num_of_sectors = None
        self.b_part_type = None
        self.b_part_start = None
        self.b_part_end = None
        self.parent = None
        
