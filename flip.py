#! /home/jgaines/vpy/mybin/bin/python
"""Flip between eng-tools and administrator directories.

Future Enhancements:

Add some actual command processing (either using stdlib or click).
Set up external config file for specifying project dirs.  Make it look
less like I wrote it under extreme time pressure. ;)

Another idea is to roll up the shell integration script into this, so
passing this script a parameter of some sort would cause it to puke
out the proper shell function, so to use it on a unix box, you'd add a
line like:

    source $(python /path/to/flip.py --shell)

to your shell start up script.  And it could pull all the info it
needs to figure out what shell it's running under, where the goto.py
script lives and the proper python to run under.  It would then send
the following to stdout:

function goto {
    ~/bin/flip.py $*
    if [ $? == 0 ]
    then
        cd `cat ~/.flip_directory`
    fi
}

"""
import os
import pathlib
import sys


FLIPS = {  # TODO: This should probably be in an external config
    ('administrator', 'eng-tools'),
}
FLIP_FLOP = {k: v for k, v in FLIPS}
FLIP_FLOP.update((v, k) for k, v in FLIPS)


def flip(_args):
    current_dir = pathlib.Path(os.getcwd())
    try:
        other_parent = FLIP_FLOP[current_dir.parent.name]
    except KeyError:
        print("Couldn't figure out how to flip from here.")
        return 1
    else:
        other_dir = current_dir.parent.parent / other_parent / current_dir.name
        if other_dir.exists():
            with open(os.path.expanduser('~/.flip_directory'), 'w') as f:
                    f.write(str(other_dir))
            return 0


if __name__ == '__main__':
    exit(flip(sys.argv[1:]))
