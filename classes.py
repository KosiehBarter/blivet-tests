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

    def get_attributes(self):
        return ["name", "sector_size"]


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
        self.disk_uuid = get_disk_uuid(self.name)


class SystemPartition(SystemDisk):
    """ Creates a partition using system tool and creates a object with
        related data."""
    def __init__(self, arg):
        """
            :param
        """
        super(SystemPartition, self).__init__()
        self.sd_part_name = "{}{}".format(self.name, part_num)
        self.sd_part_uuid = test_utils.get_disk_uuid(self.sd_part_name)
        self.sd_part_size = int(test_utils.cat_data("/sys/block/{}/{}{}/size".format(self.name, self.sd_part_name))) * self.num_of_sectors
        self.sd_part_start = int(test_utils.cat_data("/sys/block/{}/{}{}/start".format(self.name, self.sd_part_name)))
        self.sd_part_end = self.sd_part_size + 2048




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


class BlivetDisk(BlivetInitialization):
    """ Contains data related to a disk,
        how Blivet recognizes it."""
    def __init__(self, disk):
        """
            :param str disk: disk's name
        """
        super(BlivetDisk, self).__init__(disk)
        self.b_name = self.b_disk.name
        self.b_system_path = self.b_disk.path
        self.b_removable = self.b_disk.removable
        self.b_vendor = self.b_disk.vendor
        self.b_model = self.b_disk.model
        self.b_space = int(self.b_disk.size)


class BlivetDiskFormatted(BlivetDisk):
    """ Contains gathered information by Blivet related to formatted
        disk."""
    def __init__(self, disk):
        """
            :param str disk: disk's name
        """
        super(BlivetDiskFormatted, self).__init__(disk)
        self.b_alloc_type = self.b_disk.format.partedDisk.type
        self.b_disk_uuid = self.b_disk.uuid


class BlivetPartition(BlivetDisk):
    """ Object containing basic partition info."""
    def __init__(self, arg):
        super(BlivetPartition, self).__init__()
        self.bd_part_name = blivet_test_utils.get_dev_kids(self.b_disk)[part_num].name
        self.bd_part_uuid = blivet_test_utils.get_dev_kids(self.b_disk)[part_num].format.uuid
        self.bd_part_size = blivet_test_utils.get_dev_kids(self.b_disk)[part_num].size
        self.bd_part_start = blivet_test_utils.get_dev_kids(self.b_disk)[part_num].
