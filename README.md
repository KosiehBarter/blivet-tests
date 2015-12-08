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

[UPDATE]
GitHubURL = https://github/your/custom/url
GitHubBranch = your branch name
GitHubDestDir = /your/dest/in/vm
GitHubDepthNum = 1
```

A little bit of explanation:
MachineName - your machine's name.
MachineRam - How much the machine will have MB of ram?
MachineNoOfDisks - Number, how much additional disks (machine creates one by default) will machine have.
MachineSnapshotName - Your snapshot's name. Note: A fall-back snapshot at the end of installation is created automatically, based on your snapshot name. Don't forget it to set it!

MachineInstallPath - where your machine will be installed. Handy, if you need to install on non-system disk. Don't forget to add a ending slash!
MachinePathToKickstart - A URL where is your kickstart file. See example.ks form details.
MachinePathToISO - Where is your install ISO? Full path, including the iso extension.
MachineCopySource - This is a location, where you actually downloaded this package, which contains tests and test_deps folders.

GitHubURL - GitHub URL to a Blivet repo.
GitHubBranch - a specific branch to download from.
GitHubDestDir - a directory inside virtual machine to download to. Also, don't forget to add ending slash!
GitHubDepthNum - Specific depth of the repo.

Note that MachineRam and MachineNoOfDisks are numbers. MachineRam is in Megabytes.

# Starting the machine:
To start the machine, run (with sudo or as root!) python3 Execute_test.py -i \<your_file_with_extension.ini\>. This will run the installation. Also, it will automatically generate run_update.sh based on your INI settings for specific update proccess.

# WIKI for creating tests:
https://github.com/KosiehBarter/blivet-tests/wiki

# Depedencies / Requirements:
* python3
* virsh
* virt-install (part of virsh)
* ssh + scp + ssh-keygen

# Note: This guide is in development, so tools will be added and there is possibility, that some tools in repository will be changed.
