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
<summary><h1>setup tailwind on react</h1></summary>

if ur using vite:

```bash
npm install tailwindcss @tailwindcss/vite
```

`vite.config.js`
```js
import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import tailwindcss from '@tailwindcss/vite'

export default defineConfig({
  plugins: [react(), tailwindcss()],
})
```

`src/index.css`:
```css
@import "tailwindcss";
```

</details>

<details>
<summary><h1>setup routes on react</h1></summary>

```bash
npm install react-router-dom
```

wrap your app with `<BrowserRouter>`
`main.jsx` (or `index.jsx`)
```jsx
import { StrictMode } from "react";
import { createRoot } from "react-dom/client";
import { BrowserRouter } from "react-router-dom";
import App from "./App";

createRoot(document.getElementById("root")).render(
  <StrictMode>
    <BrowserRouter>
      <App />
    </BrowserRouter>
  </StrictMode>
);
```

`App.jsx`
```jsx
import { Routes, Route } from "react-router-dom";
import Home from "./pages/Home";
import About from "./pages/About";

function App() {
  return (
    <Routes>
      <Route path="/" element={<Home />} />
      <Route path="/about" element={<About />} />
    </Routes>
  );
}

export default App;
```

navigate between them ex:
```jsx
import { Link } from "react-router-dom";

function Home() {
  return (
    <div>
      <h1>Home</h1>
      <Link to="/about"><button>Go to About</button></Link>
    </div>
  );
}
```

</details>

<details>
<summary><h1>setup roles on react + laravel</h1></summary>

## backend
```
php artisan make:migration add_role_to_users_table --table=users
```

```php
// database/migrations/xxxx_add_role_to_users_table.php
<?php

use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

return new class extends Migration
{
    public function up(): void
    {
        Schema::table('users', function (Blueprint $table) {
            // add this
            $table->string('role')->default('guest'); // admin, guest
        });
    }

    public function down(): void
    {
        Schema::table('users', function (Blueprint $table) {
            // add this
            $table->dropColumn('role');
        });
    }
};
```
```php
// app/Models/User.php

#[Fillable(['name', 'email', 'password', 'role'])]  // add role

// add these (u know where)
public function isAdmin(): bool
{
    return $this->role === 'admin';
}
public function hasRole(string $role): bool
{
    return $this->role === $role;
}
```
```
php artisan make:controller AuthController
```
```php
<?php

namespace App\Http\Controllers;

use Illuminate\Http\Request;
use Illuminate\Support\Facades\Auth;

class AuthController extends Controller
{
    public function login(Request $request)
    {
        $credentials = $request->validate([
            'email' => 'required|email',
            'password' => 'required',
        ]);

        if (!Auth::attempt($credentials)) {
            return response()->json(['message' => 'Invalid credentials'], 401);
        }

        $token = $request->user()->createToken('auth-token')->plainTextToken;

        return response()->json([
            'token' => $token,
            'user'  => $request->user()->only('id', 'name', 'email', 'role'),
        ]);
    }

    public function user(Request $request)
    {
        return response()->json($request->user()->only('id', 'name', 'email', 'role'));
    }

    public function logout(Request $request)
    {
        $request->user()->currentAccessToken()->delete();
        return response()->json(['message' => 'Logged out']);
    }
}
```
```
php artisan make:middleware RoleMiddleware
```
```php
// app/Http/Middleware/RoleMiddleware.php
<?php

namespace App\Http\Middleware;

use Closure;
use Illuminate\Http\Request;
use Symfony\Component\HttpFoundation\Response;

class RoleMiddleware
{
    public function handle(Request $request, Closure $next, string ...$roles): Response
    {
        if (!$request->user() || !in_array($request->user()->role, $roles)) {
            return response()->json(['message' => 'Forbidden'], 403);
        }
        return $next($request);
    }
}
```
```php
// bootstrap/app.php
//...
->withMiddleware(function ($middleware) {
    // add this
    $middleware->alias([
        'role' => \App\Http\Middleware\RoleMiddleware::class,
    ]);
})
//...
```
```php
// routes/api.php
//...
// add these
use App\Http\Controllers\AuthController;

Route::post('/login', [AuthController::class, 'login']);

Route::middleware('auth:sanctum')->group(function () {
    Route::post('/logout', [AuthController::class, 'logout']);
    Route::get('/user', [AuthController::class, 'user']);
    // TODO: add routes here that the not logged in users should not see

    Route::middleware('role:admin')->group(function () {
        // TODO: Add admin routes here
    });
});
```

## frontend
```jsx
// src/contexts/AuthContext.jsx
import { createContext, useContext, useState, useEffect } from 'react';
import axios from 'axios';

const AuthContext = createContext(null);

export default function AuthProvider({ children }) {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const token = localStorage.getItem('token');
    if (token) {
      axios.get('/api/user', {
        headers: { Authorization: `Bearer ${token}` },
      })
        .then(res => setUser(res.data))
        .catch(() => localStorage.removeItem('token'))
        .finally(() => setLoading(false));
    } else {
      setLoading(false);
    }
  }, []);

  const login = async (email, password) => {
    const res = await axios.post('/api/login', { email, password });
    localStorage.setItem('token', res.data.token);
    setUser(res.data.user);
  };

  const logout = async () => {
    const token = localStorage.getItem('token');
    await axios.post('/api/logout', {}, {
      headers: { Authorization: `Bearer ${token}` },
    });
    localStorage.removeItem('token');
    setUser(null);
  };

  const hasRole = (role) => user?.role === role;

  return (
    <AuthContext.Provider value={{ user, loading, login, logout, hasRole }}>
      {children}
    </AuthContext.Provider>
  );
}

export const useAuth = () => useContext(AuthContext);
```
```jsx
// src/main.jsx
...
import AuthProvider from './contexts/AuthContext.jsx'

createRoot(document.getElementById('root')).render(
  <StrictMode>
    <BrowserRouter>
      // wrap it with AuthProvider
      <AuthProvider>
        <App />
      </AuthProvider>
    </BrowserRouter>
  </StrictMode>,
)
```
- example usage
```jsx
// src/App.jsx
//...
import { Routes, Route } from "react-router-dom";
import ProtectedRoute from './components/ProtectedRoute';

function App() {
  return (
    <Routes>
      <Route path="/example" element={
        <ProtectedRoute>
          <ForLoggedInUsersPageIdk/>
        </ProtectedRoute>
      }/>
      
      {/* TODO: add login and register */}
      {/* <Route path="/login" element={<Login/>}/> */}
      {/* <Route path="/register" element={<Register/>}/> */}
    </Routes>
  )
}

export default App
```



</details>

<details>
<summary><h1>deploy react to github</h1></summary>

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

<details>
<summary><h1>generate android kotlin project</h1></summary>

super minimal, barebones kind of project

download [generate_android_project.py](https://github.com/IMOitself/setup-some-stuffs/blob/main/generate_android_project.py)

```bash
python generate_android_project.py --output MyApp --package com.example.myapp --name "My App"
```

u know what to edit in the command obviously.


</details>

<details>
<summary><h1>build android kotlin project</h1></summary>

install all tools without having to install a single program on ur computer

`cd` into the project folder, then run:

- run these 2 code snippets **ONCE**
```powershell
curl.exe -L -o gradle-9.7.0-bin.zip https://services.gradle.org/distributions/gradle-9.7.0-bin.zip
curl.exe -L -o jdk-21.0.12+8.zip https://github.com/adoptium/temurin21-binaries/releases/download/jdk-21.0.12%2B8/OpenJDK21U-jdk_x64_windows_hotspot_21.0.12_8.zip
curl.exe -L -o commandlinetools-win.zip https://dl.google.com/android/repository/commandlinetools-win-15859902_latest.zip

mkdir temp_build\gradle
mkdir temp_build\jdk
mkdir temp_build\android-sdk

tar -xf gradle-9.7.0-bin.zip -C temp_build\gradle
tar -xf jdk-21.0.12+8.zip -C temp_build\jdk
tar -xf commandlinetools-win.zip -C temp_build\android-sdk
```

```powershell
mkdir temp_build\android-sdk\cmdline-tools\latest
move temp_build\android-sdk\cmdline-tools\bin temp_build\android-sdk\cmdline-tools\latest\bin
move temp_build\android-sdk\cmdline-tools\lib temp_build\android-sdk\cmdline-tools\latest\lib
move temp_build\android-sdk\cmdline-tools\NOTICE.txt temp_build\android-sdk\cmdline-tools\latest\NOTICE.txt
move temp_build\android-sdk\cmdline-tools\source.properties temp_build\android-sdk\cmdline-tools\latest\source.properties
```

- run these 2 code snippets **whenever** ur gonna build the app
```powershell
$env:JAVA_HOME="$PWD\temp_build\jdk\jdk-21.0.12+8"
$env:ANDROID_HOME="$PWD\temp_build\android-sdk"

1..20 | ForEach-Object { "y" } | & "$PWD\temp_build\android-sdk\cmdline-tools\latest\bin\sdkmanager.bat" --licenses
& "$PWD\temp_build\android-sdk\cmdline-tools\latest\bin\sdkmanager.bat" "platform-tools" "platforms;android-37.0"
```
```powershell
& "$PWD\temp_build\gradle\gradle-9.7.0\bin\gradle.bat" assembleRelease
```

Use `assembleDebug` instead of `assembleRelease` for a debug build. Note that
`$env:JAVA_HOME` / `$env:ANDROID_HOME` only last for the current terminal
session — set them again (the two lines above) if you open a new terminal.

The built APK will be located at:
```
app\build\outputs\apk\release\app-release-unsigned.apk
app\build\outputs\apk\debug\app-debug.apk
```

## signing:
do this once:
```
keytool -genkeypair -v -keystore imo-tvbrowser-key.jks -keyalg RSA -keysize 2048 -validity 10000 -alias imo-tvbrowser-key
```
do this after u compiled the apk:
```powershell
.\temp_build\android-sdk\build-tools\36.0.0\apksigner.bat sign --ks <anything-idk>.jks --ks-key-alias <anything-idk> --out app-release-signed.apk ".\app\build\outputs\apk\release\app-release-unsigned.apk"
```

**WAIT**, change the `<anything-idk>` to whatever u want obviously

</details>
