# mS-DS-CreatorSID.py
mS-DS-CreatorSID.py文件解决了Adfine.exe查看机器账号的mS-DS-CreatorSID属性和被杀软标记的麻烦。
### 如果运行出现问题请使用下面两个方法尝试
pip3 install python-ldap
  
pip3 install ldap3

### 使用方法
python3 mS-DS-CreatorSID.py -dc-ip 10.10.10.8 -u cv17 -p Admin12345 -dc "DC=redteam,DC=red" -computer-name computer -domain redteam.red -port 389

![image](https://github.com/Allengot/tools/blob/main/mS-DS-CreatorSID/mS-DS-CreatorSID.png)
