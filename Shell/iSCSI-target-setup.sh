#!/bin/bash
# iSCSI Target machine Script using the following VM: https://drive.google.com/drive/folders/0B3zw9iQqnZcSNjBDZXpmMnhiWEE

# First create the Disk Storage:

sudo /sbin/mkfs -t ext3 /dev/sda1p3 2M

# Mount the disk storage:

sudo mount /dev/sda1p3 /data/

# Restart Target:

sudo service iscsitarget restart

echo "Partition sda1p3 file system created and mounted on /data/. iscsitarget service restarted."
