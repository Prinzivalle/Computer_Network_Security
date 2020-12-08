#!/bin/bash

#choose if authenticate A to B, put 1 if you want authentication of A
authA=0

cd /root/

####### start listening for incoming files
port=9000
(while true; do nc -l -p $port | tar -x; done)&
touch portA
echo $port > portA

#wait for ping, otherwise keys will not be sent
while ! timeout 0.2 ping -c 1 -n 1.0.1.5 &> /dev/null ; do sleep 1; done
while ! timeout 0.2 ping -c 1 -n 1.0.1.3 &> /dev/null ; do sleep 1; done
echo "start"
tar -c portA | nc -q 0 1.0.1.5 9000
tar -c portA | nc -q 0 1.0.1.3 9001

# use this directory to store all the keys
cd /root/keys/

###### generate keys for A

#generate private key for DH
openssl genpkey -paramfile dhp.pem -out dhkeyPC1.pem

#generate public key for DH
openssl pkey -in dhkeyPC1.pem -pubout -out dhpubPC1.pem

#generate common secret with pc3
openssl pkeyutl -derive -inkey dhkeyPC1.pem -peerkey dhpubPC3.pem -out secret3.bin

#generate RSA keys
openssl genrsa -out keypc1.pem 4096
openssl rsa -in keypc1.pem -out keypc1.pub -pubout

####### send public key to pc3
tar -c dhpubPC1.pem | nc -q 0 1.0.1.5 9000
sleep 1
tar -c keypc1.pub | nc -q 0 1.0.1.5 9000

####### generate certificate for A

#generate private key for A for certificates
openssl genrsa -out A.key 2048

#generate Certificate Signing Request
echo -e '\n\n\n\n\n\n\n\n\n' |  openssl req -new -key A.key -out A.csr

#send CSR to C
tar -c A.csr | nc -q 0 1.0.1.5 9000

####### request public key of B
touch B
echo "B\nB\n" > B
sleep 1
tar -c B | nc -q 0 1.0.1.5 9000

#verify file sent from B
cd /root/keys/
ead Db; while ! [ -s Db ]; do sleep 1 ; done
authB=1
sed -n "1p;" Db > timeB
sed -n '2p;' Db > A
sed -n '3,6p;' Db > secret1.enc
read A; while ! [ -s A ]; do sleep 1 ; done 
echo "A"
openssl pkeyutl -derive -inkey dhkeyPC1.pem -peerkey dhpubPC2.pem -out secret1.bin
read secret1.enc; while ! [ -s secret1.enc ]; do sleep 1 ; done && openssl rsautl -in secret1.enc -out secret1B.bin -inkey keypc1.pem -decrypt && if ! [ cmp -s secret1.bin secret1B.bin ] ; then (echo "cannot authenticate" && authB=0) fi
echo "authenticated"
verified="Verified OK"
signature=$(openssl dgst -sha256 -verify keypc2.pub -signature signDb.sha256 -binary Db)
if [ "$signature" != "$verified" ] ; then (echo "cannot authenticate" && authB=0) fi 
echo $authB

####### authenticate A to B
cd /root/
if [ "$authA" -eq "1" ]
then
	touch messages/authentication
	echo "authenticate me" > messages/authentication
	tar -c messages/authentication | nc -q 0 1.0.1.3 9001
	cd /root/keys
	timestamp() {
	  date +"%T" # current time
	}
	read dhpubPC2.pem; while ! [ -s dhpubPC2.pem ]; do sleep 1 ; done && openssl pkeyutl -derive -inkey dhkeyPC1.pem -peerkey dhpubPC2.pem -out secret2.bin 
	openssl rsautl -in secret2.bin -out secret2.enc -pubin -inkey keypc2.pub -encrypt
	touch Da
	timestamp > Da
	cat B >> Da
	cat secret2.enc >> Da
	openssl dgst -sha256 -sign keypc1.pem -out signDa.sha256 Da

	touch timeA
	timestamp > timeA

	# send files to B
	cd /root/
	tar -c keys/A.cer | nc -q 0 1.0.1.3 9001
	tar -c keys/Da | nc -q 0 1.0.1.3 9001
	tar -c keys/signDa.sha256 | nc -q 0 1.0.1.3 9001
else
	touch messages/authentication
	echo "no authentication, send" > messages/authentication
	tar -c messages/authentication | nc -q 0 1.0.1.3 9001
fi

# wait for ack then send messages to B
openssl dgst -sha256 -out keys/secret2.sha256 keys/secret1.bin
sleep 1
read messages/send; while ! [ -s messages/send ]; do sleep 2 ; done && openssl aes-256-cbc -in messages/foo1 -out messages/message1.enc -pass file:keys/secret2.sha256 && openssl dgst -sha256 -sign keys/keypc1.pem -out messages/message1.sha256 messages/message1.enc  && tar -c messages/message1.enc | nc -q 0 1.0.1.3 9001 && sleep 1 && tar -c messages/message1.sha256 | nc -q 0 1.0.1.3 9001
#read messages/send; while ! [ -s messages/send ]; do sleep 2 ; done && 
openssl aes-256-cbc -in messages/foo2 -out messages/message2.enc -pass file:keys/secret2.sha256 && openssl dgst -sha256 -sign keys/keypc1.pem -out messages/message2.sha256 messages/message2.enc  && tar -c messages/message2.enc | nc -q 0 1.0.1.3 9001 && sleep 1 && tar -c messages/message2.sha256 | nc -q 0 1.0.1.3 9001

