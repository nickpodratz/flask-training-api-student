#!/bin/bash

mkdir .ssh
set +x
echo "$ID_RSA" > .ssh/id_rsa
echo "$ID_RSA_PUB" > .ssh/id_rsa.pub
echo "$KNOWN_HOSTS" > .ssh/known_hosts
set -x

chmod 600 .ssh/*
