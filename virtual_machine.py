### Test utils - Blivet
### Part of: Blivet test collection
### Author: kvalek@redhat.com
### This program is under GPL licence.

import subprocess

subprocess.call(["virt-install", "--name", "{}".format(mach_name), "--disk",\
 "{}".format(full_disk_path), "--location", "{}".format(full_loc_path),\
 "--ram", "{}".format(ram_size), "-x", "{}".format(ks_file_path)])
