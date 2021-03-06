
===========
scm-latexdiff
===========

A command line tool to create diff pdf's from git and mercurial repos.
The script will automatically detect if the repo is git or hg. The
result is a pdf with the differences between the revisions, diff.pdf.

Usage:

	scm-latexdiff OLD:FILE NEW:FILE DIFF_DIR

where:

	OLD:    old revision id, local for non-commited
	NEW:    new revision id, local for non-commited
	FILE:   filename of the file you want to diff
	DIFF_DIR: diff file directory

Examples
========

for git

	scm-latexdiff 87213:draft/spam.tex 97123:draft/spam.tex draft

Notes
=====

I kept `diff.aux`, `diff.tex` files and added `DIFF_DIR` to allow troublesome when sometimes `Bibtex` does not work. Please run this script under root directory for the repo.

INSTALL
=======

This tool uses distutils for installation. The following command installs
the tool on your machine:

	python setup.py install

To install to a non-standard directory tree (e.g. in your home directory) use
`--prefix`:

	python setup.py install --prefix=/home/spam/

Do remember to add `/home/spam/lib/python2.x/site-packages/` to your `PYTHONPATH` environment variable.

License
=======

Copyright © 2012, Paul Hiemstra <paul@numbertheory.nl>,
Ronald van Haren <ronald@archlinux.org>.
This file is part of scm-latexdiff.

scm-latexdiff is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the Licence, or
(at your option) any later version.

scm-latexdiff is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.


Contributors
============

- Paul Hiemstra <paul@numbertheory.nl>
- Ronald van Haren <ronald@archlinux.org>
