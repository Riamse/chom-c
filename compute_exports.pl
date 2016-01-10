#!/usr/bin/perl

use strict;
use warnings;

use Data::Dumper qw(Dumper);

my $HEADERS;
my $TPL;
$HEADERS = ['assert.h', 'ctype.h', 'errno.h', 'fenv.h', 'float.h', 'inttypes.h', 'iso646.h', 'limits.h', 'locale.h', 'math.h', 'setjmp.h', 'signal.h', 'stdarg.h', 'stdbool.h', 'stddef.h', 'stdint.h', 'stdio.h', 'stdlib.h', 'string.h', 'tgmath.h', 'time.h', 'uchar.h', 'wchar.h', 'wctype.h'];
$TPL = <<END;
import pickle
from pathlib import *
data = %s
with (Path("header_exports")/%s).open("wb") as fp:
    pickle.dump(data, fp)

END

foreach my $dot_h (@$HEADERS) {
    my $text;
    my $script;
    $text = `perl get_exports.pl $dot_h`;
    chomp($dot_h = Dumper $dot_h);
    $dot_h = substr($dot_h, 8, -1) . '.pkl';
    #$dot_h =~ s/(;|\$VAR1 = )//g;
    $script = sprintf $TPL, $text, $dot_h;
    system("python3", "-c", $script);
}
