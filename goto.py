#!/usr/bin/env python3
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


def help():
    print("usage goto [[parent...] project]\n"
          "\n\n"
          "Normal usage is to just supply a project name, that will search the list of project dirs\n"
          "for folder starting with the specified project name.  Supplying a parent will limit to\n"
          "parent directories starting with that string.  Calling goto with no arguments will\n"
          "attempt to go to the last project goto went to."
    )
    exit(0)


if len(sys.argv) > 1:
    if sys.argv[1][0] == '-':
        help()
    *parents, target = [d.lower() for d in sys.argv[1:]]
elif os.path.exists(os.path.expanduser(last_project_file)):
    with open(os.path.expanduser(last_project_file), 'r') as f:
        target = f.read()
    if os.path.exists(target):
        os.chdir(target)
        exit(0)
    else:
        target = None
else:
    target = None

if not target:
    help()

for proj_dir in (os.path.expanduser(p) for p in project_dirs):
    if parents:
        # OK, since even I'm not going to grok this next time I read it, basically, we're
        # checking to make sure that the list of parents matches the start of the tail end
        # of the proj_dir path.  If not, don't look in this project dir.
        if not all(d.startswith(p) for d, p
                   in zip([n.lower() for n in proj_dir.split(os.path.sep) if n][-len(parents):],
                          parents)):
            continue
    # look for exact match to project directory
    for name in sorted(os.listdir(proj_dir)):
        if os.path.isdir(os.path.join(proj_dir, name)):
            if name.lower().startswith(target):
                goto_project(os.path.join(proj_dir, name))
                exit(0)
