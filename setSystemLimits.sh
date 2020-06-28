#!/bin/bash
# not required if deployed over ansible!"
file="/etc/sysctl.conf"

grep -v "vm.max_map_count" $file > temp && sudo mv temp $file
sudo echo vm.max_map_count=524288 >> $file
sudo sysctl -w vm.max_map_count=524288
