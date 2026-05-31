
### Установка FreeIPA-сервера <!-- HEAD -->

#### Установка генератора энтропии <!-- NAME -->

```CODE
apt-get update && apt-get install -y haveged                                             
                                                                                              
 
```

#### Включение и запуск haveged <!-- NAME -->

```CODE
systemctl enable --now haveged                                                           
                                                                                              
 
```

#### Установка пакета FreeIPA <!-- NAME -->

```CODE
apt-get install -y freeipa-server                                                        
                                                                                              
 
```

#### Запуск интерактивной установки <!-- NAME -->

```CODE
ipa-server-install --setup-dns                                                           
 
```

> --setup-dns опционально, если нужна интеграция с DNS

#### Параметры установки <!-- LIST -->
- Server host name: имя узла FreeIPA-сервера
- Domain name: доменное имя
- Realm name: пространство Kerberos (обычно домен в верхнем регистре)
- Directory Manager password: пароль для LDAP-администратора (минимум 8 символов)
- IPA admin password: пароль администратора FreeIPA
- NetBIOS name: имя NetBIOS
- DNS forwarders: внешние DNS-серверы (например 8.8.8.8)
- Reverse DNS zone: обратная DNS-зона

> Имена узла, домена и realm нельзя изменить после установки

### Создание пользователей и групп <!-- HEAD -->

#### Получение билета Kerberos <!-- NAME -->

```CODE
kinit admin                                                                              
 
```

> Ввести пароль администратора FreeIPA

#### Создание 30 пользователей с паролем <!-- NAME -->

```CODE
for i in {1..30}; do                                                                     
      echo "P@ssw0rd" | ipa user-add user$i --first=User --last=$i --password;                
      ipa user-mod user$i --setattr=krbPasswordExpiration=20251225011529Z;                    
  done                                                                                        
 
```

> Устанавливает срок действия пароля до 2025 года, чтобы не требовалась смена при первом входе

#### Создание групп <!-- NAME -->

```CODE
for i in {1..3}; do
      ipa group-add group$i;                                                                  
  done                                                                                        
                                                                                              
 
```

#### Добавление пользователей в группы <!-- NAME -->

```CODE
for i in {1..10}; do                                                                     
      ipa group-add-member group1 --users=user$i;                                             
  done                                                                                        
                                                                                              
  for i in {11..20}; do                                                                       
      ipa group-add-member group2 --users=user$i;
  done                                                                                        
                  
  for i in {21..30}; do                                                                       
      ipa group-add-member group3 --users=user$i;
  done                                                                                        
                                                                                              
 
```

### Подключение клиента к FreeIPA <!-- HEAD -->

#### Установка пакетов на клиенте <!-- NAME -->

```CODE
apt-get update && apt-get install -y freeipa-client zip                                  
                                                                                              
 
```

#### Запуск настройки клиента <!-- NAME -->

```CODE
ipa-client-install --server=srv-hq.your.domain --domain=your.domain --mkhomedir          
 
```

> --mkhomedir автоматически создаёт домашние каталоги для доменных пользователей

> Скрипт автоматически найдёт настройки FreeIPA-сервера и запросит имя пользователя с правом ввода машин в домен

#### Перезагрузка клиента <!-- NAME -->

```CODE
reboot       
                                                                                              
 
```

### Установка CA-сертификата на клиенте <!-- HEAD -->

#### Копирование сертификата с сервера <!-- NAME -->

```CODE
scp /etc/ipa/ca.crt root@CLI-HQ:/etc/pki/ca-trust/source/anchors/                        
 
```

> Выполняется на FreeIPA-сервере

#### Обновление доверенных сертификатов на клиенте <!-- NAME -->

```CODE
update-ca-trust                                                                          
                                                                                              
 
```

### Проверка FreeIPA <!-- HEAD -->

#### Проверка пользователя <!-- NAME -->

```CODE
ipa user-find admin                                                                      
                                                                                              
 
```

#### Проверка HTTPS-соединения <!-- NAME -->

```CODE
curl https://srv-hq.your.domain                                                          
                                                                                              
 
```

#### Проверка запущенных служб <!-- NAME -->

```CODE
ipactl status 
```
