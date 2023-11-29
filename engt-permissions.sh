#!/bin/env bash

# Chunk of code Eddy wrote to spew out user rights assigned to ENGT repos.
# Added groups output as well.
# And yes, this is slow...

source ~/.ssh/bb-prod-token

for slug in $(curl -s -H "Authorization: Bearer $BITBUCKET_TOKEN" 'https://bosenbbucket1.netscout.com:8443/rest/api/latest/projects/ENGT/repos?limit=1000' | jq -r '.values[].slug'); do
    echo "$slug: "
    users=$(curl -s -H "Authorization: Bearer $BITBUCKET_TOKEN" "https://bosenbbucket1.netscout.com:8443/rest/api/latest/projects/ENGT/repos/$slug/permissions/users?limit=1000")
    [[ $(echo "$users" | jq .values) != "null" ]] && echo "$users" | jq '.values[] | "\(.user.name) - \(.permission)"'
    groups=$(curl -s -H "Authorization: Bearer $BITBUCKET_TOKEN" "https://bosenbbucket1.netscout.com:8443/rest/api/latest/projects/ENGT/repos/$slug/permissions/groups?limit=1000")
    [[ $(echo "$groups" | jq .values) != "null" ]] && echo "$groups" | jq '.values[] | "\(.group.name) - \(.permission)"'
done 
