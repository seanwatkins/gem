#!/usr/bin/perl -w
#
# rrdaddsource  Adds a new data source to an RRD database.
#
# $Id: rrdaddsource-1.2 8 2005-07-26 13:02:58Z joostc $
#
# Written by Joost Cassee
# Update to RRDtool 1.2 by David Behr
# Copyright 2005 Bateau Knowledge
# http://dev.bateauknowledge.nl/trac/wiki/RrdAddSource
#
# Update to support adding multiple data sources by Jens-U. Mozdzen <jmozdzen@nde.ag>
# See http://technik.blogs.nde.ag/
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# See the complete licence at http://dev.bateauknowledge.nl/svn/COPYING

my $basename;

sub BEGIN {
    $basename = 'rrdaddsource';
    $SIG{__WARN__} = sub { warn "$basename: $_[0]"; };
    $SIG{__DIE__} = sub { die "$basename: $_[0]"; };
}

use strict;

my $rrdtool = '/usr/bin/rrdtool';

if (defined $ARGV[0] and $ARGV[0] eq '--help') {
	print <<".";
usage:  $basename <original rrd file> <new rrd file> <data source> { <data source> }

Adds new data sources to an RRD database. Uses rrdtool to dump the original
database to an XML file, edits it and then restores it to the new database.

The datasource arguments have the same format as in rrdtool create:
  ds-name:DST:heartbeat:min:max
See rrdcreate(1) for more information. Note that those arguments are not checked
for validity.
.
	exit;
}

die "illegal number of arguments\n" unless $#ARGV >= 2;

my $infile = $ARGV[0];
my $outfile = $ARGV[1];
my $i;
my $rows = "";

for ($i = 2 ; $i <= $#ARGV; $i++) {
	my ($dsname, $dstype, $dshb, $dsmin, $dsmax, $undef) = split(/:/, $ARGV[ $i]);
	die "illegal source format: $ARGV[ $i]\n" unless defined $dsmax and not defined $undef;

	# pre-construct dummy values for new sources
	$rows = $rows . "<v> NaN </v>";
}
# terminate dummy values for new sources
$rows = $rows . "</row>";

open(IN, "$rrdtool dump $infile|") or die "$!";
open(OUT, "|$rrdtool restore - $outfile") or die "$!";

while (<IN>) {
	# Define new data source
	m#<!-- Round Robin Archives --># and do {
		for ($i = 2 ; $i <= $#ARGV; $i++) {
			my ($dsname, $dstype, $dshb, $dsmin, $dsmax, $undef) = split(/:/, $ARGV[ $i]);

			print OUT <<".";
<ds>
	<name> $dsname </name>
	<type> $dstype </type>
	<minimal_heartbeat> $dshb </minimal_heartbeat>
	<min> $dsmin </min>
	<max> $dsmax </max>

	<!-- PDP Status -->
	<last_ds> UNKN </last_ds>
	<value> 0.0000000000e+00 </value>
	<unknown_sec> 0 </unknown_sec>
</ds>

.
		};
	};

	# Add empty entry to the values
	m#</cdp_prep># and do {
		for ($i = 2 ; $i <= $#ARGV; $i++) {
			print OUT <<"."
<ds>
	<primary_value> 0.0000000000e+00 </primary_value>
	<secondary_value> 0.0000000000e+00 </secondary_value>
	<value> NaN </value>
	<unknown_datapoints> 0 </unknown_datapoints>
</ds>

.
		};
	};

	# Add empty entries to the database
	s#</row>#$rows#e;

	print OUT $_;
}

close(IN) or die "$!";
close(OUT) or die "$!";
