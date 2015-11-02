#version=DEVEL
url --url="http://dl.fedoraproject.org/pub/fedora/linux/development/$releasever/$basearch/os/"

install
network --bootproto=dhcp

bootloader --timeout=1
zerombr
clearpart --all --initlabel --drives=vda
autopart

keyboard --xlayouts=cz
lang cs_CZ.UTF-8
timezone Europe/Prague --utc
rootpw anaconda

shutdown

%packages
python3-blivet
python3-ipython
@core
%end
