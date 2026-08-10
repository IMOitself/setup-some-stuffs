<div align=center><h1>setup anything :D</h1></div>

<details>
<summary><h1>setup laravel</h1></summary>

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
![](install-nodejs.png)

## usage
create project:
```
laravel new my-app
php artisan migrate
```

</details>

<details>
<summary><h1>setup adb</h1></summary>

```
winget install Google.PlatformTools
```

</details>

<details>
<summary><h1>deploy react in github</h1></summary>

on your react project:
```
npm install gh-pages --save-dev
```
at the top level of `package.json`:
```json
"homepage": "https://your-github-username.github.io/your-repo-name",
```
on the scripts section of `package.json`:
```json
"scripts": {
  // ... ur existing scripts
  "predeploy": "npm run build",
  "deploy": "gh-pages -d dist",
  // "deploy": "gh-pages -d build", // use this instead if ur not using vite
}
```
(skip this if ur not using vite) add this on `defineConfig()` function in `vite.config.js`:
```js
// ... code above
export default defineConfig({
  // ...
  base: '/your-repo-name/',
  // ...
})
```
deploy the app:
```
npm run deploy
```

</details>

<details>

<summary><h1>deploy react to firebase</h1></summary>

```
npm install -g firebase-tools
```
```
firebase login
```
```
npm run build
```
1. go to [Google Cloud Console](https://console.cloud.google.com/).
2. ensure ur signed in with the exact same Google account u used for `firebase login`.
click "get started by blah blah"
<img width="1829" height="910" alt="image" src="https://github.com/user-attachments/assets/74afad29-19ba-4903-9669-10d57fad2b43" />
enter project name and proceed until its been created
<img width="1901" height="902" alt="image" src="https://github.com/user-attachments/assets/09ea2705-e3c4-4367-923a-a2eec0d3b4cf" />

<br><br>
do the stuffs above first before the code below<br>*i see u, u copy and paster >:D*
```
firebase init hosting
```
when it asks:
- select existing project
- set public directory to `dist` (or `build` if ur not using vite)
- configure as a single-page app: yes
- set up automatic builds with GitHub: no (unless u want that)
```
firebase deploy --only hosting
```
</details>
