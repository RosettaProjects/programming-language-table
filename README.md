# programming-language-table

A side-by-side comparison of programming languages, with code examples.

Design goals: Groups of programming languages, and each group or individual language can be hidden
by clicking. Same for the rows, each of which illustrates a specific feature, with analogous groups
for categories of features.

## Design Goals

WIP

## Contributing

To keep the barriers to entry as low as is reasonably possible, the only dependencies to build the
page from the markdown files is the programming language Perl 5. This is a compromise between
choosing the right tool or the job and choosing something universal, easily installable, and
well-documented.

The conversion is performed by `make.pl`, a Perl script that uses modules defined in `./modules`.
Output is written to `./build`.
