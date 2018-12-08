import os

sudoPassword = 'CWFcwf1234!'

Addresses = {'b8:27:eb:10:86:1a' : ('192.168.1.101', 's01'),
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
             'b8:27:eb:e1:59:6c' : ('192.168.1.114', 's14')}

def getMAC():
    try:
        str = open('/sys/class/net/wlan0/address').read()
    except:
        str = "00:00:00:00:00:00"
    return str[0:17]

def issueCommand(command):
    print(command)
    print(os.system('echo %s|sudo -S %s' %(sudoPassword, command)))


try:
    macAddress = getMAC()
    currentHostname = open('/etc/hostname').read().rstrip()
    newHostname = Addresses[macAddress][1].rstrip()
    if currentHostname != newHostname:
        print('Configuring hostname')
        issueCommand('chown pi /etc/hostname')
        issueCommand('echo %s > /etc/hostname' %(newHostname))
        issueCommand('chown root /etc/hostname')
        print('Configuring ip address')
        issueCommand('chown pi /etc/dhcpcd.conf')
        issueCommand('echo "interface wlan0" >> /etc/dhcpcd.conf')
        issueCommand('echo "static ip_address=%s/24" >> /etc/dhcpcd.conf' %(Addresses[macAddress][0]))
        issueCommand('chown root /etc/dhcpcd.conf')
        issueCommand('reboot')    
    else:
        print('Already configured')
    
    #command = 'chown pi /etc/dhcpcd.conf'
    #print(os.system('echo %s|sudo -S %s' %(sudoPassword, command)))
     
    #command = 'echo "interface wlan0" >> /etc/dhcpcd.conf'
    #print(os.system('echo %s|sudo -S %s' %(sudoPassword, command)))

    #command = 'echo "static ip_address=%s/24" >> /etc/dhcpcd.conf' %(Addresses[mac][0])
    #print(os.system('echo %s|sudo -S %s' %(sudoPassword, command)))

    #command = 'chown root /etc/dhcpcd.conf'
    #print(os.system('echo %s|sudo -S %s' %(sudoPassword, command)))


    
except:
    print('Not Found')