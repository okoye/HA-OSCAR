#!/usr/bin/perl
# Directory (file/directory tree) monitoring script
# Please refer to ./filemon.pl --help (or $help_str) for usage 

use strict;
use warnings;
use Sys::Gamin;
use Getopt::Long;
use Switch;
use threads;
use threads::shared;
use File::Basename;

my ($primary_server, $secondary_server);
my $recursive = "";
my $period = "300";
my $ssh_user = "root";
my $help = 0;
GetOptions(	'recursive' => \$recursive, 
			'period=i' => \$period,
			'primary=s' => \$primary_server, 
			'secondary=s' => \$secondary_server,
			'ssh-user=s' => \$ssh_user,
			'help' => \$help);
			
my $help_str = <<eos

    Usage: filemon.pl [--recursive] [--period=<seconds>]
           [--primary=<primary_server>] [--secondary=<secondary_server>]
           [--ssh-user=<ssh_user>] [--help]
           <dir1> [<dir2> ...]
    Options:
        --recursive 
        	Specified if you want to watch the directory (file)
        	recursively
        	
        --period=<second>
        	The minimum time between consecutive rsync call.
        	Normally, rsync would be called every file changes.
        	But, doing so may heavily load the system and then
        	interfere normal system operation.
        	Specifying the period (in seconds) will prevent this
        	kind of situation. Rsync command will not be invoked
        	until the time from last rsync exceed the period.
        	
        --primary=<primary_server>
        	Just specify the primary server
        
        --secondary=<secondary_server>
        	Secondary (standby) server
        	
        --ssh-user=<user>
        	Specifying a user for ssh connection to secondary server.
        	root is the default value for this parameter.
        
        --help
        	Print this message
        	
        <dir#>
        	are the FULL PATH directory to be listened.
eos
;
if ($help) {
	print "$help_str";
	exit 0;
}
			
if ((! $primary_server) or (!$secondary_server)){
	die "primary or secondary server unspecified";
}
			
print "period = $period\n";

my $fm = new Sys::Gamin;
my $last_change = 0;

# The rest of the arguments (@ARGV) are directory to be watched

sub recursively_add_watch {
	my ($path) = @_;
	if (-d $path) {
		print "Watching $path\n";
		$fm->monitor($path);
		opendir my $DIR, "$path";
		my @files = readdir($DIR);
		foreach my $file (@files){
			if (!($file eq "." || $file eq "..")) {
				recursively_add_watch("$path/$file");
			}
		}
		closedir $DIR;
	}
}

sub get_event_path {
	my ($event) = @_;
	my $path = $event->filename;
	if ($path !~ m/^\//) {
		# If it is not absolute path, we need to do some more stuff
		$path = $fm->which($event)."/".$path;
	}
	return $path;
}

sub call_rsync {
	# TODO Invoke rsync properly
	print "RSYNC CALLED\n";
	foreach my $path (@ARGV){
		my $mod = basename($path);
		my $rsync_cmd = "ssh -l $ssh_user $secondary_server rsync -t -r -z --delete rsync://$primary_server/$mod $path";
		print "Synchronizing $mod\n"; 
		print "command = $rsync_cmd\n";
		!system($rsync_cmd) or die "Error in '$rsync_cmd'";
	}
}

my $dirty = 0; # Dirty bit variable (shared) for rsync wait 
share($dirty);

sub change_event_handler {
	my ($event) = @_;
	my $path = get_event_path($event);
	my $current = time();
	if ($current - $last_change < $period) {
		if (! $dirty) {
			$dirty = 1;
			my $t = threads->create(
					sub {
						my ($sleep_time) = @_;
						print "sleeping beauty ...\n";
						sleep $sleep_time;
						call_rsync();
						$dirty = 0;
					},
					$period
				);
		}
	}
	else {
		call_rsync();
	}
	
	$last_change = $current;
}

sub create_event_handler {
	my ($event) = @_;
	my $path = get_event_path($event);
	if ($recursive && -d $path) {
		recursively_add_watch($path);
	}
}

sub event_handler {
	my ($event) = @_;
#	print "Path: ", $fm->which($event), "/", $event->filename, " Event: ", $event->type, "\n";
#	return 0;
	switch ($event->type) {
		case "change" {
			change_event_handler($event);
		}
		case "create" {
			create_event_handler($event);
		}
		# "move" is quivalent to delete + create
	}
}

foreach my $path (@ARGV) {
	if ($path !~ m/^\//) {
		die "$path is not a full path";
	}
	if ($recursive) {
		recursively_add_watch($path);
	}
	else {
		$fm->monitor($path) if -d $path;
	}
}


while (1) {
	my $event = $fm->next_event; # Blocking call
	event_handler($event); 
}


