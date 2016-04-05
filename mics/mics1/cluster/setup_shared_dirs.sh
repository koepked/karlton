#!/bin/bash

mkdir -p /shared/root/.ssh
chmod 700 /shared/root/.ssh
ssh-keygen -f /shared/root/.ssh/id_rsa -t rsa -N ''
cp /shared/root/.ssh/id_rsa.pub /shared/root/.ssh/authorized_keys
chmod 600 /shared/root/.ssh/authorized_keys
dd if=/dev/urandom bs=1 count=1024 > /shared/shared/munge.key
chmod 600 /shared/shared/munge.key
echo "Host *" > /shared/root/.ssh/config
echo "    StrictHostKeyChecking no" >> /shared/root/.ssh/config
rm -rf /shared/root/.ssh/known_hosts
