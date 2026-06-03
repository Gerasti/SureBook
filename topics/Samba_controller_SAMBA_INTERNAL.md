
### Установка Samba DC <!-- HEAD -->

#### Установка пакетов <!-- NAME -->

```CODE
apt-get update && apt-get install -y task-samba-dc                                       
```

> task-samba-dc(Samba DC на базе Heimdal Kerberos)

#### Остановка конфликтующих служб <!-- NAME -->

```CODE
for i in smb nmb krb5kdc slapd bind; do systemctl disable $i --now; done                 
```

> Samba DC использует собственные LDAP и Kerberos

### Настройка имени узла и домена <!-- HEAD -->

#### В /etc/sysconfig/network <!-- NAME -->

```CODE
HOSTNAME=dc.domain.sample
```

> dc.domain.sample(FQDN сервера); domain.sample(имя домена)

#### Установка имени узла <!-- NAME -->

```CODE
hostnamectl set-hostname dc.domain.sample                                                  
exec bash                                                                                   
domainname domain.sample                                                                      
```

> exec bash(перезагрузка оболочки для применения)

#### В /etc/resolvconf.conf <!-- NAME -->

```CODE
nameserver 127.0.0.1                                                                     
```

> для корректного распознавания локальных DNS-запросов

### Подготовка к созданию домена <!-- HEAD -->

#### Очистка баз и конфигурации Samba <!-- NAME -->

```CODE
rm -f /etc/samba/smb.conf
rm -rf /var/lib/samba                                                                       
rm -rf /var/cache/samba                                                                     
mkdir -p /var/lib/samba/sysvol                                                              
```

> удаляет предыдущую конфигурацию домена

### Создание домена <!-- HEAD -->

#### Интерактивное создание домена <!-- NAME -->

```CODE
samba-tool domain provision
```

> указать: доменное имя, рабочую группу, роль dc, бэкенд SAMBA_INTERNAL, DNS forwarder 77.88.8.8, пароль администратора

#### Пакетное создание домена <!-- NAME -->

```CODE
samba-tool domain provision --realm=domain.sample --domain=domain --adminpass='P@ssw0rd'
--dns-backend=SAMBA_INTERNAL --option="dns forwarder=77.88.8.8" --server-role=dc            
--use-rfc2307   
```

> --realm(имя области Kerberos и DNS домена); --domain(имя рабочей группы); --dns-backend(бэкенд DNS); --use-rfc2307(поддержка UID/GID и ACL)

#### Запуск службы Samba <!-- NAME -->

```CODE
systemctl enable --now samba

```

#### Копирование конфигурации Kerberos <!-- NAME -->

```CODE
cp /var/lib/samba/private/krb5.conf /etc/krb5.conf                                       
```

> Samba создает шаблон krb5.conf при создании домена

### Проверка <!-- HEAD -->

#### Проверка статуса службы <!-- NAME -->

```CODE
systemctl status samba
```

> служба должна быть active (running)

#### Просмотр информации о домене <!-- NAME -->

```CODE
samba-tool domain info 127.0.0.1                                                         
```

> показывает общую информацию о домене

#### Просмотр общих ресурсов <!-- NAME -->

```CODE
smbclient -L localhost -U administrator                                                  
```

> должны быть netlogon и sysvol

#### Проверка DNS в /etc/resolv.conf <!-- NAME -->

```CODE
cat /etc/resolv.conf                                                                     
```

> должен быть nameserver 127.0.0.1

#### Проверка SRV-записи Kerberos <!-- NAME -->

```CODE
host -t SRV _kerberos._udp.domain.sample.                                                  
```

> утилита host из пакета bind-utils

#### Проверка SRV-записи LDAP <!-- NAME -->

```CODE
host -t SRV _ldap._tcp.domain.sample.                                                      
```

> проверяет доступность LDAP

#### Проверка A-записи хоста <!-- NAME -->

```CODE
host -t A dc.domain.sample.                                                                
```

> должен вернуть IP-адрес контроллера домена

#### Проверка Kerberos <!-- NAME -->

```CODE
kinit administrator@DOMAIN.SAMPLE                                                          
```

> имя домена в верхнем регистре; запрашивает пароль администратора
