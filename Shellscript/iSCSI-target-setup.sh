#!/bin/bash
# iSCSI Target machine Script to be run after modifying the file in the LUN 0.

# First create the Disk Storage:

sudo /sbin/mkfs -t ext4 /dev/sda1p3 2M

# Mount the disk storage (umount if it is already mounted) and create test file:
sudo rm /data/*.txt
sudo umount /dev/sda1p3
sudo mount /dev/sda1p3 /data/
sudo echo "Test ISCSI File" > /data/test.txt

# Restart Target:

sudo service iscsitarget restart

echo "Partition sda1p3 file system created and mounted on /data/. iscsitarget service restarted."
