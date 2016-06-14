#!/bin/bash
# iSCSI Initiator setup

umount /media/william/97a89aa9-7ae1-4641-87dd-593ea1fc525b
echo Insert target IP address:
read ip
sudo iscsiadm -m node --logout
sudo iscsiadm -m discovery -t st -p $ip
sudo iscsiadm -m node -T "iqn.2016-06.local.iit:storage.sys0" -p "$ip:3260" --login
sudo mount -t ext3 /dev/sdb