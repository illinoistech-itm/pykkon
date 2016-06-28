#!/bin/bash
# iSCSI Target machine Script using the following VM: 

# First create the Disk Storage:

sudo /sbin/mkfs -t ext4 /dev/sda1p3 2M

# Mount the disk storage and create test file:

sudo mount /dev/sda1p3 /data/
sudo echo "Test ISCSI File" > /data/test.txt

# Restart Target:

sudo service iscsitarget restart

echo "Partition sda1p3 file system created and mounted on /data/. iscsitarget service restarted."
