# blivet-tests

This package is designed to perform specific tests regarding to Blivet and also includes automatic machine creation as well as testing inside machine.

Main file is classes.py, where are objects. These objects are created automatically after start. All values are gathered and computed automatically as well as compared.

# How to:
Run virtual_machine.py as root or with sudo to start automatic machine creation. The machine will be created and automatic kickstart installation will start. The virtual machine is reachable with vncviewer or any vnc client with localhost:0.

After install, there is a automatic dynamic timer, which will wait for installation completion and will initiate tests written in test_arrays.py, which includes classes.py as a object for comparation.

There are several tools, test_utils.py and test_utils_blivet.py. Both files include basic gather tools for system and blivet respectively.

# Note: This guide is in development, so tools will be added and there is possibility, that some tools in repository will be changed.
