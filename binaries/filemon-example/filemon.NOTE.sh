#!/bin/bash
./filemon.pl --recursive --period=30 --primary=192.168.0.253 --secondary=192.168.0.1 --ssh-user=aig $PWD/test-dir $PWD/test-dir-2
