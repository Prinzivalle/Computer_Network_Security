#!/bin/bash

cd /root/keys/

####### start listening for incoming files
(while true; do nc -l -p 9000 | tar -x; done)&
touch portA
echo "9000" > portA
tar -c portA | nc -q 0 1.0.1.5 9000

###### generate keys for A

#generate private key
openssl genpkey -paramfile dhp.pem -out dhkeyPC1.pem

#generate public key
openssl pkey -in dhkeyPC1.pem -pubout -out dhpubPC1.pem

#generate common secret with pc3
openssl pkeyutl -derive -inkey dhkeyPC1.pem -peerkey dhpubPC3.pem -out secret3.bin

####### send public key to pc3
tar -c dhpubPC1.pem | nc -q 0 1.0.1.5 9000

####### generate certificate for A

#generate private key for A for certificates
openssl genrsa -out A.key 2048

#generate Certificate Signing Request
echo -e '\n\n\n\n\n\n\n\n\n' |  openssl req -new -key A.key -out A.csr

#send CSR to C
tar -c A.csr | nc -q 0 1.0.1.5 9000
