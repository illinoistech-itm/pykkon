#!/bin/bash
# iSCSI Target machine Script to be run after modifying the file in the LUN 0.

# First create the file system:
sudo /sbin/mkfs -t ext4 /dev/sda1p3 2M

# Mount the disk storage (umount if it is already mounted) and create test file:
sudo rm /data/*.txt

#umount before trying mount
sudo umount /dev/sda1p3
# as this script containts mounting commands, do not run on the script mount point folder (/data)
sudo mount /dev/sda1p3 /data/
sudo echo "Test ISCSI File" > /data/test.txt

# Restart Target:

sudo service iscsitarget restart

echo "Partition sda1p3 file system created and mounted on /data/. iscsitarget service restarted."
