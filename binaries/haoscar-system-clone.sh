#!/bin/bash

$CONFIG_DIR=/usr/share/haoscar/sysimager.conf

[ -f $CONFIG_DIR/image_dir ] && 
	IMG_DIR=`cat $CONFIG_DIR/image_dir` ||
	(echo "$CONFIG_DIR/image_dir not found" && exit -1)

[ -f $CONFIG_DIR/ha_eth ] && 
	ETH=`cat $CONFIG_DIR/ha_eth` ||
	(echo "$CONFIG_DIR/ha_eth not found" && exit -1)

[ -f $CONFIG_DIR/image_name ] && 
	IMG=`cat $CONFIG_DIR/image_name` ||
	(echo "$CONFIG_DIR/image_name not found" && exit -1)

[ -f $CONFIG_DIR/group_name ] && 
	IMG_GROUP=`cat $CONFIG_DIR/group_name` ||
	(echo "$CONFIG_DIR/group_name not found" && exit -1)

[ -f $CONFIG_DIR/primary_ip_addr ] && 
	PRIMARY_IP=`cat $CONFIG_DIR/primary_ip_addr` ||
	(echo "$CONFIG_DIR/primary_ip_addr not found" && exit -1)

[ -f $CONFIG_DIR/secondary_ip_addr ] && 
	SECONDARY_IP=`cat $CONFIG_DIR/secondary_ip_addr` ||
	(echo "$CONFIG_DIR/secondary_ip_addr not found" && exit -1)

[ -f $CONFIG_DIR/primary_hostname ] && 
	PRIMARY_HOST=`cat $CONFIG_DIR/primary_hostname` ||
	(echo "$CONFIG_DIR/primary_hostname not found" && exit -1)

[ -f $CONFIG_DIR/secondary_hostname ] && 
	SECONDARY_HOST=`cat $CONFIG_DIR/secondary_hostname` ||
	(echo "$CONFIG_DIR/secondary_hostname not found" && exit -1)

[ -f $CONFIG_DIR/subnet ] && 
	SUBNET=`cat $CONFIG_DIR/subnet` ||
	(echo "$CONFIG_DIR/subnet not found" && exit -1)

[ -f $CONFIG_DIR/netmask ] && 
	NETMASK=`cat $CONFIG_DIR/netmask` ||
	(echo "$CONFIG_DIR/netmask not found" && exit -1)

if [[ ! -d $IMG_DIR ]]; then
	mkdir -p $IMG_DIR;
fi

echo "Preparing the golden client ...";
si_prepareclient --server $PRIMARY_IP --quiet || \
	(echo "Error in si_prepareclient" && exit)

echo "Getting the image";
si_getimage --golden-client $PRIMARY_IP --image $IMG --post-install reboot --exclude $IMG_DIR --directory $IMG_DIR --ip-assignment static --quiet || \
	(echo "Error in si_getimage" && exit)


# NOTE: If ufw is active, we have to add a rule to allow rsync port
echo "Start the systemimager-server-rsyncd service"
service systemimager-server-rsyncd start

echo "Make bootserver";
si_mkbootserver -f --interface=$ETH --localdhcp=y --pxelinux=/usr/lib/syslinux/pxelinux.0

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
	--netmask $NETMASK \\
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
./gen-cluster-xml.pl --primary-hostname $PRIMARY_HOST \\
	--secondary-hostname $SECONDARY_HOST \\
	--image-name $IMG \\
	--image-group-name $IMG_GROUP \\
	> $base_name

si_clusterconfig -u
si_mkclientnetboot --netboot --clients $SECONDARY_HOST --flavor $IMG

