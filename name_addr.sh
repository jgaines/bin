#!/bin/bash
# Simple script to do a name resolution lookup and print FQDN and IP address.

nslookup $1 | tail -3