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
import configparser
import csv
from collections import defaultdict
from io import StringIO
import os
import pathlib
import sys
from typing import Any, Dict, List, Tuple

from xdg import BaseDirectory


# TODO: either side of the FLIPS list should allow multiple targets, so:
#           administrator -> eng-tools, docker
#       should be a valid flip entry, meaning that from administrator,
#       first look in eng-tools then docker for a match and going the other way
#       both eng-tools and docker flip back to administrator.
#       FLIP_FLOP should be Dict[str, List[str]]
#       The code for building FLIP_FLOP from FLIPS will probably have to be done
#       with nested for loops to make it less confusing to follow.

FLIPS = {  # TODO: This should probably be in an external config
    ('administrator', 'eng-tools'),
}


FLIP_FLOP = {k: v for k, v in FLIPS}
FLIP_FLOP.update((v, k) for k, v in FLIPS)


def load_config(name:str=None) -> Tuple[Dict[str, Any], Dict[str, List[str]]]:
    """Attempt to load config."""
    options = dict()
    flips = dict()
    config = None
    for name in BaseDirectory.load_config_paths('flip'):
        config_file = pathlib.Path(name) / 'flip.cfg'
        if config_file.exists():
            config = configparser.ConfigParser()
            config.read(config_file)
            break
    if config:
        if 'options' in config:
            options = dict(config['options'])
        if 'flips' in config:
            for src in config['flips']:
                dst = [d.strip() for d in next(csv.reader(StringIO(config['flips'][src])))]
                flips[src] = dst
    return options, flips


def make_flip_flops(flips: Dict[str, List[str]]) -> Dict[str, List[str]]:
    flip_flops = defaultdict(list)
    flip_flops.update(flips)
    for src, destinations in flips.items():
        for dst in destinations:
            if src not in flip_flops[dst]:
                flip_flops[dst].append(src)
    return flip_flops


def flip(_args):
    options, flips = load_config()

    flip_flops = make_flip_flops(flips)

    current_dir = pathlib.Path(os.getcwd())
    # TODO: Add code to try stepping up the dir tree until we find a point we
    # can flip or hit home folder or root or some such.
    # home_dir = path
    # other_parent = FLIP_FLOP.get(current_dir.parent.name, None)
    # while other_parent is None and current_dir
    try:
        other_parents = flip_flops[current_dir.parent.name]
    except KeyError:
        print("Couldn't figure out how to flip from here.")
        return 1
    else:
        for other_parent in other_parents:
            other_dir = current_dir.parent.parent / other_parent / current_dir.name
            if other_dir.exists():
                with open(os.path.expanduser('~/.flip_directory'), 'w') as f:
                    f.write(str(other_dir))
                return 0
        else:
            print(f"couldn't find {other_dir} in {', '.join(other_parents)}.")
            return 1


if __name__ == '__main__':
    exit(flip(sys.argv[1:]))
