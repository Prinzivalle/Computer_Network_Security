#!/bin/bash

# mkdir /root/.keys
cd /root/keys

#generate private key
openssl genrsa -out pc2.private 1024

#generate public key
openssl rsa -in pc2.private -out pc2.public -pubout -outform PEM
