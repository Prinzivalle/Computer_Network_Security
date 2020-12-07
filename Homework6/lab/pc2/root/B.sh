#!/bin/bash

cd /root/

####### start listening for incoming files
port=9001
(while true; do nc -l -p $port | tar -x; done)&
touch portB
echo $port > portB
tar -c portB | nc -q 0 1.0.1.6 9001

#wait for ping, otherwise keys will not be sent
while ! timeout 0.2 ping -c 1 -n 1.0.1.6 &> /dev/null; do sleep 1; done
while ! timeout 0.2 ping -c 1 -n 1.0.1.2 &> /dev/null; do sleep 1; done
echo "start"

# use this directory to store all the keys
cd /root/keys

###### generate keys for B

#generate private key for DH
openssl genpkey -paramfile dhp.pem -out dhkeyPC2.pem

#generate public key for DH
openssl pkey -in dhkeyPC2.pem -pubout -out dhpubPC2.pem

#generate common secret with pc3
openssl pkeyutl -derive -inkey dhkeyPC2.pem -peerkey dhpubPC3.pem -out secret3.bin

#generate RSA keys
openssl genrsa -out keypc2.pem 4096
openssl rsa -in keypc2.pem -out keypc2.pub -pubout

####### send public key to pc3
tar -c dhpubPC2.pem | nc -q 0 1.0.1.6 9001
sleep 1
tar -c keypc2.pub | nc -q 0 1.0.1.6 9001

####### generate certificate for B

#generate private key for B for certificates
openssl genrsa -out B.key 2048

#generate Certificate Signing Request
echo -e '\n\n\n\n\n\n\n\n\n' |  openssl req -new -key B.key -out B.csr

#send CSR to C
tar -c B.csr | nc -q 0 1.0.1.6 9001

####### verify A authentication

#request A public key
touch A
echo "A\nA\n" > A
sleep 1
tar -c A | nc -q 0 1.0.1.6 9001

#verify file sent from A
auth=1
read B; while ! [ -s B ]; do sleep 1 ; done 
openssl pkeyutl -derive -inkey dhkeyPC2.pem -peerkey dhpubPC1.pem -out secret2.bin
read secret2.enc; while ! [ -s secret2.enc ]; do sleep 1 ; done && openssl rsautl -in secret2.enc -out secret2A.bin -inkey keypc2.pem -decrypt && if ! [ cmp -s secret2.bin secret2A.bin ] ; then (echo "cannot authenticate" && auth=0) fi
openssl rsautl -in secret2.enc -out secret2.bin -inkey keypc2.pem -decrypt
verified="Verified OK"
signature=openssl dgst -sha256 -verify keypc1.pub -signature signDa.sha256 -binary Da
if [ "$signature" != "$verified" ] ; then (echo "cannot authenticate" && auth=0) fi 
echo $auth

####### send clear to send to A and decrypt received messages
cd /root
if [ "$auth" -eq "1" ] 
then 
  	tar -c messages/send | nc -q 0 1.0.1.2 9000
  	cd /root/
  	#openssl pkeyutl -derive -inkey dhkeyPC2.pem -peerkey dhpubPC1.pem -out secret2.bin
	openssl dgst -sha256 -out keys/secret2.sha256 keys/secret2.bin
	#cd /root
	read messages/message1.enc; while ! [ -s messages/message1.enc ]; do sleep 1 ; done 
	openssl aes-256-cbc -d -in messages/message1.enc -out messages/foo1 -pass file:keys/secret2.sha256
	read messages/message2.enc; while ! [ -s messages/message2.enc ]; do sleep 1 ; done 
	openssl aes-256-cbc -d -in messages/message2.enc -out messages/foo2 -pass file:keys/secret2.sha256
fi

