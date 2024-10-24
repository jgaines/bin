#!/bin/bash

USER="your.username"
DOMAIN="yourdomain.com"

smbpasswd -U $USER -r `nslookup _ldap._tcp.dc._msdcs.netscout.com | awk '{print $2;exit;}'`