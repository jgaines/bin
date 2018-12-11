#!/usr/bin/env python
"""Goto project directory with somewhat fuzzy searching.

Future Enhancements:

Add some actual command processing (either using stdlib or click).
Set up external config file for specifying project dirs.  Make it look
less like I wrote it under extreme time pressure. ;)

Set up command line completion.

Another idea is to roll up the shell integration script into this, so
passing this script a parameter of some sort would cause it to puke
out the proper shell function, so to use it on a unix box, you'd add a
line like:

    source $(python /path/to/goto.py --shell)

to your shell start up script.  And it could pull all the info it
needs to figure out what shell it's running under, where the goto.py
script lives and the proper python to run under.  It would then send
the following to stdout:

function goto {
    python ~/bin/goto.py $*
    if [ $? == 0 ]
    then
        cd `cat ~/.goto_last_project`
    fi
}

"""


import os
import sys

project_dirs = [
    '~/git/eng-tools',
    '~/git/administrator',
    '~/git/docker',
    '~/projects',
    # '~/work/@active',
    # '~/work/@done',
    # '~/work/@hold',
    # '~/work',
]
last_project_file = '~/.goto_last_project'


def goto_project(target):
    os.chdir(target)
    with open(os.path.expanduser(last_project_file), 'w') as f:
        f.write(target)
    exit(0)

if len(sys.argv) > 1:
    target = sys.argv[1].lower()
elif os.path.exists(os.path.expanduser(last_project_file)):
    with open(os.path.expanduser(last_project_file), 'r') as f:
        target = f.read()
    if os.path.exists(target):
        os.chdir(target)
        exit(0)
else:
    target = None

if not target:
    print 'usage: goto [project]'
    exit(1)

for proj_dir in (os.path.expanduser(p) for p in project_dirs):
    # look for exact match to project directory
    for name in os.listdir(os.path.expanduser(proj_dir)):
        if os.path.isdir(os.path.join(proj_dir, name)):
            if name.lower().startswith(target):
                goto_project(os.path.join(proj_dir, name))
                exit(0)
