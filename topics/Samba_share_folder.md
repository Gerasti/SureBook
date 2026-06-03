
### Настройка Samba для анонимного доступа <!-- HEAD -->

#### Создание общей директории <!-- NAME -->

```CODE
mkdir /opt/data                                                                          
chmod 777 /opt/data                                                                         
```

> 777(полные права для всех пользователей)

#### В /etc/samba/smb.conf добавить секцию <!-- NAME -->

```CODE
[samba]                                                                                  
path = /opt/data                                                                            
browseable = yes                                                                            
writable = yes                                                                              
guest ok = yes                                                                              
read only = no                                                                              
force user = nobody                                                                         
```

> guest ok = yes(анонимный доступ); force user(все действия от имени nobody)

#### Перезапуск службы <!-- NAME -->

```CODE
systemctl restart smbd                                                                   

```

### Настройка Samba для пользователей домена <!-- HEAD -->

#### Создание общей директории <!-- NAME -->

```CODE
mkdir /opt/data
chmod 770 /opt/data                                                                         
chown root:domain_users /opt/data                                                           
```

> 770(доступ только владельцу и группе); domain_users(группа домена)

#### В /etc/samba/smb.conf добавить секцию <!-- NAME -->

```CODE
[samba]                                                                                  
path = /opt/data                                                                            
browseable = yes                                                                            
writable = yes                                                                              
valid users = @domain_users                                                                 
read only = no                                                                              
create mask = 0660                                                                          
directory mask = 0770                                                                       
```

> valid users = @domain_users(доступ только группе домена); create mask(права на новые файлы); directory mask(права на новые каталоги)

#### Добавление пользователя Samba <!-- NAME -->

```CODE
smbpasswd -a username
```

> создает пароль Samba для существующего системного пользователя

### Настройка Samba для конкретных пользователей <!-- HEAD -->

#### В /etc/samba/smb.conf добавить секцию <!-- NAME -->

```CODE
[samba]      
path = /opt/data                                                                            
browseable = yes                                                                            
writable = yes                                                                              
valid users = user1, user2, user3                                                           
read only = no                                                                              
write list = user1, user2                                                                   
```

> valid users(список разрешенных пользователей); write list(пользователи с правом записи)

### Описание основных опций Samba <!-- HEAD -->

#### Опции доступа <!-- NAME -->

```CODE
browseable = yes
guest ok = yes                                                                              
valid users = user1, @group1                                                                
invalid users = user2                                                                       
read only = no                                                                              
writable = yes                                                                              
write list = user1, @group1                                                                 
read list = user2                                                                           
```

> browseable(видимость в сети); guest ok(гостевой доступ); valid users(разрешенные пользователи/группы); invalid users(запрещенные); write list(право записи); read list(только чтение)

#### Опции прав доступа <!-- NAME -->

```CODE
create mask = 0660
directory mask = 0770                                                                       
force user = nobody                                                                         
force group = nogroup                                                                       
inherit permissions = yes                                                                   
```

> create mask(права на файлы); directory mask(права на каталоги); force user/group(принудительный владелец); inherit permissions(наследование прав)

#### Опции безопасности <!-- NAME -->

```CODE
hosts allow = 192.168.1.0/24
hosts deny = 192.168.2.0/24                                                                 
max connections = 10                                                                        
```

> hosts allow(разрешенные сети); hosts deny(запрещенные сети); max connections(лимит подключений)

### Проверка <!-- HEAD -->

#### Проверка конфигурации <!-- NAME -->

```CODE
testparm     
```

> проверяет синтаксис smb.conf

#### Просмотр активных подключений <!-- NAME -->

```CODE
smbstatus                                                                                
```

> показывает подключенных пользователей и открытые файлы

#### Подключение с клиента Windows <!-- NAME -->

```CODE
\\192.168.1.1\samba                                                                      
```

> в проводнике Windows

#### Подключение с клиента Linux <!-- NAME -->

```CODE
smb://192.168.1.1/samba                                                                  
```

> в файловом менеджере или через smbclient
