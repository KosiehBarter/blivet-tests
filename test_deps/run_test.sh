#!/bin/bash

cd /root/

## Check, if run_update is present, if so, run it
ls ./run_update.sh

if [ $? == 0 ] ; then
  /bin/bash /root/run_update.sh ;
else
  test_to_run=`ls test_stage_*.py`
  test_stage=`echo $test_to_run | sed 's/test_stage_\([0-9]*\)_.*/\1/'` ;
fi

if [ $? != 0 ] ; then
  echo "$test_to_run FAILED to run" > TEST_RESULT_$test_stage ;
fi

python3 $test_to_run

poweroff
