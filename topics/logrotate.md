
### Настройка <!-- HEAD -->

#### Содержимое файла /etc/logrotate.d/rsyslog-opt <!-- NAME -->

```CODE
/opt/*/*.log {                                                                    
weekly                                                                           
size 10M                                                                         
rotate 4                                                                         
compress                                                                         
missingok                                                                        
notifempty                                                                       
create 0640 root root                                                            
sharedscripts                                                                    
postrotate                                                                       
systemctl reload rsyslog > /dev/null 2>&1 || true                            
endscript                                                                        
}                                                                                    
```

> /opt/*/*.log (логи в поддиректориях /opt); weekly (ротация раз в неделю); size 10M (или при 10 МБ); rotate 4 (хранить 4 копии); compress (сжимать gzip); missingok (игнорировать отсутствие файлов); notifempty (не ротировать пустые); create 0640 root root (права нового файла); sharedscripts (скрипты один раз для группы); postrotate (команды после ротации)

#### Включение служб <!-- NAME -->

```CODE
systemctl enable --now rsyslog logrotate                                          

```

### Настройка клиента <!-- HEAD -->

#### В /etc/rsyslog.conf добавить <!-- NAME -->

```CODE
*.warning action(type="omfwd"                                                     
target="10.21.12.50"                                                             
port="514"                                                                       
protocol="tcp"                                                                   
action.resumeRetryCount="-1"                                                     
queue.type="linkedList"                                                          
queue.size="10000")                                                              
```

> *.warning (уровень warning и выше); target (адрес syslog-сервера); port 514 (порт отправки); protocol tcp (использовать TCP); action.resumeRetryCount=-1 (бесконечные попытки переподключения); queue.type linkedList (тип очереди); queue.size 10000 (размер очереди)

#### Включение службы на клиенте <!-- NAME -->

```CODE
systemctl enable --now rsyslog 
```
