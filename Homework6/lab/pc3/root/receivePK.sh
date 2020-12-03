#!/bin/bash

nc -l -p 9000 > /root/keys/pc1.public &
nc -l -p 9001 > /root/keys/pc2.public &
