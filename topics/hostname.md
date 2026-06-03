
### Настройка hostname <!-- HEAD -->

#### Просмотр текущего hostname <!-- NAME -->

```CODE
hostname                                                                                 
hostnamectl

```

#### Временное изменение hostname до перезагрузки <!-- NAME -->

```CODE
hostname new-hostname
```

> Изменения не сохраняются после перезагрузки

#### Постоянное изменение hostname <!-- NAME -->

```CODE
hostnamectl set-hostname new-hostname
```

> Изменения сохраняются после перезагрузки

#### Изменение hostname с обновлением текущей сессии <!-- NAME -->

```CODE
hostnamectl set-hostname new-hostname; exec bash
```

> exec bash перезапускает оболочку без login shell

#### Изменение hostname с обновлением login shell <!-- NAME -->

```CODE
hostnamectl set-hostname new-hostname; exec bash -l                                      
```

> exec bash -l перезапускает оболочку как login shell, загружает профили пользователя

#### Изменение hostname в /etc/hostname <!-- NAME -->

```CODE
echo "new-hostname" > /etc/hostname                                                      
```

> Альтернативный способ, требует перезагрузки или применения изменений

#### Изменение hostname в /etc/hosts <!-- NAME -->

```CODE
nano /etc/hosts                                                                          
```

> Добавить или изменить строку

```CODE
127.0.0.1   localhost                                                                    
127.0.1.1   new-hostname                                                                    
192.168.1.10   new-hostname.some.domain new-hostname                                        
```

> Рекомендуется синхронизировать с /etc/hostname для корректной работы DNS

#### Применение изменений без перезагрузки <!-- NAME -->

```CODE
systemctl restart systemd-hostnamed                                                      

```

### Проверка hostname <!-- HEAD -->

#### Проверка полного имени хоста <!-- NAME -->

```CODE
hostname -f                                                                              
```

> Показывает FQDN (Fully Qualified Domain Name)

#### Проверка короткого имени <!-- NAME -->

```CODE
hostname -s                                                                              
```

> Показывает короткое имя без домена

#### Проверка всех параметров <!-- NAME -->

```CODE
hostnamectl status                                                                       
```

> Показывает Static hostname, Icon name, Chassis, Machine ID, Boot ID, Operating System, Kernel, Architecture
