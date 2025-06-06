# My ~/bin

Just a place to keep a copy of my ~/bin hacks.

I have a local .venv inside my ~/bin folder.  I think the only thing that really
relies on it is the flip.py script (through flip.func).  And as I recall all it
really cares about is that it has to be a recent 3.x Python.

| app                       | description                                                              |
| :------------------------ | :----------------------------------------------------------------------- |
| changelog                 | show the changelog for some apps I'm interested in                       |
| check                     | show installed and latest versions of tools                              |
| checkrequirements         | check local virtualenv requirements                                      |
| codesync                  | script for synchronizing vscode and vscode-insider configs               |
| dockerhosts               | list all docker hosts from ansible repo, used by following               |
| dockerlist                | lists apps on docker hosts                                               |
| dockerload                | shows Docker version and usage info for all docker hosts                 |
| dockerver                 | shows Docker and docker-compose versions on docker hosts                 |
| edit                      | helper script for editing files                                          |
| engt-permissions.sh       | spew out user and group rights assigned to ENGT repos                    |
| fixdockernet              | script to fix Docker networking issues                                   |
| fixusb                    | utility to fix USB device issues                                         |
| flip                      | function to flip between administrator and eng-tools folders             |
| flip.func                 | sourced script to create flip function                                   |
| flip.py                   | python script to calculate the flipping                                  |
| flush-dns-cache           | script to flush DNS cache                                                |
| git_state.py              | script to report/toggle git in the workspace in the current directory    |
| git-authors               | show all authors in a git repo in pyproject.toml format                  |
| git-configs               | print a list of all currently active git configs                         |
| git-who                   | show who has touched a file in a git repo                                |
| gohere                    | update GOHOME to current directory, for Go language                      |
| goplay                    | start up Go language godoc server                                        |
| injectqa.py               | inject qa lib into a virtualenv                                          |
| install-meslo-nf-fonts.sh | script to install Meslo Nerd Fonts into local fonts and kitty terminal   |
| is_user_locked_out.py     | Python script to check if a user account is locked out                   |
| john-sync                 | synchronize select files to john.eng.netscout.com                        |
| killemacsserver           | script to kill an Emacs server                                           |
| loglp                     | script to log print requests rather than print them                      |
| make_envrc.sh             | script to create .envrc files until uv does so natively                  |
| make_mise_toml.sh         | script to create python .mise.toml files                                 |
| make-local-latest.sh      | symlink all the latest mise managed tools to ~/.local/latest             |
| membersof                 | script to list members of an LDAP group                                  |
| merge-zsh-history.sh      | merge two zsh history files (used when moving to new machine)            |
| morning-brew.sh           | script to update brew and brew managed tools (called by start)           |
| name_addr.sh              | do a name resolution lookup and print FQDN and IP address                |
| neoswap.sh                | script for swapping Neovim configs                                       |
| oldvnpfu                  | legacy script for VPN connection                                         |
| palmdetection             | script to toggle palm detection on touchpad                              |
| pyusage.py                | script to analyze python usage in projects                               |
| randpw.func               | bash function to randomly generate password                              |
| randpwz.func              | zsh function to randomly generate password                               |
| releases                  | show the releases for some apps I'm interested in (symlink to changelog) |
| removews                  | remove all spaces/tabs from a file                                       |
| samaccountname            | script to look up sAMAccountName for one or more email addresses         |
| scat                      | cat file with source highlighting (I still use this occasionally)        |
| soar_update.sh            | script to update soar and soar managed tools (called by start)           |
| solcarrot-calc            | calculator for Sol-carrot Minecraft mod                                  |
| spellcheck.sh             | script to check spelling in files                                        |
| start                     | script I fire up to start up things at work                              |
| startemacs                | script to start Emacs                                                    |
| swarm                     | start/stop local docker swarm and load secrets from ansible              |
| test.dockerignore.sh      | test a .dockerignore file against a directory                            |
| touchpad                  | script to enable/disable touchpad                                        |
| update                    | script to update select managed tools (called by start)                  |
| update-all-repos          | script to run "git pull --rebase=preserve" in all git repos              |
| update-lmd                | script to update lmd(maldet) tool                                        |
| update-werk.sh            | script to update werk (a WIP 'just' contender)                           |
| valheim_backup            | script for backing up Valheim game data                                  |
| valheim_profile           | profile settings for Valheim                                             |
| vcat                      | cat a file with all comment-only and blank lines removed                 |
| versions                  | script to print out various language/shell/tool versions                 |
| vpnfu                     | script to connect to arbor (aa) vpn                                      |
| vpnmafu                   | script to connect to arbor (ma) vpn                                      |
| vpnoff                    | kill the vpn client                                                      |
| wersions                  | display version information for all instances of a command on path       |
| whichpkg                  | script to tell me which package a file is from                           |
| zsh_history_fix           | fixes a corrupted .zsh_history file                                      |
