#!/bin/env bash

# Chunk of code Eddy wrote to spew out user rights assigned to ENGT repos.
# Added groups output as well.
# And yes, this is slow...

TOKEN_FILE="$HOME/.ssh/bb-prod-token"
if [[ ! -f "$TOKEN_FILE" ]]; then
    echo "Error: Token file $TOKEN_FILE not found"
    exit 1
fi

# Verify file permissions
if [[ "$(stat -c '%a' "$TOKEN_FILE")" != "600" ]]; then
    echo "Warning: $TOKEN_FILE has insecure permissions. Recommend: chmod 600 $TOKEN_FILE"
fi

# Source token file but don't expose its contents in error messages
set +x
source "$TOKEN_FILE"
set -x

# Verify token was loaded
if [[ -z "${BITBUCKET_TOKEN:-}" ]]; then
    echo "Error: BITBUCKET_TOKEN variable not set in $TOKEN_FILE"
    exit 1
fi

for slug in $(curl -s -H "Authorization: Bearer $BITBUCKET_TOKEN" 'https://bosenbbucket1.netscout.com:8443/rest/api/latest/projects/ENGT/repos?limit=1000' | jq -r '.values[].slug'); do
    echo "$slug: "
    users=$(curl -s -H "Authorization: Bearer $BITBUCKET_TOKEN" "https://bosenbbucket1.netscout.com:8443/rest/api/latest/projects/ENGT/repos/$slug/permissions/users?limit=1000")
    [[ $(echo "$users" | jq .values) != "null" ]] && echo "$users" | jq '.values[] | "\(.user.name) - \(.permission)"'
    groups=$(curl -s -H "Authorization: Bearer $BITBUCKET_TOKEN" "https://bosenbbucket1.netscout.com:8443/rest/api/latest/projects/ENGT/repos/$slug/permissions/groups?limit=1000")
    [[ $(echo "$groups" | jq .values) != "null" ]] && echo "$groups" | jq '.values[] | "\(.group.name) - \(.permission)"'
done 
