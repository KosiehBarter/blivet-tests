#version=DEVEL
url --url="<your url to distro's s repo>"

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

repo --name=python3repo --baseurl="<url for python3 repo if needed>"

shutdown

%packages
python3
python3-six
python3-kickstart
python3-pyudev
parted
python3-pyparted
libselinux-python3
python3-blockdev
libblockdev-plugins-all
util-linux
dosfstools
e2fsprogs
lsof
python3-hawkey
python3-gobject-base
git
@core
%end

%post
git clone "https://github.com/rhinstaller/blivet.git" /root/blivet/ --branch=1.x-branch --depth=1
cd /root/blivet/
/usr/bin/python3 /root/blivet/setup.py install
/usr/bin/pip3 install ipython

cat << EOF > /usr/lib/systemd/system/blivet-tests.service
[Unit]
Description=Blivet-tests package initializer

[Service]
Type=oneshot
ExecStart=/root/run_test.sh

[Install]
WantedBy=multi-user.target
EOF
systemctl enable blivet-tests.service
%end
