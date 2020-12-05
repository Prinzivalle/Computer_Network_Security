#!/bin/bash

#nc -q 0 1.0.1.6 9001 < /root/keys/dhpubPC2.pem
cd /root/keys/
tar -c dhpubPC2.pem | nc -q 0 1.0.1.6 9001
