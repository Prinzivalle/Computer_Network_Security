#!/bin/bash

cd /root/keys/

###### generate keys for A

#generate private key
openssl genpkey -paramfile dhp.pem -out dhkeyPC1.pem

#generate public key
openssl pkey -in dhkeyPC1.pem -pubout -out dhpubPC1.pem

#generate common secret with pc3
openssl pkeyutl -derive -inkey dhkeyPC1.pem -peerkey dhpubPC3.pem -out secret3.bin

####### send public key
tar -c dhpubPC1.pem | nc -q 0 1.0.1.5 9000
