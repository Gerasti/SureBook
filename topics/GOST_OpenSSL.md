
### Настройка HTTPS с ГОСТ-сертификатами <!-- HEAD -->

> Создание собственного удостоверяющего центра (УЦ), выпуск ГОСТ-сертификатов для веб-ресурсов, настройка доверия

### Установка поддержки ГОСТ <!-- HEAD -->

#### Установка пакета <!-- NAME -->

```CODE
apt-get install -y openssl-gost-engine                                                   
                                                                                              
 
```

#### Включение поддержки ГОСТ <!-- NAME -->

```CODE
control openssl-gost enabled                                                             
                                                                                              
 
```

#### Подключение GOST к OpenSSL в /etc/openssl/openssl.cnf <!-- NAME -->

```CODE
openssl_conf = openssl_def                                                               
                                                                                              
  [openssl_def]                                                                               
  engines = engine_section                                                                    
                                                                                              
  [engine_section]                                                                            
  gost = gost_section                                                                         
                                                                                              
  [gost_section]  
  engine_id = gost                                                                            
  dynamic_path = /usr/lib64/openssl/engines-1.1/gost.so                                       
  default_algorithms = ALL                                                                    
 
```

> Необходимо для создания ключей по алгоритмам ГОСТ, выпуска сертификатов с ГОСТ-подписью, корректной работы Nginx с ГОСТ-криптографией

### Создание корневого сертификата УЦ <!-- HEAD -->

#### Создание закрытого ключа УЦ <!-- NAME -->

```CODE
openssl genpkey -algorithm gost2012_256 -pkeyopt paramset:A -out ca.key                  
                                                                                              
 
```

#### Создание самоподписанного сертификата УЦ <!-- NAME -->

```CODE
openssl req -x509 -new -key ca.key -days 365 -out ca.cer -engine gost -md_gost12_256     
 
```

> В Common Name указать IP сервера или имя корневого сервера; ca.key(закрытый ключ УЦ); ca.cer(корневой сертификат УЦ)

### Создание сертификатов для доменов <!-- HEAD -->

#### Создание закрытого ключа для домена <!-- NAME -->

```CODE
openssl genpkey -algorithm gost2012_256 -pkeyopt paramset:A -out web.some.domain.key     
  openssl genpkey -algorithm gost2012_256 -pkeyopt paramset:A -out docker.some.domain.key     
                                                                                              
 
```

#### Создание запроса на подпись (CSR) <!-- NAME -->

```CODE
openssl req -new -key web.some.domain.key -out web.some.domain.csr -engine gost          
  -md_gost12_256                                                                              
  openssl req -new -key docker.some.domain.key -out docker.some.domain.csr -engine gost
  -md_gost12_256                                                                              
 
```

> В Common Name указать IP или домен(ы), например *.some.domain

#### Подпись сертификатов УЦ <!-- NAME -->

```CODE
openssl x509 -req -in web.some.domain.csr -CA ca.cer -CAkey ca.key -CAcreateserial -out  
  web.some.domain.cer -days 365 -engine gost -md_gost12_256                                   
  openssl x509 -req -in docker.some.domain.csr -CA ca.cer -CAkey ca.key -CAcreateserial -out
  docker.some.domain.cer -days 365 -engine gost -md_gost12_256                                
                  
 
```

#### Проверка сертификата <!-- NAME -->

```CODE
openssl x509 -in web.some.domain.cer -text -noout
                                                                                              
 
```

### Установка сертификатов в систему <!-- HEAD -->

#### Копирование сертификатов в доверенные <!-- NAME -->

```CODE
cp ca.cer /etc/pki/ca-trust/source/anchors/                                              
  cp web.some.domain.cer /etc/pki/ca-trust/source/anchors/                                    
  cp docker.some.domain.cer /etc/pki/ca-trust/source/anchors/                                 
                                                                                              
 
```

#### Обновление доверенных сертификатов <!-- NAME -->

```CODE
update-ca-trust         
```
