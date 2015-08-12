### Single disk - single partition
### Part of: Blivet test collection
### Author: kvalek@redhat.com
### All programs I create are under GPL license.
import test_utils
import blivet_test_utils
import checker_test_utils

class SystemDisk(object): # Uppercase znaky nevadi, bez podtrzitek
    """SystemDisk class contains all data regarding to a disk.
    At start, a "disk" parameter is received. Based on this parameter,
    all required data are gathered."""
    def __init__(self, disk):
        """
        
        :param str disk: disk's name
        """
        self.name = disk # Disk name
        self.sector_size = int(test_utils.cat_data("/sys/block/{}/queue/hw_sector_size".format(disk))) # disk sector size
        self.num_of_sectors = int(test_utils.cat_data("/sys/block/{}/size".format(disk))) # Disk num of sectors
        self.system_path = test_utils.ls_path("/dev/{}".format(disk)) # Disk system path
        self.removable = int(test_utils.cat_data("/sys/block/{}/removable".format(disk))) # Removable disk?
        self.vendor = test_utils.cat_data("/sys/block/{}/device/vendor".format(disk)) # Disk vendor
        self.model = test_utils.cat_data("/sys/block/{}/device/vendor".format(disk)) # Disk model
        self.serial_num = None     # Disk S/N
        self.space = self.sector_size * self.num_of_sectors # Disk size
        self.children = []

class SystemPartition(object):
    def __init__(self, disk, part_num):
        self.name = "{}{}".format(disk, part_num)
        self.num_of_sectors = None
        self.system_path = None
        self.space = None
        self.parent = disk


