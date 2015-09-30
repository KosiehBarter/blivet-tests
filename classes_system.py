### Classes definition - System
### Part of: Blivet test collection
### Author: kvalek@redhat.com
### This program is under GPL licence.

"""
    Basic class definitions for tests for Blivet. This is system-tool part
    (only system tools are used here).
    This program contains operations for modifying disk (using system tools)
    and scanning (what Blivet performs in classes_blivet.py).
"""

import test_utils
import blivet_test_utils

class SystemDisk_Exe(object):
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

    def get_attributes(self):
        return ["name", "sector_size"]


class SystemDiskFormatted_Exe(SystemDisk_Exe):
    """ Contains formatted disk object as well as data related to this
        object"""
    def __init__(self, disk):
        """
            :param str disk: disk's name
        """
        super(SystemDiskFormatted_Exe, self).__init__(disk)
        test_utils.create_new_alloc_table(self.name, 'msdos')
        test_utils.create_new_alloc_table(self.name)
        self.alloc_type = test_utils.get_alloc_type(self.name)
        self.disk_uuid = test_utils.get_disk_uuid(self.name)


class SystemPartition_Exe(SystemDiskFormatted_Exe):
    """ Creates a partition using system tool and creates a object with
        related data."""
    def __init__(self, disk, part_num):
        """
            :param str disk: disk's name
            :param int part_num: disk's partition number
            :param int part_start: Start sector of the partition. See size_type.
            :param int part_end: End sector of the partition. See size_type.
            :param str size_type: Type of size (MiB, GiB, etc.)
            :param str part_type: Partition type. Types: primary, extended, logical
        """
        super(SystemPartition_Exe, self).__init__(disk)

        self.sd_part_name = "{}{}".format(self.name, part_num)
        self.sd_part_uuid = test_utils.get_disk_uuid(self.name, 1)
        self.sd_part_size = int(test_utils.cat_data("/sys/block/{}/{}{}/size".format(self.name, self.sd_part_name))) * self.num_of_sectors
        self.sd_part_start = int(test_utils.cat_data("/sys/block/{}/{}{}/start".format(self.name, self.sd_part_name)))
        self.sd_part_end = self.sd_part_size + 2048


class SystemPartitionFormatted_Exe(SystemPartition):
    """ Docstring here"""
    def __init__(self, disk, part_num, format):
        """
            :param str
        """
        super(SystemPartitionFormatted_Exe, self).__init__(disk, part_num)
        self.sd_part_for_format = None
        self.sd_part_for_uuid = None


class SystemExtended_Exe(SystemDiskFormatted_Exe):
    """ docstring for SystemExtended_Exe"""
    def __init__(self, disk):
        """
            :param
        """
        super(SystemExtended_Exe, self).__init__(disk)
        self.sd_ex_name = None
        self.sd_ex_uuid = None
        self.sd_ex_type = None
        self.sd_ex_size = None
        self.sd_ex_strt = None
        self.sd_ex_end = None
        self.sd_ex_logv = None


class SystemLogical_Exe(SystemExtended_Exe):
    """ docstring"""
    def __init__(self, disk, logv_num):
        """
            :param
        """
        super(SystemLogical_Exe, self).__init__(disk)
        self.sd_lv_name = None
        self.sd_lv_uuid = None
        self.sd_lv_type = None
        self.sd_lv_size = None
        self.sd_lv_strt = None
        self.sd_lv_end = None
        self.sd_lv_logv = None
