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
import blivet_utils


class BlivetInitialization(object):
    """ This basic class initializes Blivet and returns
        Blivet object, performs Blivet().reset()"""
    def __init__(self, disk, child_index = None, stage_num = None):
        """
            :param str disk: disk's name
            :param bool child: If TRUE, get disk's partition / child object
            :param int child_index: If child is TRUE, then this is index of a child object
        """
        super(BlivetInitialization, self).__init__()
        self.object = blivet_utils.init_blivet_basic()
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
        self.sc_bare_name = d_name
        self.sc_bare_path = test_utils.ls_path("/dev/{}".format(self.sc_bare_name))
        self.sc_bare_remb = test_utils.cat_data_boolean("/sys/block/{}/removable".format(self.sc_bare_name))
        self.sc_bare_vend = test_utils.cat_data("/sys/block/{}/device/vendor".format(self.sc_bare_name))
        self.sc_bare_sys_pat = test_utils.get_data_head(self.sc_bare_name)
        self.sc_bare_sec_siz = int(test_utils.cat_data("/sys/block/{}/queue/hw_sector_size".format(self.sc_bare_name)))
        self.sc_bare_num_sec = int(test_utils.cat_data("/sys/block/{}/size".format(self.sc_bare_name)))
        self.sc_bare_size = self.sc_bare_num_sec * int(test_utils.cat_data("/sys/block/{}/queue/hw_sector_size".format(self.sc_bare_name)))

    def get_attributes(self):
        return [("sc_bare_name", "name"), ("sc_bare_path", "path"), ("sc_bare_remb", "removable"), ("sc_bare_vend", "vendor"), ("sc_bare_sys_pat", "sysfsPath"), ("sc_bare_size", "size"), ("sc_bare_sec_siz", "format.partedDevice.sectorSize"), ("sc_bare_num_sec", "format.partedDevice.length")]

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
        self.sc_dfor_type = test_utils.get_alloc_type(self.sc_bare_name)
        self.sc_dfor_uuid = test_utils.get_disk_props(self.sc_bare_name, 1)

    def get_attributes(self):
        return [("sc_dfor_type", "format.partedDisk.type"), ("sc_dfor_uuid", "format.uuid")]


class SystemPartition_Scan(SystemDiskFormatted_Scan):
    """ Creates a partition using system tool and creates a object with
        related data."""
    def __init__(self, d_name, part_num):
        """
            :param str disk: disk's name
            :param int part_num: disk's partition number
        """
        super(SystemPartition_Scan, self).__init__(d_name)

        self.sc_part_name = "{}{}".format(self.sc_bare_name, part_num)
        self.sc_part_uuid = test_utils.get_disk_props(self.sc_part_name, 1)
        self.sc_part_num_sec = int(test_utils.get_data_fdisk(self.sc_part_name, 3))
        self.sc_part_str_sec = int(test_utils.get_data_fdisk(self.sc_part_name, 1))
        self.sc_part_end_sec = int(test_utils.get_data_fdisk(self.sc_part_name, 2))
        self.sc_part_size = self.sc_bare_sec_siz * self.sc_part_num_sec

    def get_attributes(self):
        return [("sc_part_name", "name"), ("sc_part_uuid", "format.uuid"), ("sc_part_num_sec", "partedPartition.geometry.length"), ("sc_part_str_sec", "partedPartition.geometry.start"), ("sc_part_end_sec", "partedPartition.geometry.end"), ("sc_part_size", "size")]


class SystemPartitionFormatted_Scan(SystemPartition_Scan):
    """ Docstring here"""
    def __init__(self, d_name, part_num):
        """
            :param str d_name: disk's name
            :param int part_num: partition number
        """
        super(SystemPartitionFormatted_Scan, self).__init__(d_name, part_num)
        self.sc_part_for_format = test_utils.get_disk_props(self.sc_part_name, 3)
        self.sc_part_for_uuid = test_utils.get_disk_props(self.sc_part_name, 1)

    def get_attributes(self):
        return [("sc_part_for_format", "format.type"), ("sc_part_for_uuid", "format.uuid")]


class SystemExtended_Scan(SystemPartition_Scan):
    """ docstring for SystemExtended_Scan"""
    def __init__(self, d_name, part_num):
        """
            :param str d_name: disk's name
            :param int part_num: partition number
        """
        super(SystemExtended_Scan, self).__init__(d_name, part_num)
        self.sc_ex_name = "{}{}".format(d_name, part_num)
        self.sc_ex_uuid = test_utils.get_disk_props(self.sc_ex_name, 1)
        self.sc_ex_bool = None
        self.sc_ex_num_sec = int(test_utils.get_data_fdisk(self.sc_ex_name, 3))
        self.sc_ex_str_sec = int(test_utils.get_data_fdisk(self.sc_ex_name, 1))
        self.sc_ex_end_sec = int(test_utils.get_data_fdisk(self.sc_ex_name, 2))
        self.sc_ex_size = self.sc_bare_sec_siz * self.sc_ex_num_sec

    def get_attributes(self):
        return [("sc_ex_name", "name"), ("sc_ex_uuid", "format.uuid"), ("sc_ex_bool", "isExtended"), ("sc_ex_num_sec", "partedPartition.geometry.length"), ("sc_ex_str_sec", "partedPartition.geometry.start"), ("sc_ex_end_sec", "partedPartition.geometry.end"), ("sc_ex_size", "size")]


class SystemLogical_Scan(SystemExtended_Scan):
    """ docstring"""
    def __init__(self, d_name, part_num, logical_p_num):
        """
            :param str d_name: disk's name
        """
        super(SystemLogical_Scan, self).__init__(d_name, part_num)
        self.sc_lv_name = "{}{}".format(d_name, logical_p_num)
        self.sc_lv_uuid = test_utils.get_disk_props(self.sc_lv_name, 1)
        self.sc_lv_type = None
        self.sc_lv_num_sec = int(test_utils.get_data_fdisk(self.sc_lv_name, 3))
        self.sc_lv_str_sec = int(test_utils.get_data_fdisk(self.sc_lv_name, 1))
        self.sc_lv_end_sec = int(test_utils.get_data_fdisk(self.sc_lv_name, 2))
        self.sc_lv_size = self.sc_bare_sec_siz * self.sc_lv_num_sec

    def get_attributes(self):
        return [("sc_lv_name", "name"), ("sc_lv_uuid", "format.uuid"), ("sc_lv_num_sec", "partedPartition.geometry.length"), ("sc_lv_str_sec", "partedPartition.geometry.start"), ("sc_lv_end_sec", "partedPartition.geometry.end"), ("sc_lv_size", "size")]


class System_LVMBasic_Scan(SystemPartition_Scan):
    """ docstring for System_LVMBasic_Scan"""
    def __init__(self, disk, part_num):
        """
            :param str disk: disk's name
            :param int part_num: number of partition
        """
        super(System_LVMBasic_Scan, self).__init__(disk, part_num)
        self.sc_lvm_pv_name = "{}{}".format(disk, part_num)
        self.sc_lvm_pv_uuid = test_utils.get_disk_props(self.sc_lvm_pv_name, 1)
        self.sc_lvm_pv_part_uuid = test_utils.get_disk_props(self.sc_lvm_pv_name, 5)
        self.sc_lvm_pv_bool = False
        self.sc_lvm_pv_size = int(test_utils.cat_data("/sys/block/{}/{}/size".format(disk, self.sc_lvm_pv_name))) * self.sc_bare_sec_siz
        self.sc_lvm_pv_type = test_utils.get_disk_props(self.sc_lvm_pv_name, 3)

    def get_attributes(self):
        return [(("sc_lvm_pv_name", "name"), ("sc_lvm_pv_uuid", "format.uuid"), ("sc_lvm_pv_size", "size"), ("sc_lvm_pv_type", "format.type"))]
