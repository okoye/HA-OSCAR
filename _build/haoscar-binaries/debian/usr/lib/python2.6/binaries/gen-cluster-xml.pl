#!/usr/bin/perl
# For more info see ./gen-cluster-xml.pl --help
use warnings;
use strict;
use Getopt::Long;


my $primary_hostname = "primary";
my $secondary_hostname = "secondary";
my $image_group_name = "ha_group";
my $image_name = "ha_image";

my $help = 0;

my $result = GetOptions(
		"primary-hostname=s" => \$primary_hostname,
		"secondary-hostname=s" => \$secondary_hostname,
		"image-group=s" => \$image_group_name,
		"image-name=s" => \$image_name,
		"help" => \$help
	);

if ($help){
	# Display help and exit
	print <<EOS

	This script generates content for cluster.xml file.
	The proper location for cluster.xml is 
	/etc/systemimager/cluster.xml

	However, this program will generate the output content
	through standard output. So, you'll have to redirect
	the generated content to the file yourself :D 
	
	Options:

	--primary-hostname STRING
		Just a hostname of the primary server.

	--secondary-hostname STRING
		A hostname of the secondary server
	
	--image-name STRING
		An image name to be provided to the secondary server.
		Default: ha_image
	
	--image-group-name STRING 
		Just a group name ... nothing important for our task :)
		Default: ha_group

EOS
;
	exit 0;
}

my $str = <<EOF
<?xml version='1.0' standalone='yes'?>
<xml>
    <master>$primary_hostname</master>
    <name>all</name>
    <override>all</override>
    <group>
        <name>$image_group_name</name>
        <image>$image_name</image>
        <node>$secondary_hostname</node>
    </group>
</xml>
EOF
;

print "$str\n";

