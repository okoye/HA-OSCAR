#!/usr/bin/perl
# This script generates a rsyncd.conf configuration file for rsync daemon
# Please refer to ./rsyncd.conf-gen.pl --help (or $help_str) for usage 
use strict;
use warnings; 
use File::Basename; 
use Getopt::Long;

my $script_dir = dirname($0);

my $output_file = "$script_dir/rsyncd.conf";
my ($primary_server, $secondary_server);

my $help_str = <<EOS
	Usage: 
	rsyncd.conf-gen.pl [--output=<output_file>] --primary=<primary_server>
	                   --secondary=<secondary_server>
	                   <dir1> [<dir2> ...]
	Description:
	The script will generate ./rsyncd.conf (if not specified otherwise by
	--output) having individual module for each dir1, dir2, etc

	<dir1>, <dir2>, ... should be full path	
	
	Options:
	--output=<output_file>
	    The output file. The default is ./rsyncd.conf
	
	--primary=<primary_server>
	    Hostname or the IP address of the primary server
	    
	--secondary=<secondary_server>
	    Hostname or the IP address of the secondary server
	    
	<dir1> [<dir2> ...]
	    Full path(s) of the directory (directories)
EOS
;

my $help;

GetOptions(	"output=s" => \$output_file,
			"primary=s" => \$primary_server,
			"secondary=s" => \$secondary_server,
			"help" =>\$help);

if ($help){
	print $help_str;
	exit;
}

if (!$primary_server or !$secondary_server) {
	die "Primary or secondary server wasn't specified";
}

my @dirs = @ARGV;

#my $header_file = "$script_dir/rsyncd.conf.head";

#if (!-f $header_file) {
#	die "Can't find $header_file";
#}

#!system("cp $header_file $output_file") or die "haha";

open my $fout, "> $output_file"
	or die "Cannot write to $output_file";
	
# Each dir in the arguments will be added as a module in the configuration

print $fout <<eos
pid file = /tmp/rsyncd.pid
max connections = 1
hosts allow = $secondary_server
eos
;

foreach my $dir (@dirs) {
	if (! -d $dir) {
		die "$dir is not a directory!!!";
	}
	my $mod = basename($dir);
	print $fout
<<EOS 

[$mod]
	path = $dir
EOS
	
}

close $fout;


