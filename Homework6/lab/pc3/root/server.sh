#!/bin/bash

cd /root/keys

####### starting server
# user A
(while true; do nc -l -p 9000 | tar -x; done)&

# user B
(while true; do nc -l -p 9001 | tar -x; done)&

######## certificate autority
# create CA key
openssl genrsa -aes256 -out CA_key.private -passout pass:8%0%Zef6kbBvG0g 4096

# create root certificate
echo -e '\n\n\n\n\n\n\n' | openssl req -x509 -new -nodes -key CA_key.private -sha256 -days 1825 -out CA_root.pem -passin pass:8%0%Zef6kbBvG0g

######## receive public keys

# generate common secret with A
(read dhpubPC1.pem; while ! [ -s dhpubPC1.pem ]; do sleep 1 ; done && openssl pkeyutl -derive -inkey dhkeyPC3.pem -peerkey dhpubPC1.pem -out secret1.bin) &

#receive public keys of B and generate common secret with B
(read dhpubPC2.pem; while ! [ -s dhpubPC2.pem ]; do sleep 1 ; done && openssl pkeyutl -derive -inkey dhkeyPC3.pem -peerkey dhpubPC2.pem -out secret2.bin) &
