#!/bin/bash

#mkdir /root/.keys
cd /root/keys

#generate private key
openssl genrsa -out pc1.private 1024

#generate public key
openssl rsa -in pc1.private -out pc1.public -pubout -outform PEM
