#!/bin/bash

cd /root/keys

# create CA key
openssl genrsa -aes256 -out CA_key.private -passout pass:8%0%Zef6kbBvG0g 4096

# create root certificate
echo -e '\n\n\n\n\n\n\n' | openssl req -x509 -new -nodes -key CA_key.private -sha256 -days 1825 -out CA_root.pem -passin pass:8%0%Zef6kbBvG0g

#open-rsa directory
#dir=/usr/share/doc/openvpn/example/easy-rsa/2.0

# create certification authority
#cd $dir
#pwd
#chmod +x whichopensslcnf
#chmod +x pkitool
#source vars
#sh clean-all
#echo -e '\n\n\n\n\n\nCertification_authority\n\n' | sh build-ca 
