#!/bin/bash

cd /root/keys/

####### start listening for incoming files
(while true; do nc -l -p 9001 | tar -x; done)&

###### generate keys for B

#generate private key
openssl genpkey -paramfile dhp.pem -out dhkeyPC2.pem

#generate public key
openssl pkey -in dhkeyPC2.pem -pubout -out dhpubPC2.pem

#generate common secret with pc3
openssl pkeyutl -derive -inkey dhkeyPC2.pem -peerkey dhpubPC3.pem -out secret3.bin

####### send public key to pc3
tar -c dhpubPC2.pem | nc -q 0 1.0.1.6 9001
