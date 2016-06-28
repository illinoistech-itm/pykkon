# BSMP-2016-ISCSI-Packet-Injection
This is a repo that contains code for creating a system to hijack and insert data into an iSCSI stream

INSTALL
------------
1 - Open Target and Initiator .Vagrantfile folder and run $ bash vagrant up

2.a - On Initiator, run:

$ bash sudo iscsiadm -m discovery -t st -p "target_ip" 

$ bash sudo iscsiadm -m node -T "iqn.2016-06.local.iit:storage.sys0" -p "target_ip" --login

$ bash sudo iscsiadm -m discovery -t st -p "target_ip"

$ bash sudo iscsiadm -m node -T "iqn.2016-06.local.iit:storage.sys0" -p "target_ip" --login

2.b - On Target, make sure iscsitarget service is running:

$ bash netstat -tl
