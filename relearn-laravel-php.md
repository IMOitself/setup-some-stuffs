
## install php (`Single Line Installer`) [link](https://www.php.net/downloads.php):

![](install-php.png)

- go to this file to setup composer
```
C:\Users\<your-username>\AppData\Local\Programs\PHP\current\php.ini
```
- add these to the end of that file
```
extension=curl
extension=mbstring
extension=openssl
extension=fileinfo
extension=pdo_sqlite
```


## install composer (`Composer-Setup.exe`) [link](https://getcomposer.org/download):

![](install-composer.png)

## run command
```
composer global require laravel/installer
```

## install nodejs
![](image.png)

## usage
create project:
```
laravel new my-app
php artisan migrate
```

