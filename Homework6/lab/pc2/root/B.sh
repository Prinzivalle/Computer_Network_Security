#!/bin/bash

cd /root/keys/

####### start listening for incoming files
port=9001
(while true; do nc -l -p $port | tar -x; done)&
touch portB
echo $port > portB
tar -c portB | nc -q 0 1.0.1.6 9001

###### generate keys for B

#generate private key
openssl genpkey -paramfile dhp.pem -out dhkeyPC2.pem

#generate public key
openssl pkey -in dhkeyPC2.pem -pubout -out dhpubPC2.pem

#generate common secret with pc3
openssl pkeyutl -derive -inkey dhkeyPC2.pem -peerkey dhpubPC3.pem -out secret3.bin

####### send public key to pc3
tar -c dhpubPC2.pem | nc -q 0 1.0.1.6 9001

####### generate certificate for B

#generate private key for B for certificates
openssl genrsa -out B.key 2048

#generate Certificate Signing Request
echo -e '\n\n\n\n\n\n\n\n\n' |  openssl req -new -key B.key -out B.csr

#send CSR to C
tar -c B.csr | nc -q 0 1.0.1.6 9001
