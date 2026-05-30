
### Установка <!-- HEAD -->

#### Установка пакетов OpenSSH <!-- NAME -->

```CODE
sudo apt-get install openssh-server
 
```

> openssh-server(SSH-сервер, включает openssh-common автоматически)

#### Запуск и автозагрузка службы <!-- NAME -->

```CODE
sudo systemctl enable --now sshd                                                         
                                                                                              
 
```

### Проверка <!-- HEAD -->

#### Проверка статуса службы <!-- NAME -->

```CODE
systemctl status sshd
                                                                                              
 
```

#### Проверка прослушиваемого порта <!-- NAME -->

```CODE
ss -tulpn | grep ssh                                                                     
                                                                                              
 
```

#### Проверка конфигурации <!-- NAME -->

```CODE
sshd -t                                                                                  
 
```

> Необязательно, проверяет синтаксис /etc/openssh/sshd_config перед перезапуском

#### Просмотр активных подключений <!-- NAME -->

```CODE
who                                                                                      
 
```

> Необязательно, показывает текущие SSH-сессии

#### Просмотр логов SSH <!-- NAME -->

```CODE
journalctl -u sshd                                                                       
 
```

> Необязательно, для диагностики проблем подключения

### Настройка сервера <!-- HEAD -->

#### Основной конфигурационный файл <!-- NAME -->

```CODE
/etc/openssh/sshd_config
                                                                                              
 
```

#### Настройка /etc/openssh/sshd_config <!-- NAME -->

```CODE
Port 22                                                                                  
  PasswordAuthentication yes                                                                  
  PermitRootLogin no                                                                          
  AllowUsers sshuser adminuser                                                                
  MaxAuthTries 3                                                                              
  PubkeyAuthentication yes                                                                    
 
 AuthorizedKeysFile .ssh/authorized_keys                                                     
  Banner /etc/ssh/banner.txt                                                                  
 
```

> Port(обычно 22, изменение необязательно); PasswordAuthentication(yes для начальной настройки, no после настройки ключей); PermitRootLogin no(рекомендуется); AllowUsers(необязательно, белый список); MaxAuthTries(необязательно, обычно 3-6); PubkeyAuthentication yes(обычно включено по умолчанию); AuthorizedKeysFile(стандартное расположение); Banner(необязательно)

#### Создание файла баннера /etc/ssh/banner.txt <!-- NAME -->

```CODE
************************************
  - Authorized Access Only          *                                                         
  - All activity is monitored        *                                                        
  ---
 
```

> Необязательно, содержимое баннера произвольное

#### Перезапуск службы после изменений <!-- NAME -->

```CODE
sudo systemctl restart sshd                                                              
                                                                                              
 
```

### Настройка аутентификации по ключам <!-- HEAD -->

#### Генерация SSH-ключа на клиенте <!-- NAME -->

```CODE
ssh-keygen -t ed25519 -f ~/.ssh/srv_ssh_key
 
```

> -t ed25519(современный стандарт, быстрее и безопаснее RSA); -f(имя файла, по умолчанию id_ed25519)

#### Копирование публичного ключа на сервер <!-- NAME -->

```CODE
ssh-copy-id -i ~/.ssh/srv_ssh_key.pub sshuser@192.168.11.67
 
```

> Публичный ключ добавляется в ~/.ssh/authorized_keys на сервере

### Настройка клиента <!-- HEAD -->

#### Настройка ~/.ssh/config для упрощения подключения <!-- NAME -->

```CODE
Host srv-hq  
      HostName 192.168.11.67                                                                  
      User sshuser                                                                            
      IdentityFile ~/.ssh/srv_ssh_key
      Port 22                                                                                 
 
```

> Необязательно, упрощает подключение. Port(указывать только если не 22)

#### Установка прав на config <!-- NAME -->

```CODE
chmod 600 ~/.ssh/config                                                                  
                                                                                              
 
```

#### Подключение к серверу по псевдониму <!-- NAME -->

```CODE
ssh srv-hq                                                                               
 
```

> Работает только при настроенном ~/.ssh/config

#### Подключение к серверу напрямую <!-- NAME -->

```CODE
ssh -i ~/.ssh/srv_ssh_key sshuser@192.168.11.67                                          
 
```

> Стандартный способ подключения с указанием ключа, для нестандартного порта использовать -p {8022]

#### Подключение по паролю <!-- NAME -->

```CODE
ssh sshuser@192.168.11.67                                                                
 
```

> Работает если PasswordAuthentication yes на сервере

### Создание пользователя <!-- HEAD -->

#### Создание пользователя <!-- NAME -->

```CODE
useradd -u 2026 -m -g users -G wheel sshuser
 
```

> -u(UID, необязательно); -m(создать домашний каталог); -g(основная группа, обычно users); -G wheel(для sudo)

#### Установка пароля <!-- NAME -->

```CODE
passwd sshuser
                                                                                              
 
```

#### Настройка sudo без пароля <!-- NAME -->

```CODE
visudo                                                                                   
 
```

> Добавить: %wheel ALL=(ALL:ALL) NOPASSWD: ALL. Необязательно, обычно sudo требует пароль

#### Проверка sudo <!-- NAME -->

```CODE
sudo whoami                                                                              
 
```

> Результат: root
