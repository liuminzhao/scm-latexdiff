from distutils.core import setup

setup(
    name="scm-latexdiff",
    version="0.1.0",
    description="A command line tool to create diffs between latex documents in a Mercurial or Git repository resulting in a pdf with the changes.",
    author="Paul Hiemstra <paul@numbertheory.nl>, Ronald van Haren <ronald@archlinux.org>",
	author_email="Paul Hiemstra <paul@numbertheory.nl>, Ronald van Haren <ronald@archlinux.org>",
	url="https://bitbucket.org/paulhiemstra/scm-latexdiff",
    license="GPL v3",
    packages=["scm_latexdiff"],
    scripts=["bin/scm-latexdiff"],
    long_description=open('readme.md').read(),
)
