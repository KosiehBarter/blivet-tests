# blivet-tests

This package is designed to perform specific tests regarding to Blivet and also includes automatic machine creation as well as testing inside machine.

Main file is classes.py, where are objects. These objects are created automatically after start. All values are gathered and computed automatically as well as compared.

# How to:
Firstly, modify Execute_test to suit your needs and your system, mainly paths and ssh keys. Also, do not forget to set up your kickstart file.

Then run the script with python3 as root or with sudo to start automatic machine creation. The machine will be created and automatic kickstart installation will start. The virtual machine is reachable with vncviewer or any vnc client with localhost:0.

After install, there is a automatic dynamic timer, which will wait for installation completion and will initiate tests written in test_arrays.py, which includes classes.py as a object for comparation.

There are several tools, test_utils.py and test_utils_blivet.py. Both files include basic gather tools for system and blivet respectively.

You have to create your own custom \*.ini file which will include following:
```
[MACHINE]
MachineName = YourMachineName
MachineRam = 2048
MachineNoOfDisks = 3
MachineSnapshotName = MySnapshot

[PATHS]
MachineInstallPath = /your/install/path/
MachinePathToKickstart = http://your.server/kickstart.ks
MachinePathToISO = /your/path/to/cd_image.iso
MachineCopySource = /your/path/where/files/will/be/copied/from/

```

Note that MachineRam and MachineNoOfDisks are numbers. MachineRam is in Megabytes.

# Starting the machine:
To start the machine, run (with sudo or as root!) python3 Execute_test.py -i \<your_file_with_extension.ini\>. This will run the installation.

# WIKI for creating tests:
https://github.com/KosiehBarter/blivet-tests/wiki

# Depedencies / Requirements:
* python3
* virsh
* virt-install (part of virsh)
* ssh + scp + ssh-keygen

# Note: This guide is in development, so tools will be added and there is possibility, that some tools in repository will be changed.
