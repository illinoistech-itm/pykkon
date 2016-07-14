# Initiator iSCSI CentOS shell script

yum -y install iscsi-initator-utils
cd /etc/iscsi
vim initiatorname.iscsi 
> Initiatorname=iqn.2016-06.edu.iit.example:client.initiator
systemctl restart iscsid
systemctl enable iscsid
