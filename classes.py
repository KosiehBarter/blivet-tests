### Classes definition
### Part of: Blivet test collection
### Author: kvalek@redhat.com
### This program is under GPL licence.

"""
    Basic class definitions for tests related to Blivet recognition
    engine.
"""

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
        self.sector_size = int(test_utils.cat_data("/sys/block/{}/queue/hw_sector_size".format(self.name)))
        self.system_path = test_utils.ls_path("/dev/{}".format(self.name))
        self.num_of_sectors = int(test_utils.cat_data("/sys/block/{}/size".format(self.name)))
        self.removable = test_utils.cat_data_boolean("/sys/block/{}/removable".format(self.name))
        self.vendor = test_utils.cat_data("/sys/block/{}/device/vendor".format(self.name))
        self.space = self.sector_size * self.num_of_sectors
        self.children = None


class SystemDiskFormatted(SystemDisk):
    """ Contains formatted disk object as well as data related to this
        object"""
    def __init__(self, disk):
        """
            :param str disk: disk's name
        """
        super(SystemDiskFormatted, self).__init__(disk)
        test_utils.create_new_alloc_table(self.name, 'msdos')
        test_utils.create_new_alloc_table(self.name)
        self.alloc_type = test_utils.get_alloc_type(self.name)


class SystemPartition(SystemDisk):
    """ Contains data regarding to a partition.
        This object defines what is a partition and what kind of data are
        related to a partition."""
    def __init__(self, disk, part_num):
        """
            :param str disk: disk's name
            :param int part_num: partition number
        """
        super(SystemPartition, self).__init__(disk)
        self.name = "{}{}".format(disk, part_num)
        self.system_path = test_utils.ls_path("/dev/{}{}".format(disk, part_num))
        self.part_num_of_sectors = int(test_utils.cat_data("/sys/block/{}/{}{}/size".format(disk, disk, part_num)))
        self.part_type = 
        self.part_start = test_utils.get_part_block(self.name, 'first')
        self.part_end = test_utils.get_part_block(self.name, 'last')
        self.part_sector_size = 
        self.part_size = self.part_num_of_sectors * self.part_sector_size
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
        self.b_children = None


class BlivetDiskFormatted(BlivetDisk):
    """ Contains gathered information by Blivet related to formatted
        disk."""
    def __init__(self, disk):
        """
            :param str disk: disk's name
        """
        super(BlivetDiskFormatted, self).__init__(disk)
        self.b_alloc_type = self.b_disk.format.partedDisk.type

class BlivetPartition(BlivetDisk):
    """ Contains data related to partitions, as Blivet recognizes it."""
    def __init__(self, disk, partition):
        """
            :param str disk: disk's name
        """
        super(BlivetPartition, self).__init__(disk)
        self.b_part_name = disk.name
        self.b_part_system_path = disk.path
        self.b_part_format = disk.format.type
        self.b_part_size = int(disk.size)
        self.b_part_start = None    # FIXME
        self.b_part_end = None      # FIXME
        self.b_parent = disk
