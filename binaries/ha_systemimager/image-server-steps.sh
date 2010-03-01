#!/bin/bash

IMG_DIR=/root/systemimager/images
ETH=eth0
IMG=ha_image

if [[ ! -d $IMG_DIR ]]; then
	mkdir -p $IMG_DIR;
fi

echo "Preparing the golden client ...";
si_prepareclient --server 192.168.0.1 --quiet || \
	(echo "Error in si_prepareclient" && exit)

echo "Getting the image";
si_getimage --golden-client 192.168.0.1 --image $IMG --post-install reboot --exclude $IMG_DIR --directory $IMG_DIR --ip-assignment static --quiet || \
	(echo "Error in si_getimage" && exit)


# NOTE: If ufw is active, we have to add a rule to allow rsync port
echo "Start the systemimager-server-rsyncd service"
service systemimager-server-rsyncd start

echo "Make bootserver";
si_mkbootserver -f --interface=$ETH --localdhcp=y --pxelinux=/usr/lib/syslinux/pxelinux.0

exit;
# I exit here because after this point we need some
# manual works. We can remove 'exit' after the
# automatic script generation is done 

# Hey, you may have to manually edit the dhcp configuration file
# instead of using the interactive si_mkdhcpserver
# Then, don't forget to restart the dhcp server
# NOTE: The following line is for ubuntu only
echo "Configuring DHCP ... make it yourself!!!";
service dhcp3-server restart

echo "Configuring cluster.xml ... make it yourself!!!";
# Then edit the file /etc/systemimager/cluster.xml
#  defining your cluster (well ... just primary head as image server
#  and secondary head as client) 
# Then, run the following command
si_clusterconfig -u
si_mkclientnetboot --netboot --clients 'ubuntu-server-2' --flavor $IMG

