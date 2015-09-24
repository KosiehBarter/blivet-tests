# blivet-tests

This package is designed to perform specific tests regarding to Blivet and also includes automatic machine creation as well as testing inside machine.

Main file is classes.py, where are objects. These objects are created automatically after start. All values are gathered and computed automatically as well as compared.

# How to:
Run virtual_machine.py as root or with sudo to start automatic machine creation. The machine will be created and automatic kickstart installation will start. The virtual machine is reachable with vncviewer or any vnc client with localhost:0.

After install, there is a automatic dynamic timer, which will wait for installation completion and will initiate tests written in test_arrays.py, which includes classes.py as a object for comparation.

There are several tools, test_utils.py and test_utils_blivet.py. Both files include basic gather tools for system and blivet respectively.

Note that in virtual_machine.py, at the begining, there are some constants, which can be altered for your needs.
A small documentation:
* install_name - name of machine and installation.
* install_disk - a iso, which is used for installation. You can specify your own.
* full_disk_path_1 - same as install_disk, but for disk. You can specify your own, but you have to manually create dirs if needed.
* full_loc_path - same as before.

* ks_file_path - kickstart file, can be URL or local. URL is preffered.
* key_location - your own ssh key. You have to create your own.
* ram_size - amount of machine memory, in MB.
* scp_source - source for tests, have to be set manually.

# Depedencies / Requirements:
* python3
* virsh
* virt-install (part of virsh?)
* ssh + scp + ssh-keygen


# Note: This guide is in development, so tools will be added and there is possibility, that some tools in repository will be changed.
