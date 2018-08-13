#!/bin/bash

echo "Adding IxChariot Performance Endpoints"

apt-get update -y
apt-get upgrade -y

wget http://10.246.240.100/ixia/pelinux_amd64_93.tar.gz
tar -xvf pelinux_amd64_93.tar.gz
./endpoint.install accept_license 10.246.240.130
cp /usr/local/Ixia/rc2exec.lnx /etc/init.d/endpoint
update-rc.d endpoint defaults
