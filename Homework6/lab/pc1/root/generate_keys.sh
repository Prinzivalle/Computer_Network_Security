#!/bin/bash

#mkdir /root/.keys
cd /root/keys

#generate private key
openssl genpkey -paramfile dhp.pem -out dhkeyPC1.pem
# openssl genrsa -out pc1.private 1024

#generate public key
openssl pkey -in dhkeyPC1.pem -pubout -out dhpubPC1.pem
# openssl rsa -in pc1.private -out pc1.public -pubout -outform PEM

#generate common secret with pc3
openssl pkeyutl -derive -inkey dhkeyPC1.pem -peerkey dhpubPC3.pem -out secret3.bin
