#!/bin/bash

nc -l -p 9000 > /root/keys/dhpubPC1.pem &
nc -l -p 9001 > /root/keys/dhpubPC2.pem &
