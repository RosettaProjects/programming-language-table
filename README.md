# programming-language-table

A side-by-side comparison of programming languages, with code examples.

Design goals: Groups of programming languages, and each group or individual language can be hidden
by clicking. Same for the rows, each of which illustrates a specific feature, with analogous groups
for categories of features.

The source for the website is itself written in readable Markdown, which comes in both a feature
view and a language view, which are kept in sync and updated from each other courtesy of the same
in-house Python package that generates the html+js+css for the website.

## Design Goals

The motivation for this project is the desire for a thorough side-by-side comparison of programming
languages. This is primarily for learning, since it allows the learner to contextualize what is
learned by comparing and contrasting with what is already known. For example, a Python programmer curious about Haskell can simply select the Python and Haskell columns and read through the different features to see how Haskell solves the same problems. While language evaluation is a secondary goal, this may well be useful
when selecting a new language to learn or to use for a new project.

This approach to learning is analogous to (and perhaps even inspired by - see
[here](https://github.com/PolyglotToolkit))
the idea of learning a foreign language by reading a parallel text. Seeing the unfamiliar
side-by-side and in one-to-one correspondence with the familiar is a powerful tool for learning.

## Contributing

To keep the barriers to entry as low as is reasonably possible, I use Python 3 to generate the html
from markdown. Yeah, yeah, I know Python is for normies and there are sexier languages out there.
Still, Python is somewhat of a lingua franca and it also has Pygments, an excellent library for code
syntax highlighting. Sometimes getting Python installed and managing virtual environments can be a
pain, so I have written detailed guides to make the process as painless as possible.

This is a compromise between choosing the right tool or the job and choosing something universal,
easily installable, readable, and well-documented. When I find the time, maybe I'll re-write it in
Rust or Go, but until then, Python does the job.

See [here](./guides/python_and_poetry.md) for instructions on getting up and running with Python,
Poetry, and Just. To use Python inside of a Nix development environment, which is highly
recommended but does require a bit of setup up front, see [these instructions](./guides/nix.md).
You may also find the [guide on using pre-commit](./guides/pre-commit.md) helpful.

After cloning the repo and installing the prereqisite tools, the first thing to do will be to run
`just install`. This will make the pltgen binary available inside your environment (if using Nix,
it will be taken care of for you by the omniscient flake). Once you have your development
environment set up, you can run `just generate` to generate the HTML file. If you don't like the
result, you can run `just revert` to roll back the changes. If you only want to synchronize or
validate the markdown files, run the corresponding commands: `just sync` or `just validate`.
Quelle surprise.

## Roadmap

- [ ] change boilerplate to verbose and simply have two sets of content and two sets of output: simple and verbose
- [ ] add option to highlight boilerplate or not
- [ ] separate language classes and languages (either separate menus or just different html classes) to allow individual languages to override classes if unselected after classes (maybe do the same for rows, but less important)
- [ ] add colorscheme selection and editable custom colorscheme values
- [ ] minimal markdown to generate minimal HTML example
- [ ] MVP Python package for html generation
- [ ] make everything keyboard-controllable
- [ ] add keyboard scrolling side-to-side in cells (and vertically?)
