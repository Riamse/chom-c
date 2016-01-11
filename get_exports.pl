#!/usr/bin/perl

# OKAY TO BE HONEST
# I DIDN'T WORK HARD
# ON MAKING THIS LOOK PRETTY.
# PLUS IT'S PERL
# SO STOP COMPLAINING.

use strict;
use warnings;

use Data::Dumper qw(Dumper);

my $DOT_H;
my @lines;
my @idents;

$DOT_H = shift @ARGV or die "usage: perl get_exports.pl file.h";

if ($DOT_H) {
    open FH, ">/tmp/shit.c";
    print FH "#include <$DOT_H>\n";
    close FH;
}

chdir '/tmp/';
system("gcc -fdump-translation-unit -c -o /dev/null /tmp/shit.c");
open FH, "</tmp/shit.c.001t.tu";
@lines = grep {$_ =~ /identifier_node/} <FH>;
close FH;
foreach my $line (@lines) {
    my @words;
    @words = split /:/, $line;
    if (index($words[1], "_") != -1) {
        next;
    }
    $words[1] =~ s/lngt$//;
    $words[1] =~ s/^\s+|\s+$//g;
    push @idents, $words[1];
}

open(FH2, '-|', "cpp -dM < /tmp/shit.c");
foreach my $line (<FH2>) {
    my $paren;
    my @parts;
    @parts = split / /, $line, 3;
    if (index($parts[1], "_") != -1) {
        next;
    }
    $parts[1] =~ s/^\s+|\s+$//g;
    $paren = index $parts[1], "(";
    if ($paren != -1) {
        $parts[1] = substr $parts[1], 0, $paren;
    }
    push @idents, $parts[1];
}
close FH2;

printf "{%s}\n", join(", ", map { substr Dumper($_), 8, -2 } @idents);
