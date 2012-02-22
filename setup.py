#!/usr/bin/env python2
# released under the GPL v3

from distutils.core import setup

def main():
    setup( name="scm-latexdiff",
    version="0.1.0",
    description="A command line tool to create diffs between latex documents in a Mercurial or Git repository resulting in a pdf with the changes.",
    author="Paul Hiemstra <paul@numbertheory.nl>, Ronald van Haren <ronald@archlinux.org>",
    url="https://bitbucket.org/paulhiemstra/scm-latexdiff",
    license="GPL v3",
    packages=["python-scm-latexdiff"], 
    scripts=["bin/scm-latexdiff"],
    classifiers=["Development Status :: 5 - Production/Stable", "Intended Audience :: End Users/Desktop", "License :: OSI Approved :: GNU General Public License (GPL)", "Operating System :: POSIX :: Linux"],
        # a bunch of optional tags, a list of classifiers can be found at http://pypi.python.org/pypi?:action=list_classifiers
    long_description=open('README').read(),

