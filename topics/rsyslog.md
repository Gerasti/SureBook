
### Установка <!-- HEAD -->

#### Установка пакетов на всех устройствах <!-- NAME -->

```CODE
apt-get install rsyslog logrotate                                                        
 
```

> rsyslog(сбор и пересылка логов); logrotate(ротация и сжатие логов)

> Обычно работают в связке

### Настройка сервера сбора логов <!-- HEAD -->

#### В /etc/rsyslog.conf <!-- NAME -->

```CODE
module(load="imuxsock")                                                                  
  module(load="imklog")                                                                       
  module(load="imudp")                                                                        
  input(type="imudp" port="514")                                                              
  module(load="imtcp")                                                                        
  input(type="imtcp" port="514")                                                              
                                                                                              
  $template RemoteLogs, "/opt/%HOSTNAME%/%PROGRAMNAME%.log"                                   
                  
  if ($fromhost-ip != "127.0.0.1" and $syslogseverity <= 4) then ?RemoteLogs                  
  & stop          
 
```

> imuxsock(локальные сообщения); imklog(логи ядра); imudp/imtcp(приём по UDP/TCP); $syslogseverity <= 4(warning и выше); & stop(остановка обработки)

#### Создание каталогов для логов <!-- NAME -->

```CODE
mkdir -p /opt/client1
  mkdir -p /opt/client2                                                                       
  mkdir -p /opt/client3                                                                       
 
```

> создаются каталоги для каждого клиента

#### Установка прав на каталоги <!-- NAME -->

```CODE
chown -R root:root /opt                                                                  
  chmod -R 755 /opt                                                                           
 
```

> права для записи логов службой rsyslog

#### Перезапуск службы на сервере <!-- NAME -->

```CODE
systemctl restart rsyslog                                                                
                                                                                              
 
```

### Настройка клиента <!-- HEAD -->

#### В /etc/rsyslog.conf на клиенте <!-- NAME -->

```CODE
*.warning action(type="omfwd"                                                            
      target="<HQ-SRV_IP>"                                                                    
      port="514"                                                                              
      protocol="tcp"                                                                          
      action.resumeRetryCount="-1"                                                            
      queue.type="linkedList"                                                                 
      queue.size="10000")                                                                     
 
```

> *.warning(уровень warning и выше); target(IP сервера логов); protocol(tcp для надежности); resumeRetryCount=-1(бесконечные попытки); queue.size(размер очереди сообщений)

#### Перезапуск службы на клиенте <!-- NAME -->

```CODE
systemctl restart rsyslog
                                                                                              
 
```

### Проверка <!-- HEAD -->

#### Проверка открытого порта на сервере <!-- NAME -->

```CODE
ss -tulpn | grep 514                                                                     
 
```

> должен показать порты 514 TCP и UDP

#### Проверка каталогов логов на сервере <!-- NAME -->

```CODE
ls -la /opt/                                                                             
 
```

> должны появиться каталоги с именами клиентов

#### Проверка содержимого логов <!-- NAME -->

```CODE
ls -la /opt/client1/                                                                     
 
```

> должны появиться файлы логов от клиента

#### Тестовая отправка сообщения с клиента <!-- NAME -->

```CODE
logger -p user.warning "Test message from client"                                        
 
```

> отправляет тестовое сообщение уровня warning

#### Проверка получения на сервере <!-- NAME -->

```CODE
tail -f /opt/client1/*.log                                                               
 
```

> должно появиться тестовое сообщение
