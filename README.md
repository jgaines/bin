# My ~/bin

Just a place to keep a copy of my ~/bin hacks.

I have a local .venv inside my ~/bin folder.  I think the only thing that really
relies on it is the flip.py script (through flip.func).  And as I recall all it
really cares about is that it has to be a recent 3.x Python.

| app                       | description                                                              |
| :------------------------ | :----------------------------------------------------------------------- |
| changelog                 | show the changelog for some apps I'm interested in                       |
| checkrequirements         | check local virtualenv requirements                                      |
| dockerhosts               | list all docker hosts from ansible repo, used by following               |
| dockerlist                | lists apps on docker hosts                                               |
| dockerload                | shows Docker version and usage info for all docker hosts                 |
| dockerserver              | shows Docker and docker-compose versions on docker hosts                 |
| engt-permissions.sh       | spew out user and group rights assigned to ENGT repos                    |
| flip                      | function to flip between administrator and eng-tools folders             |
| flip.func                 | sourced script to create flip function                                   |
| flip.py                   | python script to calculate the flipping                                  |
| git-authors               | show all authors in a git repo in pyproject.toml format                  |
| git-configs               | print a list of all currently active git configs                         |
| git-who                   | show who has touched a file in a git repo                                |
| gohere                    | update GOHOME to current directory, for Go language                      |
| goplay                    | start up Go language godoc server                                        |
| goto                      | function to go to folders from partial prefix                            |
| goto.func                 | shell script for goto function                                           |
| goto.py                   | brains behind goto function                                              |
| injectqa.py               | inject qa lib into a virtualenv                                          |
| john-sync                 | synchronize select files to john.eng.netscout.com                        |
| latest-*                  | show installed and latest versions of a tool                             |
| loglp                     | script to log print requests rather than print them                      |
| make-local-latest.sh      | symlink all the latest mise managed tools to ~/.local/latest             |
| make_envrc.sh             | script to create .envrc files until uv does so natively                  |
| make_mise_toml.sh         | script to create python .mise.toml files                                 |
| merge-zsh-history.sh      | merge two zsh history files (used when moving to new machine)            |
| morning-brew.sh           | script to update brew and brew managed tools                             |
| name_addr.sh              | do a name resolution lookup and print FQDN and IP address                |
| pipx-check-all            | check all pipx installed tools for updates (pip list -o)                 |
| pipx-pyupgrade            | force a python upgrade to a pipx managed tool                            |
| pipx-upgrade-all          | upgrade all pipx managed tools                                           |
| randpw.func               | bash function to randomly generate password                              |
| randpwz.func              | zsh function to randomly generate password                               |
| releases                  | show the releases for some apps I'm interested in (symlink to changelog) |
| removews                  | remove all spaces/tabs from a file                                       |
| scat                      | cat file with source highlighting (I still use this occasionally)        |
| showpath                  | dump path out with one directory per line                                |
| swarm                     | start/stop local docker swarm and load secrets from ansible              |
| start                     | script I fire up to start up things                                      |
| test.dockerignore.sh      | test a .dockerignore file against a directory                            |
| touchpad                  | script to enable/disable touchpad                                        |
| update-all-repos          | script to run "git pull --rebase=preserve" in all git repos              |
| update-kitty              | update my copy of kitty terminal tool                                    |
| vcat                      | cat a file with all comment-only and blank lines removed                 |
| versions                  | script to print out various language/shell/tool versions                 |
| vpnfu                     | script to connect to arbor (aa) vpn                                      |
| vpnmafu                   | script to connect to arbor (ma) vpn                                      |
| vpnoff                    | kill the vpn client                                                      |
| whichpkg                  | script to tell me which package a file is from                           |
| zsh_history_fix           | fixes a corrupted .zsh_history file                                      |
