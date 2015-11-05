#version=DEVEL
url --url="http://download.eng.brq.redhat.com/pub/fedora/fedora-alt/stage/23_TC11/Server/x86_64/os/"

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
