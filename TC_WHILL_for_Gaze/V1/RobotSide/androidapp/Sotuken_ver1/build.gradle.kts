// Top-level build file where you can add configuration options common to all sub-projects/modules.
buildscript {
    repositories {
        google()  // or maven { url "https://maven.google.com" } for Gradle <= 3
        mavenCentral()
        maven { url = uri("https://jitpack.io") }
    }
    dependencies {
        classpath("com.google.android.gms:oss-licenses-plugin:0.10.6")
        classpath ("com.android.tools.build:gradle:7.0.4")
    }
}

plugins {
    id("com.android.application") version "8.1.1" apply false
    id("org.jetbrains.kotlin.android") version "1.9.0" apply false
    id("com.android.library") version "7.3.1" apply false
}


