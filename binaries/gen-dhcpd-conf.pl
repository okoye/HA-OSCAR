#!/usr/bin/perl

use strict;
use warnings;
use Getopt::Long;

my $primary_ip;
my $secondary_ip;
my $subnet;
my $netmask; 

my $help = 0;

GetOptions(
	"primary-ip=s" => \$primary_ip,
	"secondary-ip=s" => \$secondary_ip,
	"subnet=s" => \$subnet,
	"netmask=s" => \$netmask,
	"help" => \$help
);

if ($help) {
	print <<EOS

	gen-dhcpd-conf.pl

	Similar to gen-cluster-xml.pl, this script generates contents
	for the file dhcpd.conf (which is in
		/etc/dhcp3 for Ubuntu, and in
		/etc for CentOS
	)

	NOTE: This script will produce the content thru standard output
	You have to redirect the output to the dhcpd.conf yourself :D
	
	The required options are 

	--primary-ip ###.###.###.###
		The IP address for primary server

	--secondary-ip ###.###.###.###
		The IP address for secondary server

	--netmask ###.###.###.###
		The netmask

	--subnet ###.###.###.###
		The subnet

EOS
;
	exit 0;
}

my $str = <<EOS
authoritative;
ddns-update-style none;

# Imageserver
option option-140 code 140 = text;

# log_server_port
option option-141 code 141 = unsigned integer 32;

# ssh_download_url
option option-142 code 142 = string;

# flamethrower_directory_portbase
option option-143 code 143 = string;

# tmpfs_staging
option option-144 code 144 = string;

# option-140 is the IP address of your SystemImager image server
option option-140 "$primary_ip";

# option-142 specifies the URL address of your ssh download
# This should be in the format of "http://192.168.0.1/systemimager/boot/".
#option option-142 "http://192.168.0.1/systemimager/boot/"; 

# option-143 specifies the Flamethrower directory port.
# The default is "9000".
#option option-143 "9000"; 

  # 
  # option-144 tells your auto-install client to spool the image into a tmpfs
  # prior to laying it down on disk.  It is not certain that this is always
  # a good thing to do.  And if you're feeling gutsy and want to try it, be
  # sure that your (memory + swap) is at least twice the size of your image
  # or your image transfer will fail when the tmpfs filesystem gets full!!!
  # If unsure, say "no".
  # 
  option option-144 "n"; 

# next-server is your network boot server
next-server $primary_ip; 

# log-servers
#option log-servers 1.2.3.4; 

# option-141 is the port number your log server uses
#option option-141 514; 


# set lease time to infinite (-1)
default-lease-time -1;

# Uncomment one of the two following lines.  The first, if you need to
# boot i386 clients, or the second for booting ia64 clients.
filename "pxelinux.bin";   # i386
#filename "elilo.efi";   # ia64

subnet $subnet netmask $netmask { 
  range  $secondary_ip $secondary_ip; 
  option domain-name ""; 
  option routers $primary_ip; 
 } 
EOS
;

print "$str\n";


