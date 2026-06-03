
### Установка <!-- HEAD -->

#### Установка OpenSSL <!-- NAME -->

```CODE
apt-get install openssl
```

> Обычно уже установлен в системе

### Настройка сервера CA <!-- HEAD -->

#### Создание корневой директории CA <!-- NAME -->

```CODE
mkdir /ca    

```

#### Поиск конфигурационного файла OpenSSL <!-- NAME -->

```CODE
openssl ca                                                                               
```

> Команда выдаст ошибку с путём к конфигурационному файлу (/var/lib/ssl/openssl.cnf, /etc/ssl/openssl.cnf)

#### Резервная копия конфигурационного файла <!-- NAME -->

```CODE
cp /var/lib/ssl/openssl.cnf /var/lib/ssl/openssl.cnf.backup

```

#### В /var/lib/ssl/openssl.cnf в секции [ CA_default ] <!-- NAME -->

```CODE
dir = /ca                                                                                
```

> Изменение корневой директории CA с ./demoCA на /ca

#### Создание структуры директорий CA <!-- NAME -->

```CODE
cd /ca                                                                                   
mkdir certs newcerts crl private                                                            
touch index.txt                                                                             
echo -n '00' > serial                                                                       
```

> certs(выпущенные сертификаты); newcerts(новые сертификаты); crl(списки отзыва); private(приватные ключи); index.txt(база данных сертификатов); serial(серийный номер); -n(без пробела и перевода строки)

#### В /var/lib/ssl/openssl.cnf в секции [ CA_default ] <!-- NAME -->

```CODE
policy = policy_anything
```

> Принимаем любые значения, требуем только CN (Common Name)

#### В /var/lib/ssl/openssl.cnf в секции [ policy_anything ] <!-- NAME -->

```CODE
commonName = supplied                                                                    
```

> CN обязателен для заполнения

#### В /var/lib/ssl/openssl.cnf в секции [ req_distinguished_name ] <!-- NAME -->

```CODE
countryName_default = RU                                                                 
0.organizationName_default = domain.sample                                                  
```

> Значения по умолчанию для CA: C=RU, O=domain.sample, CN указывается при генерации

#### В /var/lib/ssl/openssl.cnf в секции [ v3_ca ] <!-- NAME -->

```CODE
basicConstraints = CA:true                                                               
```

> Сертификат может быть корневым CA

#### Генерация ключей и запроса на сертификат CA <!-- NAME -->

```CODE
openssl req -nodes -new -out cacert.csr -keyout private/cakey.pem -extensions v3_ca      
```

> -nodes(без пароля на ключ); -new(новый запрос); -out(файл запроса); -keyout(приватный ключ); -extensions v3_ca(расширения CA). При заполнении: C=RU и O=domain.sample подставятся автоматически, CN указать вручную (например domain.sample RootCA), пустые поля заполнить точкой

#### Самоподписание сертификата CA <!-- NAME -->

```CODE
openssl ca -selfsign -in cacert.csr -out cacert.pem -extensions v3_ca
```

> -selfsign(самоподписание); подтвердить y на вопросы

#### Просмотр содержимого сертификата <!-- NAME -->

```CODE
openssl x509 -text -noout -in cacert.pem | less                                          
```

> Необязательно, для проверки содержимого сертификата

### Настройка клиента <!-- HEAD -->

#### Подготовка сертификата для клиента <!-- NAME -->

```CODE
mv cacert.pem cacert.crt
```

> Сертификаты должны иметь расширение .crt

#### Копирование сертификата на клиент Debian/Ubuntu <!-- NAME -->

```CODE
cp cacert.crt /usr/local/share/ca-certificates/                                          
update-ca-certificates                                                                      
```

> Для дистрибутивов на базе deb

#### Копирование сертификата на клиент ALT/RHEL/CentOS <!-- NAME -->

```CODE
cp cacert.crt /etc/pki/ca-trust/source/anchors/                                          
update-ca-trust                                                                      
```

> Для дистрибутивов на базе rpm

### Проверка <!-- HEAD -->

#### Проверка доверия к сертификату <!-- NAME -->

```CODE
openssl verify cacert.crt
```

> Должен вывести: cacert.crt: OK
