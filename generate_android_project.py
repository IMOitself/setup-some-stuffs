#!/usr/bin/env python3
"""
generate_android_project.py

Generates a barebones Android + Kotlin project: just enough files to build
a "Hello, Android!" APK with Gradle. No AndroidX, no layouts, no themes,
no gradle wrapper, no test folders - only what's required to compile.

Usage:
    python generate_android_project.py
    python generate_android_project.py --output MyApp --package com.example.myapp --name "My App"
"""

import argparse
import os

# ---- Pinned tool versions (latest stable as of Aug 2026) ----
AGP_VERSION = "9.3.0"       # Android Gradle Plugin (built-in Kotlin support, no kotlin-android plugin needed)
GRADLE_VERSION = "9.7.0"    # Gradle
COMPILE_SDK = 37            # Android 17
TARGET_SDK = 36             # Android 16 (matches current Play Store minimum target requirement)
MIN_SDK = 24                # Android 7.0

FILES = {}  # populated by build_files()


def build_files(package: str, app_name: str) -> dict:
    pkg_path = package.replace(".", "/")

    files = {}

    files["settings.gradle.kts"] = f'''\
pluginManagement {{
    repositories {{
        google()
        mavenCentral()
        gradlePluginPortal()
    }}
}}

dependencyResolutionManagement {{
    repositories {{
        google()
        mavenCentral()
    }}
}}

rootProject.name = "{app_name}"
include(":app")
'''

    files["build.gradle.kts"] = "// Intentionally empty: no top-level plugins needed.\n"

    files["gradle.properties"] = '''\
android.useAndroidX=true
org.gradle.jvmargs=-Xmx2048m -Dfile.encoding=UTF-8
'''

    files["app/build.gradle.kts"] = f'''\
plugins {{
    id("com.android.application") version "{AGP_VERSION}"
}}

android {{
    namespace = "{package}"
    compileSdk = {COMPILE_SDK}

    defaultConfig {{
        applicationId = "{package}"
        minSdk = {MIN_SDK}
        targetSdk = {TARGET_SDK}
        versionCode = 1
        versionName = "1.0"
    }}

    compileOptions {{
        sourceCompatibility = JavaVersion.VERSION_17
        targetCompatibility = JavaVersion.VERSION_17
    }}
}}
'''

    files["app/src/main/AndroidManifest.xml"] = '''\
<?xml version="1.0" encoding="utf-8"?>
<manifest xmlns:android="http://schemas.android.com/apk/res/android">

    <application
        android:allowBackup="true"
        android:label="@string/app_name"
        android:theme="@android:style/Theme.Material.Light.DarkActionBar">

        <activity
            android:name=".MainActivity"
            android:exported="true">
            <intent-filter>
                <action android:name="android.intent.action.MAIN" />
                <category android:name="android.intent.category.LAUNCHER" />
            </intent-filter>
        </activity>

    </application>

</manifest>
'''

    files[f"app/src/main/java/{pkg_path}/MainActivity.kt"] = f'''\
package {package}

import android.app.Activity
import android.os.Bundle
import android.widget.TextView

class MainActivity : Activity() {{
    override fun onCreate(savedInstanceState: Bundle?) {{
        super.onCreate(savedInstanceState)
        setContentView(TextView(this).apply {{
            text = "Hello, Android!"
            textSize = 20f
        }})
    }}
}}
'''

    files["app/src/main/res/values/strings.xml"] = f'''\
<resources>
    <string name="app_name">{app_name}</string>
</resources>
'''

    return files


def write_project(output_dir: str, package: str, app_name: str) -> None:
    files = build_files(package, app_name)
    for rel_path, content in files.items():
        full_path = os.path.join(output_dir, rel_path)
        os.makedirs(os.path.dirname(full_path), exist_ok=True)
        with open(full_path, "w", newline="\n") as f:
            f.write(content)
        print(f"  wrote {rel_path}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate a barebones Android Kotlin project.")
    parser.add_argument("--output", default="BarebonesApp", help="Output directory (default: BarebonesApp)")
    parser.add_argument("--package", default="com.example.barebones", help="Application/package id (default: com.example.barebones)")
    parser.add_argument("--name", default="Barebones App", help="App display name (default: 'Barebones App')")
    args = parser.parse_args()

    print(f"Generating project in ./{args.output}")
    write_project(args.output, args.package, args.name)
    print("\nDone. See README.md for how to build it into an APK.")


if __name__ == "__main__":
    main()
