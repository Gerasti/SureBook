
### Передача сертификатов на удаленный сервер <!-- HEAD -->

#### Передача через rsync <!-- NAME -->

```CODE
rsync -avz ./ca.crt ./router.crt ./router.key USERNAME@IP_RTR:/etc/nginx/ssl/WEB.com/    
```

> -a(архивный режим); -v(подробный вывод); -z(сжатие при передаче)

#### Передача через scp <!-- NAME -->

```CODE
scp -P 2222 ca.crt router.crt router.key USERNAME@IP_RTR:/etc/nginx/ssl/WEB.com/         
```

> -P(указание порта SSH)

#### Передача через sftp <!-- NAME -->

```CODE
sftp USERNAME@IP_RTR                                                                     
put ca.crt /etc/nginx/ssl/WEB.com/                                                          
put router.crt /etc/nginx/ssl/WEB.com/                                                      
put router.key /etc/nginx/ssl/WEB.com/                                                      
exit                                                                                        
```

> Интерактивная передача файлов

### Установка сертификатов в систему <!-- HEAD -->

#### Переход в каталог <!-- NAME -->

```CODE
cd /etc/nginx/ssl/WEB.com/                                                               

```

#### Копирование в доверенные сертификаты <!-- NAME -->

```CODE
cp ./* /etc/pki/ca-trust/source/anchors/                                                 

```

#### Обновление доверенных сертификатов <!-- NAME -->

```CODE
update-ca-trust 
```
