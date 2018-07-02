### hp19xx-connect
connecting hp1910, 1920



### You must install the pexpect module  
```
pip install pexpect
```

How use it:  

#import this file is your project  
from hp19xx_connect import ConnectHP19xx  
#Connecting devices [ip, login, password, factory_password]  
con = ConnectHP19xx('192.168.1.1', 'admin', 'admin', '512900')  


#send_hp19xx - returns a string. By default, nothing shows up on the screen  
con.send_hp19xx('display version', show=True) # This print version device  

## Example ntp configuration   
```
from hp19xx_connect import ConnectHP19xx  

con = ConnectHP19xx('192.168.1.1', 'cisco', 'cisco', '512900')  
if con.get_status_connect is False:  
    exit(0)  
con.send_hp19xx('sys')  
con.send_hp19xx('ntp-service unicast-server 192.168.1.1')  
con.send_hp19xx('save force')  
```

