#!/bin/bash

cd /root/
test_to_run=`ls test_stage*.py`
python3 $test_to_run && poweroff
