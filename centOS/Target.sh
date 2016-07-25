# Commands run in the second time of the installation of the CentOS
# IMPORTANT TO RUN AS ROOT USER AND NOT TARGET USER

# username: root
# password: admin

# list all disks
# important to create an extra storage disk
lsblk

# Partition the storage disk
fdisk /dev/sdb
# Message given after using the first SUDO command:
# We trust you have received the usual lecture from the local System
# administrator. It usually boils down to these three things:

#		#1) Respect the privacy of others.
#		#2) Think before you type.
#		#3) With great power comes great responsability.
> n
> p
> ENTER
> ENTER
> ENTER

# Create Physical Volume
pvcreate /dev/sdb1

# Create Volume Group
vgcreate vg_iscsi /dev/sdb1

# Install iSCSI target utilities
yum -y install targetcli

# Run targetcli
targetcli
> cd backstores/fileio/
> create disk01 /dev/sdb1
> cd /iscsi
> create iqn.2016-06.edu.iit.example:storage.target00
> cd iqn.2016-06.edu.iit.example:storage.target00/tpg1/portals
# Create the private IP address, for example, 192.168.1.156
> create 192.168.1.156
> cd ../luns
# Create the Logical Unit Number
> create backstores/fileio/disk01
> cd ../acls
# Create the Initiator
> create iqn.2016-06.edu.iit.example:client.initiator
# No authentication
> exit

# Show iSCSI listening
netstat -lnp | grep 3260

# Enable Firewall
firewall-cmd --zone=internal --add-port=3260/tcp --permanent
# Reload firewall config
firewall-cmd --reload

# Create a file system in the sdb1 partition
mkfs.ext3 /dev/sdb1

# Create directory for iscsi storage
mkdir /mnt/iscsi-storage

# Mount the sdb1 partition
mount /dev/sdb1 /mnt/iscsi-storage



