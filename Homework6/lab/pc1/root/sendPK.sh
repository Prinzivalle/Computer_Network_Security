#!/bin/bash

#nc -q 0 1.0.1.5 9000 < /root/keys/dhpubPC1.pem
cd /root/keys/
tar -c dhpubPC1.pem | nc -q 0 1.0.1.5 9000
