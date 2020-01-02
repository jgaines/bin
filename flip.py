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


# This is a minimal default used if we can't find config file or a [flips]
# section in config file.
FLIPS = {
    'administrator': ['eng-tools'],
}


def load_config(name:str=None) -> Tuple[Dict[str, Any], Dict[str, List[str]]]:
    """Attempt to load config.

    Looks in the XDG config folders, for the first 'flip/flip.cfg' file.
    Normally, you'd set up a local one at $HOME/.config/flip/flip.cfg. It's
    expecting a standard INI format file with a section named [flips] with
    `parent: alternate1, ..., alternateN` keys listing possible parallel
    folders. For example:

    [flips]
    administrator: eng-tools, docker
    projects: docker

    That states that if you're in a folder whose parent is administrator, look
    in ../eng-tools or ../docker for a possible matching folder to flip to. And
    vice-versa so from docker/foo, it would look to see if ../administrator/foo
    existed and flip there if so.
    """
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
    if not flips:
        flips = FLIPS
    return options, flips


def make_flip_flops(flips: Dict[str, List[str]]) -> Dict[str, List[str]]:
    """Covert table flips into flip-flops.

    Given the input of:

    flips = {
        'administrator': ['eng-tools', 'docker'],
    }

    It will return:

    {
    'administrator': ['eng-tools', 'docker'],
    'docker': ['administrator'],
    'eng-tools': ['administrator'],
    }
    """
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

    # Because flip_flops is a defaultdict(list), it always returns other_parents,
    # which will be an empty list if current_dir.parent.name is not in other_parents.
    other_parents = flip_flops[current_dir.parent.name]

    if not other_parents:
        print(f"No flip targets found for parent dir: {current_dir.parent.name}.")
        return 1
    else:
        for other_parent in other_parents:
            other_dir = current_dir.parent.parent / other_parent / current_dir.name
            if other_dir.exists():
                with open(os.path.expanduser('~/.flip_directory'), 'w') as f:
                    f.write(str(other_dir))
                return 0
        else:
            relative_parents = (f"../{p}" for p in other_parents)
            print(f"couldn't find {current_dir.name} in {', '.join(relative_parents)}.")
            return 1


if __name__ == '__main__':
    exit(flip(sys.argv[1:]))
