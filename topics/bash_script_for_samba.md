
### Массовый импорт пользователей в Samba AD <!-- HEAD -->

#### Подготовка CSV-файла <!-- NAME -->

```CODE
First Name;Last Name;Role;Phone;OU;Street;ZIP;City;Country;Password                      
  Ivan;Ivanov;Administrator;+79990000001;IT;Lenina 1;101000;Moscow;RU;P@ssw0rd1               
  Petr;Petrov;Manager;+79990000002;Sales;Mira 10;101001;Moscow;RU;P@ssw0rd1                   
 
```

> Разделитель - точка с запятой; First Name(имя); Last Name(фамилия); Role(должность); Phone(телефон); OU(подразделение); Street(улица); ZIP(индекс); City(город); Country(страна); Password(пароль)

#### Создание скрипта импорта <!-- NAME -->

```CODE
vim import_user.sh
                                                                                              
 
```

#### Содержимое /root/import_user.sh <!-- NAME -->

```CODE
#!/bin/bash                                                                              
                                                                                              
  csv_file="$1"                                                                               
                                                                                              
  # Create OU                                                                                 
  awk -F ';' 'NR>1 {print $5}' "$csv_file" | sort | uniq | while read ou;
  do                                                                                          
      samba-tool ou add OU="$ou",DC=au-team,DC=irpo;                                          
  done                                                                                        
                                                                                              
  # Create Users                                                                              
  while IFS=";" read -r firstName lastName role phone ou street zip city country password;
  do                                                                                          
      if [ "$firstName" == "First Name" ];
      then                                                                                    
          continue
      fi                                                                                      
                  
      username=$(echo $firstName | tr '[:upper:]' '[:lower:]' | tr -d ' '),$(echo $lastName | 
  tr '[:upper:]' '[:lower:]' | tr -d ' ')
                                                                                              
      samba-tool user add "$username" P@ssw0rd1 \                                             
      --given-name="$firstName" \
      --surname="$lastName" \                                                                 
      --telephone-number="$phone" \                                                           
      --job-title="$role" \                                                                   
      --ou="OU=$ou" \                                                                         
      --userou="OU=$ou" --noexpiry                                                            
  done < "$csv_file"                                                                          
 
```

> Скрипт автоматически создаёт OU и пользователей; username формируется как ivan,ivanov; --noexpiry(пароль не истекает)

#### Выдача прав на запуск <!-- NAME -->

```CODE
chmod +x import_user.sh
                                                                                              
 
```

### Запуск импорта <!-- HEAD -->

#### Импорт пользователей из CSV <!-- NAME -->

```CODE
./import_user.sh /mnt/Users.csv                                                          
 
```

> Запускать от root или администратора домена

### Проверка <!-- HEAD -->

#### Проверка созданных OU <!-- NAME -->

```CODE
samba-tool ou list                                                                       
                                                                                              
 
```

#### Проверка объектов внутри OU <!-- NAME -->

```CODE
samba-tool ou listobjects OU=IT                                                          
 
```

> Можно проверять любые подразделения {OU=Sales, OU=IT}
