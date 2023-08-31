# My ~/bin

Just a place to keep a copy of my ~/bin hacks.

I have a local .venv inside my ~/bin folder.  I think the only thing that really relies
on it is the flip.py script (through flip.func).  And as I recall all it really cares
about is that it has to be a recent 3.x Python.

| app                  | description                                                   |
|:---------------------|:--------------------------------------------------------------|
| checkrequirements    | check local virtualenv requirements                           |
| dockerlist           | lists apps on docker hosts                                    |
| dockerload           | shows Docker version and usage info for all docker hosts      |
| dockerserver         | shows Docker and docker-compose versions on docker hosts      |
| flip                 | function to flip between administrator and eng-tools folders  |
| flip.func            | sourced script to create flip function                        |
| flip.py              | python script to calculate the flipping                       |
| gohere               | update GOHOME to current directory, for Go language           |
| goplay               | start up Go language godoc server                             |
| goto                 | function to go to folders from partial prefix                 |
| goto.func            | shell script for goto function                                |
| goto.py              | brains behind goto function                                   |
| injectqa.py          | inject qa lib into a virtualenv                               |
| latest-*             | show installed and latest versions of a tool                  |
| loglp                | script to log print requests rather than print them           |
| merge-zsh-history.sh | merge two zsh history files (used when moving to new machine) |
| pipx-check-all       | check all pipx installed tools for updates (pip list -o)      |
| pipx-pyupgrade       | force a python upgrade to a pipx managed tool                 |
| randpw.func          | bash function to randomly generate password                   |
| randpwz.func         | zsh function to randomly generate password                    |
| scat                 | "source cat" cat file with source highlighting                |
| showpath             | dump path out with one directory per line                     |
| start                | script I fire up to start up things                           |
| touchpad             | script to enable/disable touchpad                             |
| update-all-pipsi     | script to run "pipsi upgrade" on all pipsi installed apps     |
| update-all-repos     | script to run "git pull --rebase=preserve" in all git repos   |
| update-kitty         | update my copy of kitty terminal tool                         |
| vcat                 | cat a file with all comment-only and blank lines removed      |
| versions             | script to print out various language/shell/tool versions      |
| vpnfu                | script to connect to arbor (aa) vpn                           |
| vpnmafu              | script to connect to arbor (ma) vpn                           |
| vpnoff               | kill the vpn client                                           |
| whichpkg             | script to tell me which package a file is from                |
| zsh_history_fix      | fixes a corrupted .zsh_history file                           |
