
### Настройка <!-- HEAD -->

#### Изменение параметра в /etc/net/sysctl.conf <!-- NAME -->

```CODE
net.ipv4.ip_forward=1                                                                    
```

> Разрешает маршрутизацию пакетов между интерфейсами

#### Применение изменений из файла <!-- NAME -->

```CODE
sysctl -p                                                                                

```

#### Временное включение до перезагрузки <!-- NAME -->

```CODE
echo 1 > /proc/sys/net/ipv4/ip_forward                                                   

```

#### Включение через sysctl напрямую <!-- NAME -->

```CODE
sysctl -w net.ipv4.ip_forward=1                                                          
```

> Изменения через echo и sysctl -w не сохраняются после перезагрузки

#### Проверка текущего значения <!-- NAME -->

```CODE
cat /proc/sys/net/ipv4/ip_forward                                                        
sysctl net.ipv4.ip_forward                                                                  
```

> Должно вернуть 1 если включено, 0 если выключено
