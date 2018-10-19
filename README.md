# Shinken_SSH_Plugins (Documentation in Progress)
<a href="http://bitly.com/2grT54q"><img src="https://cdn.codementor.io/badges/i_am_a_codementor_dark.svg" alt="I am a codementor" style="max-width:100%"/></a><a href="http://bitly.com/2grT54q"><img src="http://www.shinken-monitoring.org/img/LogoFrameworkBlack.png" height="50"> 
 [![Donate](https://www.paypalobjects.com/en_US/i/btn/btn_donateCC_LG.gif)](https://www.paypal.com/cgi-bin/webscr?cmd=_s-xclick&hosted_button_id=WX4EKLLLV49WG)

## Desciption :

In a cloud environment you don't have the configuration of the target machine before deploying it, so monitoring the machine over ssh it's a best compromise that handle this problem, shinken is a full open source project written in python fron nagios core, and with this couple of plugins you have the heavy artillery to deploy and supervise your AWS / AZURE / GCP host from on-premise wether you have an hybrid cloud or a full public cloud

## Common option :
```python
'-H', '--hostname',
                  dest="hostname", help='Hostname to connect to')
parser.add_option('-p', '--port',
                  dest="port", type="int", default=22,
                  help='SSH port to connect to. Default : 22')
parser.add_option('-i', '--ssh-key',
                  dest="ssh_key_file",
                  help='SSH key file to use. By default will take ~/.ssh/id_rsa.')
parser.add_option('-u', '--user',
                  dest="user", help='remote use to use. By default shinken.')
parser.add_option('-P', '--passphrase',
```
'-H', '--hostname' : Hostname to connect to

'-p', '--port' : the host ssh port default to 22

'-i', '--ssh-key' : required ssh key file

'-u', '--user' : remote use to use. By default shinken

'-P', '--passphrase' : the passphrase default to null

### Check cpu stats

```bash
check_cpu_stats_by_ssh.py -H [Hostname]  -p [Port] -i [SSH Key File] -u [User] -P [Passphrase]
```
### Check Marathon services
This programme check the service runing uder marathon if it's in running state or in failed stat

Option :

'-C', '--container : the service or container to check

'-M' : The name of the dcos master 

```bash
check_marathon_services.py	-C kafka -M master001.leader  -H [Hostname]  -p [Port] -i [SSH Key File] -u [User] -P [Passphrase]
```
### Check ntp sync
```bash
check_ntp_sync_by_ssh.py	  -H [Hostname]  -p [Port] -i [SSH Key File] -u [User] -P [Passphrase]
```
### Check ssh proxy	
```bash
check_ssh_proxy_check.py	 -H [Hostname]  -p [Port] -i [SSH Key File] -u [User] -P [Passphrase]
```
### Check test
```bash
check_test.py -H [Hostname]  -p [Port] -i [SSH Key File] -u [User] -P [Passphrase]
```
### Check disks	
```bash
check_disks_by_ssh.py	-H [Hostname]  -p [Port] -i [SSH Key File] -u [User] -P [Passphrase]
```
### Check mdadm		
```bash
check_mdadm_by_ssh.py	-H [Hostname]  -p [Port] -i [SSH Key File] -u [User] -P [Passphrase]
```
### Check processes
```bash
check_processes_by_ssh.py  -H [Hostname]  -p [Port] -i [SSH Key File] -u [User] -P [Passphrase]
```
### Check Systemd services	
This programme check the Linux service controled by Systemd

Option :

'-S', '--service', the systemd service to check 
```bash
check_systemd_services.py  -S kafka -H [Hostname]  -p [Port] -i [SSH Key File] -u [User] -P [Passphrase]
```
### Check Uptime
```bash
check_uptime_by_ssh.py  -H [Hostname]  -p [Port] -i [SSH Key File] -u [User] -P [Passphrase]
```
### Check Disks stats
```bash
check_disks_stats_by_ssh.py -H [Hostname]  -p [Port] -i [SSH Key File] -u [User] -P [Passphrase]
```
### Check Memory		
```bash
check_memory_by_ssh.py -H [Hostname]  -p [Port] -i [SSH Key File] -u [User] -P [Passphrase]
```
### Check Readonly filesystem	
```bash
check_ro_filesystem_by_ssh.py -H [Hostname]  -p [Port] -i [SSH Key File] -u [User] -P [Passphrase]
```
### Check if a Systemd services is active	
```bash
check_systemd_services_isactive.py -H [Hostname]  -p [Port] -i [SSH Key File] -u [User] -P [Passphrase]
```
### schecks
```bash
schecks.py -H [Hostname]  -p [Port] -i [SSH Key File] -u [User] -P [Passphrase]
```
### Check Kernel stats	
```bash
check_kernel_stats_by_ssh.py -H [Hostname]  -p [Port] -i [SSH Key File] -u [User] -P [Passphrase]
```
### Check Net stats		
```bash
check_net_stats_by_ssh.py	 -H [Hostname]  -p [Port] -i [SSH Key File] -u [User] -P [Passphrase]
```
### Check Yum Security Updates		
```bash
check_sec_updates.py -H [Hostname]  -p [Port] -i [SSH Key File] -u [User] -P [Passphrase]
```
### Check if a Systemd services is enabled
```bash
check_systemd_services_isenabled.py -H [Hostname]  -p [Port] -i [SSH Key File] -u [User] -P [Passphrase]
```
### Check Load Average
```bash
check_load_average_by_ssh.py	 -H [Hostname]  -p [Port] -i [SSH Key File] -u [User] -P [Passphrase]
```
### Check NFS Stats		
```bash
check_nfs_stats_by_ssh.py -H [Hostname]  -p [Port] -i [SSH Key File] -u [User] -P [Passphrase]
```
### Check SSH connexion		
```bash
check_ssh_connexion.py -H [Hostname]  -p [Port] -i [SSH Key File] -u [User] -P [Passphrase]
```
### Check Tcp States
```bash
check_tcp_states_by_ssh.py -H [Hostname]  -p [Port] -i [SSH Key File] -u [User] -P [Passphrase]
```
