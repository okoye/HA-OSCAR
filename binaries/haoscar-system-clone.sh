#!/bin/bash

#IMAGE_DIR=/root/systemimager/images
#HA_ETH=eth0
#IMAGE_NAME=ha_image
#PRIMARY_IP=192.168.0.1
#SECONDARY_HOST=ubuntu-server-2

CONFIG_FILE=/usr/share/haoscar/sysimager.conf
[ -f $CONFIG_FILE ] || 
{ echo "Error: $CONFIG_FILE not found!"  && exit -1; }

sed s/:/=/ $CONFIG_FILE > /tmp/sysimager.conf.sh
source /tmp/sysimager.conf.sh

function assert() {
	if [[ ! ${!1} ]]; then
		echo "Error: $1 is not set!!!";
		exit -1; 
	fi
}

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

rm /tmp/sysimager.conf.sh


if [[ ! -d $IMAGE_DIR ]]; then
	mkdir -p $IMAGE_DIR || 
	{echo "Cannot crate directory: $IMAGE_DIR" && exit -1 ; }
fi

echo "Preparing the golden client ...";
si_prepareclient --server $PRIMARY_IP --quiet || \
	{echo "Error in si_prepareclient" && exit -1; }

echo "Getting the image";
si_getimage --golden-client $PRIMARY_IP --image $IMAGE_NAME --post-install reboot --exclude $IMAGE_DIR --directory $IMAGE_DIR --ip-assignment static --quiet || \
	{echo "Error in si_getimage" && exit -1; }


# NOTE: If ufw is active, we have to add a rule to allow rsync port
echo "Start the systemimager-server-rsyncd service"
service systemimager-server-rsyncd start

echo "Make bootserver";
si_mkbootserver -f --interface=$HA_ETH --localdhcp=y --pxelinux=/usr/lib/syslinux/pxelinux.0

# Hey, you may have to manually edit the dhcp configuration file
# instead of using the interactive si_mkdhcpserver
# Then, don't forget to restart the dhcp server
# NOTE: The following line is for ubuntu only

echo "Configuring DHCP ...";

base_name=/etc/dhcp3/dhcpd.conf
num=1 
while [ -f $base_name.bak.$num ]; do
	num=$((num+1)) 
done
cp $base_name $base_name.bak.$num
./gen-dhcpd-conf.pl --primary-ip $PRIMARY_IP \\
	--secondary-ip $SECONDARY_IP \\
	--netmask $MASK \\
	--subnet $SUBNET > $base_name

service dhcp3-server restart



echo "Configuring cluster.xml ...";
# Then edit the file /etc/systemimager/cluster.xml
#  defining your cluster (well ... just primary head as image server
#  and secondary head as client) 
# Then, run the following command

base_name=/etc/systemimager/cluster.xml
num=1 
while [ -f $base_name.bak.$num ]; do
	num=$((num+1)) 
done
cp $base_name $base_name.bak.$num;
./gen-cluster-xml.pl --primary-hostname $PRIMARY_HOSTNAME \\
	--secondary-hostname $SECONDARY_HOST \\
	--image-name $IMAGE_NAME \\
	--image-group-name $GROUP_NAME \\
	> $base_name

si_clusterconfig -u
si_mkclientnetboot --netboot --clients $SECONDARY_HOST --flavor $IMAGE_NAME

