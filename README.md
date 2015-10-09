# blivet-tests

This package is designed to perform specific tests regarding to Blivet and also includes automatic machine creation as well as testing inside machine.

Main file is classes.py, where are objects. These objects are created automatically after start. All values are gathered and computed automatically as well as compared.

# How to:
Firstly, modify Execute_test to suit your needs and your system, mainly paths and ssh keys. Also, do not forget to set up your kickstart file.

Then run the script with python3 as root or with sudo to start automatic machine creation. The machine will be created and automatic kickstart installation will start. The virtual machine is reachable with vncviewer or any vnc client with localhost:0.

After install, there is a automatic dynamic timer, which will wait for installation completion and will initiate tests written in test_arrays.py, which includes classes.py as a object for comparation.

There are several tools, test_utils.py and test_utils_blivet.py. Both files include basic gather tools for system and blivet respectively.

Note that in Execute_test, at the begining, there are some constants, which can be altered for your needs.
A small documentation:
* machine_name - name of machine and installation.
* machine_full_path - path, where are stored virtual disks.
* machine_ks_full_path - kickstart file location, can be URL or local file. NOTE: must be full path
* machine_iso_full_path - same as machine_full_path, but iso. Include the file with extension!
* machine_snap_name - custom name for main snapshot.

* ssh_full_path - full path to private key to allow automatic test
* scp_copy_source - path to directory, where are stored all test files (including tools)

# Depedencies / Requirements:
* python3
* virsh
* virt-install (part of virsh)
* ssh + scp + ssh-keygen

# Note: This guide is in development, so tools will be added and there is possibility, that some tools in repository will be changed.
