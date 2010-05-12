#!/bin/bash
#
# Assuming that this script is running under chroot
# (/ pointing at /usr/share/haoscar/images/ha_image)

# For debugging only
# VVVVVVVVVVVVVVVVVV
CONFIG_FILE=/usr/share/haoscar/sysimager.conf
[ -f $CONFIG_FILE ] || { echo "Error: $CONFIG_FILE not found!"  && exit -1; }

sed s/:/=/ $CONFIG_FILE > /tmp/sysimager.conf.sh
source /tmp/sysimager.conf.sh
# ^^^^^^^^^^^^^^^^^^^^^
# Can be removed after debugging ...


function assert() {
        if [[ ! ${!1} ]]; then
                echo "Error: $1 is not set!!!";
                exit -1; 
        fi  
        echo "$1 = ${!1}";
}

function bak() {
        if [ ! -f $1 ]; then
                echo "Backup error: $1 not found";
                return 100;
        fi;
        base_name=$1;
        num=1;
        while [ -f $base_name.bak.$num ]; do
                num=$((num+1))
        done
        cp $base_name $base_name.bak.$num;
}


# NOTES:
# These variables should be available
assert "GROUP_NAME";
assert "HA_ETH"; 
assert "IMAGE_DIR";
assert "IMAGE_NAME";
assert "MASK";
assert "PRIMARY_HOSTNAME";
assert "PRIMARY_IP";
assert "SECONDARY_HOSTNAME";
assert "SECONDARY_IP";
assert "SUBNET";

# Altering the IP address
sed s/$PRIMARY_IP/$SECONDARY_IP/g /etc/network/interfaces > /tmp/interfaces
bak "/etc/network/interfaces";
mv /tmp/interfaces /etc/network/interfaces


exit 0; # Exit from the chroot shell 

