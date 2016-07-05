#!/bin/bash
# iSCSI Initiator setup

echo Insert target IP address:
read ip
sudo iscsiadm -m node --logout
sudo iscsiadm -m discovery -t st -p $ip
sudo iscsiadm -m node -T "iqn.2016-06.local.iit:storage.sys0" -p "$ip:3260" --login

sudo mount /dev/sdc /mnt || sudo mount /dev/sdc /mnt || sudo mount /dev/sdd /mnt || sudo mount /dev/sdd /mnt