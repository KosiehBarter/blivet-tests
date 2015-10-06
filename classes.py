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
import blivet


class BlivetInitialization(object):
    """ This basic class initializes Blivet and returns
        Blivet object, performs Blivet().reset()"""
    def __init__(self, disk, child_index = 1):
        """
            :param str disk: disk's name
            :param bool child: If TRUE, get disk's partition / child object
            :param int child_index: If child is TRUE, then this is index of a child object
        """
        super(BlivetInitialization, self).__init__()
        self.object = blivet.Blivet()
        self.object.reset()
        self.disk = self.object.devicetree.getDeviceByName(disk)
        self.child = self.object.devicetree.getChildren(self.disk)[child_index - 1]


class SystemDisk_Scan(object):
    """ Contains all data regarding to a disk.
        At start, a "disk" parameter is received. Based on this parameter,
        all required data are gathered."""
    def __init__(self, d_name):
        """
            :param str d_name: disk's name
        """
        self.name = d_name
        self.path = test_utils.ls_path("/dev/{}".format(self.name))
        self.removable = test_utils.cat_data_boolean("/sys/block/{}/removable".format(self.name))
        self.vendor = test_utils.cat_data("/sys/block/{}/device/vendor".format(self.name))
        self.sysfsPath = test_utils.get_data_head(self.name)
        self.size = int(test_utils.cat_data("/sys/block/{}/size".format(self.name))) * int(test_utils.cat_data("/sys/block/{}/queue/hw_sector_size".format(self.name)))
        self.sector_size = int(test_utils.cat_data("/sys/block/{}/queue/hw_sector_size".format(self.name)))

    def get_attributes(self):
        return ["name", "path", "removable", "vendor", "sysfsPath", "size", ("sector_size", "int(format.sectorSize)")]


class SystemDiskFormatted_Scan(SystemDisk_Scan):
    """ Contains formatted disk object as well as data related to this
        object"""
    def __init__(self, d_name):
        """
            :param str d_name: disk's name
        """
        super(SystemDiskFormatted_Scan, self).__init__(d_name)
        self.fpPtype = test_utils.get_alloc_type(self.name)
        self.uuid = test_utils.get_disk_props(self.name, 1)

    def get_attributes(self):
        return [("fpPtype", "format.partedDisk.type"), "uuid"]


class SystemPartition_Scan(SystemDiskFormatted_Scan):
    """ Creates a partition using system tool and creates a object with
        related data."""
    def __init__(self, d_name, part_num):
        """
            :param str disk: disk's name
            :param int part_num: disk's partition number
        """
        super(SystemPartition_Scan, self).__init__(d_name)

        self.p_name = "{}{}".format(self.name, part_num)
        self.p_uuid = test_utils.get_disk_props(self.p_name, 1)
        self.p_num_of_sectors = int(test_utils.cat_data("/sys/block/{}/{}/size".format(self.name, self.p_name)))
        self.p_size = self.sector_size * self.p_num_of_sectors
        self.p_P_g_start = int(test_utils.cat_data("/sys/block/{}/{}/start".format(self.name, self.p_name)))
        self.p_P_g_end = self.p_P_g_start + self.p_num_of_sectors

    def get_attributes(self):
        return [("p_name", "name"), ("p_uuid", "format.uuid"), ("p_P_g_start", "partedPartition.geometry.start"), ("p_P_g_end", "partedPartition.geometry.end")]


class SystemPartitionFormatted_Scan(SystemPartition_Scan):
    """ Docstring here"""
    def __init__(self, d_name, part_num, format):
        """
            :param str
        """
        super(SystemPartitionFormatted_Scan, self).__init__(d_name, part_num)
        self.sd_part_for_format = test_utils.get_disk_props(sd_part_name, 3)
        self.sd_part_for_uuid = test_utils.get_disk_props(sd_part_name, 1)


class SystemExtended_Scan(SystemDiskFormatted_Scan):
    """ docstring for SystemExtended_Scan"""
    def __init__(self, d_name):
        """
            :param
        """
        super(SystemExtended_Scan, self).__init__(disk)
        self.sd_ex_name = None
        self.sd_ex_uuid = None
        self.sd_ex_type = None
        self.sd_ex_size = None
        self.sd_ex_strt = None
        self.sd_ex_end = None
        self.sd_ex_logv = None


class SystemLogical_Scan(SystemExtended_Scan):
    """ docstring"""
    def __init__(self, d_name, logv_num):
        """
            :param
        """
        super(SystemLogical_Scan, self).__init__(disk)
        self.sd_lv_name = None
        self.sd_lv_uuid = None
        self.sd_lv_type = None
        self.sd_lv_size = None
        self.sd_lv_strt = None
        self.sd_lv_end = None
        self.sd_lv_logv = None
