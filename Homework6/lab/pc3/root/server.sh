#!/bin/bash

# use this directory to store all the keys
cd /root/keys/

######## starting server
# user A
(while true; do nc -l -p 9000 | tar -x; done)&

# user B
(while true; do nc -l -p 9001 | tar -x; done)&

#wait for ping, otherwise keys will not be sent
while ! ( timeout 0.2 ping -c 1 -n 1.0.1.4 &> /dev/null ) ; do sleep 1; done
while ! ( timeout 0.2 ping -c 1 -n 1.0.1.7 &> /dev/null ) ; do sleep 1; done
echo "start"

######## certificate autority
# create CA key
openssl genrsa -aes256 -out CA_key.private -passout pass:8%0%Zef6kbBvG0g 4096

# create root certificate
echo -e '\n\n\n\n\n\n\n' | openssl req -x509 -new -nodes -key CA_key.private -sha256 -days 1825 -out CA_root.pem -passin pass:8%0%Zef6kbBvG0g

######## receive public keys

# generate common secret with A
(read dhpubPC1.pem; while ! [ -s dhpubPC1.pem ]; do sleep 1 ; done && openssl pkeyutl -derive -inkey dhkeyPC3.pem -peerkey dhpubPC1.pem -out secret1.bin) &

#generate common secret with B
(read dhpubPC2.pem; while ! [ -s dhpubPC2.pem ]; do sleep 1 ; done && openssl pkeyutl -derive -inkey dhkeyPC3.pem -peerkey dhpubPC2.pem -out secret2.bin) &

######## generate certificate of A and B and send them back

cd /root/
pA=$(head -n 1 keys/portA)
echo $pA
#pB=$(head -n 1 keys/portB)
#echo $pB
(read keys/A.csr; while ! [ -s keys/A.csr ]; do sleep 1 ; done && openssl x509 -req -in keys/A.csr -CA keys/CA_root.pem -CAkey keys/CA_key.private -passin pass:8%0%Zef6kbBvG0g -CAcreateserial -out keys/A.cer -days 1 -sha256 && tar -c keys/A.cer | nc -q 0 1.0.1.4 $pA ) &
#(read keys/B.csr; while ! [ -s keys/B.csr ]; do sleep 1 ; done && openssl x509 -req -in keys/B.csr -CA keys/CA_root.pem -CAkey keys/CA_key.private -passin pass:8%0%Zef6kbBvG0g -CAcreateserial -out keys/B.cer -days 1 -sha256 && tar -c keys/B.cer | nc -q 0 1.0.1.7 $pB ) &

#(read keys/A.csr; while ! [ -s keys/A.csr ]; do sleep 1 ; done && openssl x509 -req -in keys/A.csr -CA keys/CA_root.pem -CAkey keys/CA_key.private -passin pass:8%0%Zef6kbBvG0g -CAcreateserial -out keys/A.cer -days 1 -sha256 && tar -c keys/A.cer | nc -q 0 1.0.1.4 9000 ) &
(read keys/B.csr; while ! [ -s keys/B.csr ]; do sleep 1 ; done && openssl x509 -req -in keys/B.csr -CA keys/CA_root.pem -CAkey keys/CA_key.private -passin pass:8%0%Zef6kbBvG0g -CAcreateserial -out keys/B.cer -days 1 -sha256 && tar -c keys/B.cer | nc -q 0 1.0.1.7 9001 ) &

######## send public keys to whom asked it

(read keys/B; while ! [ -s keys/B ]; do sleep 1 ; done && (tar -c keys/keypc2.pub | nc -q 0 1.0.1.4 $pA) && (tar -c keys/dhpubPC2.pem | nc -q 0 1.0.1.4 $pA) )& #&& (rm keys/B)) &
(read keys/A; while ! [ -s keys/A ]; do sleep 1 ; done && (tar -c keys/keypc1.pub | nc -q 0 1.0.1.7 9001) && (tar -c keys/dhpubPC1.pem | nc -q 0 1.0.1.7 9001) )& #&& (rm keys/A)) &
