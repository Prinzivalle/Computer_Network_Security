#!/bin/bash

#open-rsa directory
dir=/usr/share/doc/openvpn/example/easy-rsa/2.0

# create certification authority
cd $dir
pwd
chmod +x whichopensslcnf
chmod +x pkitool
source vars
sh clean-all
echo -e '\n\n\n\n\n\nCertification_authority\n\n' | sh build-ca 
