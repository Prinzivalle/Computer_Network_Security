#!/bin/bash

# use this directory to store all the keys
cd /root/keys/

####### start listening for incoming files
#port=9000
(while true; do nc -l -p 9000 | tar -x; done)&
#touch portA
#echo $port > portA
#tar -c portA | nc -q 0 1.0.1.5 9000

#wait for ping, otherwise keys will not be sent
while ! timeout 0.2 ping -c 1 -n 1.0.1.5 &> /dev/null ; do sleep 1; done

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

####### authenticate A to B

timestamp() {
  date +"%T" # current time
}
read dhpubPC2.pem; while ! [ -s dhpubPC2.pem ]; do sleep 1 ; done && openssl pkeyutl -derive -inkey dhkeyPC1.pem -peerkey dhpubPC2.pem -out secret2.bin 
openssl rsautl -in secret2.bin -out secret2.enc -pubin -inkey keypc2.pub -encrypt
Da=(timestamp B secret2.enc)
touch Da
timestamp > Da
cat B >> Da
cat secret2.enc >> Da
openssl dgst -sha256 -sign keypc1.pem -out signDa.sha256 Da
