### Classes definition - Blivet
### Part of: Blivet test collection
### Author: kvalek@redhat.com
### This program is under GPL licence.

"""
    Basic class definitions for tests for Blivet. This program contains Blivet
    tools.
    This program executes scanning (what system does to disks) and modifying
    (Blivet performs disk operations which are scanned by system)
"""

import blivet_test_utils

class BlivetInitialization(object):
    """ This basic class initializes Blivet and returns
        Blivet object, performs Blivet().reset()"""
    def __init__(self, disk):
        """
            Initialize Blivet.
        """
        super(BlivetInitialization, self).__init__()
        self.b_object = blivet_test_utils.init_blivet()
        self.b_object.reset()
        self.b_disk = blivet_test_utils.get_dev_by_name(self.b_object, disk)


class BlivetDisk_Scan(BlivetInitialization):
    """ Contains data related to a disk,
        how Blivet recognizes it."""
    def __init__(self, disk):
        """
            :param str disk: disk's name
        """
        super(BlivetDisk_Scan, self).__init__(disk)
        self.b_name = self.b_disk.name
        self.b_system_path = self.b_disk.path
        self.b_removable = self.b_disk.removable
        self.b_vendor = self.b_disk.vendor
        self.b_model = self.b_disk.model
        self.b_space = int(self.b_disk.size)


class BlivetDiskFormatted_Scan(BlivetDisk_Scan):
    """ Contains gathered information by Blivet related to formatted
        disk."""
    def __init__(self, disk):
        """
            :param str disk: disk's name
        """
        super(BlivetDiskFormatted_Scan, self).__init__(disk)
        self.b_alloc_type = self.b_disk.format.partedDisk.type
        self.b_disk_uuid = self.b_disk.uuid


class BlivetPartition_Scan(BlivetDiskFormatted_Scan):
    """ Object containing basic partition info."""
    def __init__(self, disk, part_num):
        super(BlivetPartition_Scan, self).__init__(disk)
        self.bd_part_obj = blivet_test_utils.get_dev_kids(self.b_object, self.b_disk, part_num)

        self.bd_part_name = self.bd_part_obj.name
        self.bd_part_uuid = self.bd_part_obj.format.uuid
        self.bd_part_size = self.bd_part_obj.size
        self.bd_part_start = self.bd_part_obj.partedPartition.geometry.start
        self.bd_part_end = self.bd_part_obj.partedPartition.geometry.end


class BlivetPartitionFormatted_Scan(BlivetPartition_Scan):
    """ docstring"""
    def __init__(self, disk, part_num):
        """
            :param
        """
        super(BlivetPartitionFormatted_Scan, self).__init__(disk, part_num)
        self.bd_part_for_format = self.bd_part_obj[part_num].format.type
        self.bd_part_for_uuid = self.bd_part_obj[part_num].format.uuid


class BlivetExtended_Scan(BlivetDiskFormatted_Scan):
    """ docstring"""
    def __init__(self, disk):
        """
            :param
        """
        super(BlivetExtended_Scan, self).__init__(disk)
        self.bd_ex_uuid = None
        self.bd_ex_name = None
        self.bd_ex_type = None
        self.bd_ex_size = None
        self.bd_ex_strt = None
        self.bd_ex_end = None
        self.bd_ex_logv = None


class BlivetLogical_Scan(BlivetExtended_Scan):
    """ docstring"""
    def __init__(self, disk, lvol_num):
        """
            :param
        """
        super(BlivetLogical_Scan, self).__init__(disk)
        self.bd_lv_name = None
        self.bd_lv_uuid = None
        self.bd_lv_type = None
        self.bd_lv_size = None
        self.bd_lv_strt = None
        self.bd_lv_end = None
        self.bd_lv_logv = None
