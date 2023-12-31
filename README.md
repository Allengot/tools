## mS-DS-CreatorSID.py
mS-DS-CreatorSID.py文件解决了Adfine.exe查看机器账号的mS-DS-CreatorSID属性和被杀软标记的麻烦。
### 如果运行出现问题请使用下面两个方法尝试
pip3 install python-ldap
  
pip3 install ldap3

### 使用方法
python3 mS-DS-CreatorSID.py -dc-ip 10.10.10.8 -u cv17 -p Admin12345 -dc "DC=redteam,DC=red" -computer-name computer -domain redteam.red -port 389

![image](https://github.com/Allengot/tools/blob/main/mS-DS-CreatorSID/mS-DS-CreatorSID.png)

## sid.py
sid.py解决了Adfine.exe查看机器账号的sid值的问题
### 使用方法
python3 sid.py -dc-ip 10.10.10.8 -p 389 -dc "DC=redteam,DC=red" -u cv17 -pw Admin12345 -sid S-1-5-21-1359007890-1682372173-1631803504-1131

![image](https://github.com/Allengot/tools/blob/main/sid/sid.png)

## Unconstrained.py
Unconstrained.py查看非约束委派的机器账户和普通账户
### 使用方法
###### 查询非约束委派机器账户和普通账户
python3 Unconstrained.py -dc-ip 10.10.10.8 -port 389 -u gu -p Gu12345 -dc 'DC=redteam,DC=red' -all
###### 查询非约束委派普通账户
python3 Unconstrained.py -dc-ip 10.10.10.8 -port 389 -u gu -p Gu12345 -dc 'DC=redteam,DC=red' -user
###### 查询非约束委派机器账户
python3 Unconstrained.py -dc-ip 10.10.10.8 -port 389 -u gu -p Gu12345 -dc 'DC=redteam,DC=red' -machine
