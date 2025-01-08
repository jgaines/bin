#!/usr/bin/env bash
# Install cargo-binstall and friends.  It manages a backup of the installed apps
# and will restore them if it already exists.

curl -L --proto '=https' --tlsv1.2 -sSf https://raw.githubusercontent.com/cargo-bins/cargo-binstall/main/install-from-binstall-release.sh | bash
cargo binstall cargo-update

crates_json_path=~/.local/share/mise/installs/rust/latest/binstall/crates-v1.json
crates_json_backup_path=~/.config/$USER/crates-v1.json
if [ ! -f $crates_json_backup_path ]; then
    # If the backup doesn't exist, hardlink the new crates-v1.json to the backup
    echo "No crates-v1.json backup found at $crates_json_backup_path"
    ln $crates_json_path $crates_json_backup_path
else
    # If the backup exists, remove the new crates-v1.json and hardlink the backup
    # to the new crates-v1.json
    echo "Found crates-v1.json backup at $crates_json_backup_path"
    rm $crates_json_path
    ln $crates_json_backup_path $crates_json_path
fi
cargo install-update -a
