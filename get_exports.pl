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
    if ($words[1] =~ /_/) {
        next;
    }
    $words[1] =~ s/lngt$//;
    $words[1] =~ s/^\s+|\s+$//g;
    push @idents, $words[1];
}

system("cpp -dM < /tmp/shit.c > /tmp/macros");
open FH2, "</tmp/macros";
foreach my $line (<FH2>) {
    my @parts;
    @parts = split / /, $line, 3;
    if ($parts[1] =~ /_/) {
        next;
    }
    $parts[1] =~ s/^\s+|\s+$//g;
    push @idents, $parts[1];
}
close FH2;

print "{";
for (my $i = 0; $i < scalar @idents; ++$i) {
    my $ident;
    chomp($ident = Dumper $idents[$i]);
    $ident = substr($ident, 8, -1);
    #$ident =~ s/(;|\$VAR1 = )//g;
    $ident .= ', ' if $i < scalar @idents - 1;
    print $ident;
}
print "}\n";
