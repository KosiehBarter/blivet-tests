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
    def __init__(self, disk, child_index = None):
        """
            :param str disk: disk's name
            :param bool child: If TRUE, get disk's partition / child object
            :param int child_index: If child is TRUE, then this is index of a child object
        """
        super(BlivetInitialization, self).__init__()
        self.object = blivet.Blivet()
        self.object.reset()
        self.disk = self.object.devicetree.getDeviceByName(disk)
        if child_index != None:
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
        return ["name", "path", "removable", "vendor", "sysfsPath", "size"]

    def rec_getattr(self, obj_inst, attr_name):
        return reduce(getattr, attr_name.split("."), obj_inst)


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
    def __init__(self, d_name, part_num):
        """
            :param str d_name: disk's name
            :param int part_num: partition number
        """
        super(SystemPartitionFormatted_Scan, self).__init__(d_name, part_num)
        self.sd_part_for_format = test_utils.get_disk_props(self.p_name, 3)
        self.sd_part_for_uuid = test_utils.get_disk_props(self.p_name, 1)

    def get_attributes(self):
        return [("sd_part_for_format", "format.type"), ("sd_part_for_uuid", "format.uuid")]


class SystemExtended_Scan(SystemPartition_Scan):
    """ docstring for SystemExtended_Scan"""
    def __init__(self, d_name, part_num):
        """
            :param str d_name: disk's name
            :param int part_num: partition number
        """
        super(SystemExtended_Scan, self).__init__(d_name, part_num)
        self.sd_ex_name = "{}{}".format(d_name, part_num)
        self.sd_ex_uuid = test_utils.get_disk_props(self.sd_ex_name, 3)
        self.sd_ex_bool = None
        self.sd_ex_size = int(test_utils.cat_data("/sys/block/{}/{}/size".format(self.name, self.sd_ex_name))) * self.p_num_of_sectors
        self.sd_ex_strt = int(test_utils.cat_data("/sys/block/{}/{}/start".format(self.name, self.sd_ex_name)))
        self.sd_ex_pend = self.sd_ex_strt + self.p_num_of_sectors

    def get_attributes(self):
        return [("sd_ex_name", "name"), ("sd_ex_uuid", "uuid"), ("sd_ex_bool", "isExtended"), ("sd_ex_size", "size"), ("sd_ex_strt", "partedPartition.geometry.start"), ("sd_ex_pend", "partedPartition.geometry.end")]


class SystemLogical_Scan(SystemExtended_Scan):
    """ docstring"""
    def __init__(self, d_name, part_num):
        """
            :param
        """
        super(SystemLogical_Scan, self).__init__(d_name, part_num)
        self.sd_lv_name = "{}{}".format(d_name, test_utils.assign_logical_number(d_name, part_num))
        self.sd_lv_logn = test_utils.assign_logical_number(d_name, part_num)
        self.sd_lv_uuid = None #test_utils.get_disk_props(self.sd_lv_name, 1)
        self.sd_lv_type = None
        self.sd_lv_nsec = None
        self.sd_lv_size = int(test_utils.cat_data("/sys/block/{}/{}/size".format(self.name, self.sd_lv_name)))
        self.sd_lv_strt = int(test_utils.cat_data("/sys/block/{}/{}/start".format(self.name, self.sd_lv_name)))
        self.sd_lv_pend = None #self.sd_lv_strt + self.sd_lv_nsec

    def get_attributes(self):
        return [("sd_lv_name", "name"), ("sd_lv_uuid", "uuid"), ("sd_lv_size", "size"), ("sd_lv_strt", "partedPartition.geometry.start"), ("sd_lv_pend", "partedPartition.geometry.end")]
