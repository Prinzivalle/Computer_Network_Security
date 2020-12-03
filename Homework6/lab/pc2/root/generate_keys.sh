#!/bin/bash

# mkdir /root/.keys
cd /root/keys

#generate private key
openssl genpkey -paramfile dhp.pem -out dhkeyPC2.pem
#openssl genrsa -out pc2.private 1024

#generate public key
openssl pkey -in dhkeyPC2.pem -pubout -out dhpubPC2.pem
#openssl rsa -in pc2.private -out pc2.public -pubout -outform PEM
