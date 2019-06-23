#!/usr/bin/env perl

use strict;
use warnings;

# Stolen from eHive !

my $doxy_bin    = `which doxygen`;
chomp $doxy_bin;
die "Cannot run doxygen binary, please make sure it is installed and is in the path.\n" unless(-r $doxy_bin);

my $doxy_filter = `which doxypy`;
chomp $doxy_filter;

die "Cannot find the Doxygen Python filter 'doxypy' in the current PATH.\n" unless -e $doxy_filter;

my @cmds = (
    "rm -rf docs",
    "doxygen -g -",
    "echo 'PROJECT_NAME           = pyEnsemblRest'",
    "echo 'INPUT                  = ensembl'",
    "echo 'INPUT_FILTER           = $doxy_filter'",
    "echo 'HTML_OUTPUT            = gh-pages'",
    "echo 'EXTRACT_ALL            = YES'",
    "echo 'EXTRACT_PRIVATE        = YES'",
    "echo 'EXTRACT_STATIC         = YES'",
    "echo 'FILE_PATTERNS          = *.py README.md'",
    "echo 'USE_MDFILE_AS_MAINPAGE = README.md'",
    "echo 'ENABLE_PREPROCESSING   = NO'",
    "echo 'RECURSIVE              = YES'",
    "echo 'EXAMPLE_PATTERNS       = *'",
    "echo 'HTML_TIMESTAMP         = NO'",
    "echo 'HTML_DYNAMIC_SECTIONS  = YES'",
    "echo 'GENERATE_TREEVIEW      = YES'",
    "echo 'GENERATE_LATEX         = NO'",
    "echo 'CLASS_DIAGRAMS         = YES'",
    "echo 'HAVE_DOT               = YES'",
    "echo 'CALL_GRAPH             = YES'",
    "echo 'CALLER_GRAPH           = YES'",
    "echo 'COLLABORATION_GRAPH    = NO'",
    "echo 'SOURCE_BROWSER         = YES'",
);

my $full_cmd = '('.join(' ; ', @cmds).") | doxygen -";

print "Running the following command:\n\t$full_cmd\n\n";

system( $full_cmd );



