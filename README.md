# BSMP-2016-ISCSI-Packet-Injection
This is a repo that contains code for creating a system to hijack and insert data into an iSCSI stream

INSTALL
------------
1 - Open Target and Initiator .Vagrantfile folder and run $ bash vagrant up

2.a - On Initiator, run:

	- Run the iSCSI-initiator-setup.sh in the root folder. That script contains commands to discover and login to a target LUN. You have to provide the target machine IP as required by the script.

	- after login, a disk is created to represent the iSCSI target LUN.	Such disk can be on sdb, sdc or sdd, accordingly with the order it was found. Check which one represents the iSCSI Target LUN running the command "sudo fdisk -l". The disk representing the iSCSI Target LUN has 2MB of size.

	- Once the disk was identified, open /mnt directory to access the Target LUN. A mounting command was issued to serve the disk in such folder.

2.b - On Target:

	- make sure iscsitarget service is running:

		$ bash netstat -tl

  	- download, add execution permissions and run the iSCSI-target-setup.sh if you want to test a new file being available in the LUN 0. Also run the script on up after halting the machine.


 3 - MiTM machine:

 	- Download .ova machine on https://drive.google.com/open?id=0B4MZu1rZKHeDaC1WUkdGc1BhZGc

 	- import appliance on Virtualbox. Use username as root and password as admin.

 	- Insert target and initiator IPs on mitm-arp.py script and run to begin arp poisoning.

 	- Insert target and initiator IPs and MACs on ip_forward.py and run to start the packet sniffing, forwarding and injection.

