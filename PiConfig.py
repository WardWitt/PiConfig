import os

gateway = '192.168.1.1'
dns = '192.168.1.1'
sudoPassword =""

Addresses = {'b8:27:eb:74:2b:f4' : ('192.168.1.100', 'master'),
             'b8:27:eb:10:86:1a' : ('192.168.1.101', 's01'),
             'b8:27:eb:36:3c:15' : ('192.168.1.102', 's02'),
             'b8:27:eb:3e:2d:74' : ('192.168.1.103', 's03'),
             'b8:27:eb:43:4e:74' : ('192.168.1.104', 's04'),
             'b8:27:eb:47:04:b2' : ('192.168.1.105', 's05'),
             'b8:27:eb:4a:ea:c6' : ('192.168.1.106', 's06'),
             'b8:27:eb:62:b6:4f' : ('192.168.1.107', 's07'),
             'b8:27:eb:78:c0:e2' : ('192.168.1.108', 's08'),
             'b8:27:eb:84:7f:39' : ('192.168.1.109', 's09'),
             'b8:27:eb:95:21:f5' : ('192.168.1.110', 's10'),
             'b8:27:eb:9f:58:63' : ('192.168.1.111', 's11'),
             'b8:27:eb:b2:2c:34' : ('192.168.1.112', 's12'),
             'b8:27:eb:be:41:06' : ('192.168.1.113', 's13'),
             'b8:27:eb:e1:59:6c' : ('192.168.1.114', 's14'),
             'b8:27:eb:62:22:a4' : ('192.168.1.115', 'test01')}

def getMAC():
    try:
        str = open('/sys/class/net/wlan0/address').read()
    except:
        str = "00:00:00:00:00:00"
    return str[0:17]

def issueCommand(command):
    print(command)
    os.system('echo %s|sudo -S %s' %(sudoPassword, command))


try:
    macAddress = getMAC()
    currentHostname = open('/etc/hostname').read().rstrip()
    newHostname = Addresses[macAddress][1].rstrip()
    if currentHostname != newHostname:
        #Configuring /etc/hostname
        issueCommand('chown pi /etc/hostname')
        issueCommand('echo %s > /etc/hostname' %(newHostname))
        issueCommand('chown root /etc/hostname')
        
        #Configuring /etc/hosts
        issueCommand('chown pi /etc/hosts')
        # too hard to replace just the hostname.. replace the entire line
        issueCommand("sed -i 's/^\(127.0.1.1\).*//' /etc/hosts")
        issueCommand('echo "127.0.1.1       %s" >> /etc/hosts' %(Addresses[macAddress][1]))
        issueCommand('chown root /etc/hosts')
        
        #Configuring ip address /etc/dhcpcd.conf
        issueCommand('chown pi /etc/dhcpcd.conf')
        # make sure we dont have duplicate lines
        issueCommand("sed -i 's/^\(interface wlan0\).*//' /etc/dhcpcd.conf")
        issueCommand("sed -i 's/^\(static ip_address\).*//' /etc/dhcpcd.conf")
        issueCommand("sed -i 's/^\(static routers\).*//' /etc/dhcpcd.conf")
        issueCommand("sed -i 's/^\(static domain_name_servers\).*//' /etc/dhcpcd.conf")
        # create the new entries
        issueCommand('echo "interface wlan0" >> /etc/dhcpcd.conf')
        issueCommand('echo "static ip_address=%s/24" >> /etc/dhcpcd.conf' %(Addresses[macAddress][0]))
        issueCommand('echo "static routers=%s" >> /etc/dhcpcd.conf' %(gateway))
        issueCommand('echo "static domain_name_servers=%s" >> /etc/dhcpcd.conf' %(dns))
        issueCommand('chown root /etc/dhcpcd.conf')
        
        #Disable screen blanking
        # make sure we dont have duplicate lines E.G. cards got swapped between Pis
        issueCommand("sed -i 's/^\(@xset s off\)//' /home/pi/.config/lxsession/LXDE-pi/autostart")
        issueCommand("sed -i 's/^\(@xset -dpms\)//' /home/pi/.config/lxsession/LXDE-pi/autostart")
        issueCommand("sed -i 's/^\(@xset s noblank\)//' /home/pi/.config/lxsession/LXDE-pi/autostart")
        issueCommand('echo @xset s off >> /home/pi/.config/lxsession/LXDE-pi/autostart')
        issueCommand('echo @xset -dpms >> /home/pi/.config/lxsession/LXDE-pi/autostart')
        issueCommand('echo @xset s noblank >> /home/pi/.config/lxsession/LXDE-pi/autostart')
        
        # reboot
        issueCommand('reboot')    
    else:
        print('Already configured')
    
    
except:
    print('Not Found')
