
### Настройка <!-- HEAD -->

#### Раскомментировать строки в /etc/apt/sources.list.d/yandex.list <!-- NAME -->

```CODE
rpm [alt] http://mirror.yandex.ru/altlinux Sisyphus/x86_64 classic
rpm [alt] http://mirror.yandex.ru/altlinux Sisyphus/i586 classic
rpm [alt] http://mirror.yandex.ru/altlinux Sisyphus/noarch classic
```

> alt.list желательно весь закомментировать

#### Обновление <!-- NAME -->

```CODE
apt-get update
```

> Должен работать DNS и возможно Интернет, NAT
