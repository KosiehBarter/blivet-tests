#!/bin/bash

cd /root/
test_to_run=`ls test_stage*.py`
test_stage=`echo $test_to_run | sed 's/test_stage\([0-9]*\)_.*/\1/'`

python3 $test_to_run

poweroff
