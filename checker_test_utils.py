### Test utils - Checking tool
### Part of: Blivet test collection
### Author: kvalek@redhat.com
### All programs I create are under GPL license.

## Print information
def print_information(issue_array):
    for inc in issue_array:
        print(inc)

## Check size
def check_dev_size(ia, value_a, value_b, scanned_dev):
    if (value_a == value_b):
        ia.append("PASS:\tSIZE:\t{} == {} on dev {}".format(value_a, value_b, scanned_dev))
    else:
        ia.append("FAIL:\tSIZE NOT EQUAL: size {} != {} size on dev {}".format(value_a, value_b, scanned_dev))
