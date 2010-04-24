#!/bin/bash

CONFIG_FILE=/usr/share/haoscar/sysimager.conf
[ -f $CONFIG_FILE ] || { echo "Error: $CONFIG_FILE not found!"  && exit -1; }

sed s/:/=/ $CONFIG_FILE > /tmp/sysimager.conf.sh
source /tmp/sysimager.conf.sh

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
	{ echo "Cannot crate directory: $IMAGE_DIR" && exit -1 ; }
fi

echo "Preparing the golden client ...";

si_prepareclient --server $PRIMARY_IP --quiet || { echo "Error in si_prepareclient" && exit -1; }

echo "Getting the image";
si_getimage --golden-client $PRIMARY_IP --image $IMAGE_NAME --post-install reboot --exclude $IMAGE_DIR --directory $IMAGE_DIR --ip-assignment static --quiet || { echo "Error in si_getimage" && exit -1; }


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
dhcp_conf="/etc/dhcp3/dhcpd.conf";
bak $dhcp_conf;

./gen-dhcpd-conf.pl --primary-ip $PRIMARY_IP \
	--secondary-ip $SECONDARY_IP \
	--netmask $MASK \
	--subnet $SUBNET > $dhcp_conf

service dhcp3-server restart



echo "Configuring cluster.xml ...";
# Then edit the file /etc/systemimager/cluster.xml
#  defining your cluster (well ... just primary head as image server
#  and secondary head as client) 
# Then, run the following command

cluster_xml="/etc/systemimager/cluster.xml";
bak $cluster_xml;

./gen-cluster-xml.pl --primary-hostname $PRIMARY_HOSTNAME \
	--secondary-hostname $SECONDARY_HOSTNAME \
	--image-name $IMAGE_NAME \
	--image-group-name $GROUP_NAME \
	> $base_name

si_clusterconfig -u
# This is not working
#  |
#  |
#  v
#si_mkclientnetboot --netboot --clients $SECONDARY_IP --flavor $IMAGE_NAME
#
# si_mkclientnetboot will need info from cluster.xml
# so, wee need to put secondary ip address in /etc/hosts
# for this to work
#

if grep "$SECONDARY_HOSTNAME" /etc/hosts; then
	IP=`grep "$SECONDARY_HOSTNAME" /etc/hosts | cut -f 1`;
	if [[ $IP != $SECONDARY_IP ]]; then
		sed s/$IP/$SECONDARY_IP/ /etc/hosts > /tmp/hosts.tmp
		bak /etc/hosts;
		cp /tmp/hosts.tmp > /etc/hosts 
	fi
else
	bak /etc/hosts
	echo "$SECONDARY_IP	$SECONDARY_HOSTNAME" >> /etc/hosts

fi 

si_mkclientnetboot --netboot --clients $SECONDARY_HOSTNAME --flavor $IMAGE_NAME



