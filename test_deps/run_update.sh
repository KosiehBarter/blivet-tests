#!/bin/bash

cd /root/
rm -rf ./*.py
rm -rf ./blivet

sleep 20

git clone "https://github.com/rhinstaller/blivet.git" /root/blivet/ --branch=1.x-branch --depth=1
echo "$? blivet git download" > res

/usr/bin/python3 /root/blivet/setup.py install >> res
echo "$? blivet install" >> res

dnf upgrade -y
echo "$? update system" >> res

rm -rf ./run_test.sh && rm -rf ./run_update.sh
poweroff
