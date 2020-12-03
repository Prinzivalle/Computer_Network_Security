#!/bin/bash

cd /root/keys

#receive public keys of A and generate common secret with A
(nc -l -p 9000 > /root/keys/dhpubPC1.pem && openssl pkeyutl -derive -inkey dhkeyPC3.pem -peerkey dhpubPC1.pem -out secret1.bin) &

#receive public keys of B and generate common secret with B
(nc -l -p 9001 > /root/keys/dhpubPC2.pem && openssl pkeyutl -derive -inkey dhkeyPC3.pem -peerkey dhpubPC2.pem -out secret2.bin) &

#cd /root/keys

#generate common secret with A
#openssl pkeyutl -derive -inkey dhkeyPC3.pem -peerkey dhpubPC1.pem -out secret1.bin

#generate common secret with B
#openssl pkeyutl -derive -inkey dhkeyPC3.pem -peerkey dhpubPC2.pem -out secret2.bin
