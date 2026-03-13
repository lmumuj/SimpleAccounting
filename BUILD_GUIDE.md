# Android应用构建和部署指南

## 📋 前置条件

### 必需软件

1. **Android Studio**：最新稳定版（Hedgehog 2023.1.1 或更高）
   - 下载地址：https://developer.android.com/studio

2. **JDK**：17 或更高版本
   - Android Studio 通常会自带 JDK 17
   - 或使用 Oracle JDK：https://www.oracle.com/java/technologies/downloads/

3. **Android SDK**
   - API Level 24 (Android 7.0) 或更高
   - API Level 34 (Android 14) - 推荐
   - 在 Android Studio 的 SDK Manager 中安装

4. **Gradle**：8.2（项目已配置）

### 环境变量（可选但推荐）

```bash
# Windows
set JAVA_HOME=C:\Program Files\Android\Android Studio\jbr
set ANDROID_HOME=C:\Users\YourUsername\AppData\Local\Android\Sdk

# macOS/Linux
export JAVA_HOME=/Applications/Android\ Studio.app/Contents/jbr/Contents/Home
export ANDROID_HOME=$HOME/Library/Android/sdk
```

## 🚀 构建步骤

### 1. 克隆项目

```bash
git clone <repository-url>
cd 记账
```

### 2. 打开项目

1. 启动 Android Studio
2. 选择 `File` → `Open`
3. 浏览并选择项目根目录（`记账` 文件夹）
4. 点击 `OK`

### 3. 等待 Gradle 同步

- 首次打开项目时，Android Studio 会自动下载依赖
- 等待底部状态栏显示 "Gradle sync finished"
- 如果同步失败，尝试：
  - `File` → `Sync Project with Gradle Files`
  - 或点击工具栏的 "Sync Project with Gradle Files" 图标（大象图标）

### 4. 运行应用

#### 方式一：使用 Android Studio

1. 连接 Android 设备（需开启 USB 调试）或启动模拟器
2. 在工具栏中选择设备
3. 点击 `Run` 按钮（绿色三角形）或按 `Shift + F10`

#### 方式二：使用命令行

```bash
# 构建 Debug APK
./gradlew assembleDebug

# 安装到连接的设备
./gradlew installDebug

# Windows 用户使用
gradlew.bat assembleDebug
gradlew.bat installDebug
```

## 📱 构建变体

### Debug 版本

- 用于开发和测试
- 未签名，未混淆
- 包含调试信息

```bash
./gradlew assembleDebug
```

生成位置：`app/build/outputs/apk/debug/app-debug.apk`

### Release 版本

- 用于正式发布
- 已签名，已混淆
- 优化性能

```bash
./gradlew assembleRelease
```

生成位置：`app/build/outputs/apk/release/app-release-unsigned.apk`

## 🔐 签名配置

### 创建签名密钥库

```bash
keytool -genkey -v -keystore simple-accounting.keystore -alias simple-accounting -keyalg RSA -keysize 2048 -validity 10000
```

按照提示输入：
- 密码（记住这个密码）
- 姓名、组织等信息
- 密钥密码（可以使用相同的密码）

### 配置签名

在 `app/build.gradle.kts` 中添加：

```kotlin
android {
    ...

    signingConfigs {
        create("release") {
            storeFile = file("../simple-accounting.keystore")
            storePassword = "your_store_password"
            keyAlias = "simple-accounting"
            keyPassword = "your_key_password"
        }
    }

    buildTypes {
        release {
            isMinifyEnabled = true
            proguardFiles(
                getDefaultProguardFile("proguard-android-optimize.txt"),
                "proguard-rules.pro"
            )
            signingConfig = signingConfigs.getByName("release")
        }
    }
}
```

**安全提示**：不要将密钥库文件提交到版本控制系统！

### 生成签名 APK

#### 方式一：使用 Android Studio

1. `Build` → `Generate Signed Bundle/APK`
2. 选择 `APK`
3. 点击 `Create new...` 或选择现有密钥库
4. 选择 `release` 构建类型
5. 点击 `Finish`

#### 方式二：使用命令行

```bash
./gradlew assembleRelease
```

生成的已签名 APK：`app/build/outputs/apk/release/app-release.apk`

## 📦 发布到应用商店

### 准备发布

#### 1. 测试应用

- 在多种设备上测试
- 测试所有功能
- 检查 UI 适配

#### 2. 生成签名 APK 或 AAB

- APK：用于直接安装
- AAB：用于 Google Play Store

```bash
# 生成 AAB（推荐用于 Google Play）
./gradlew bundleRelease
```

生成位置：`app/build/outputs/bundle/release/app-release.aab`

#### 3. 准备应用素材

- **应用图标**：512x512 像素 PNG
- **功能图**：1024x500 像素
- **屏幕截图**：至少 2 张，最多 8 张
- **宣传文本**：短描述（80字符）和完整描述（4000字符）

#### 4. 填写应用信息

- 应用名称：简单记账
- 包名：com.simpleaccounting.app
- 类别：工具
- 内容分级：所有人
- 隐私政策 URL

### 发布到 Google Play

1. 访问 [Google Play Console](https://play.google.com/console)
2. 创建新应用
3. 填写应用信息
4. 上传 AAB 文件
5. 添加应用素材
6. 填写商店信息
7. 设置定价和分发范围
8. 提交审核

### 发布到其他平台

#### 国内应用商店

- 华为应用市场：https://developer.huawei.com/consumer/cn/
- 小米应用商店：https://dev.mi.com/
- OPPO 软件商店：https://open.oppomobile.com/
- vivo 应用商店：https://dev.vivo.com.cn/
- 应用宝：https://open.tencent.com/

#### 第三方分发平台

- 蒲公英：https://www.pgyer.com/
- fir.im：https://fir.im/

## 🔧 构建问题排查

### Gradle 同步失败

```bash
# 清理项目
./gradlew clean

# 删除 .gradle 文件夹
rm -rf .gradle

# 重新同步
File -> Sync Project with Gradle Files
```

### 依赖下载失败

1. 检查网络连接
2. 配置国内镜像（可选）：

在 `build.gradle.kts` 中添加：

```kotlin
repositories {
    maven { url = uri("https://maven.aliyun.com/repository/public") }
    maven { url = uri("https://maven.aliyun.com/repository/google") }
    maven { url = uri("https://jitpack.io") }
    google()
    mavenCentral()
}
```

### 编译错误

- 检查 JDK 版本（需要 17+）
- 检查 SDK 版本（需要 API 24+）
- 清理并重新构建：
  ```bash
  ./gradlew clean build
  ```

### 运行时崩溃

- 查看 Logcat 日志
- 检查权限配置
- 验证数据库初始化

## 📊 性能优化

### 代码混淆

Release 版本自动启用混淆，确保 `proguard-rules.pro` 配置正确。

### APK 大小优化

```kotlin
android {
    buildTypes {
        release {
            isMinifyEnabled = true
            isShrinkResources = true
        }
    }
}
```

### 启用 R8 完整模式

```kotlin
android {
    buildTypes {
        release {
            isMinifyEnabled = true
            proguardFiles(
                getDefaultProguardFile("proguard-android-optimize.txt"),
                "proguard-rules.pro"
            )
        }
    }
}
```

## 🔍 测试

### 单元测试

```bash
./gradlew test
```

### 仪器测试

```bash
./gradlew connectedAndroidTest
```

### UI 测试

```bash
./gradlew connectedDebugAndroidTest
```

## 📝 版本管理

### 更新版本号

在 `app/build.gradle.kts` 中修改：

```kotlin
defaultConfig {
    versionCode = 2  // 递增整数
    versionName = "1.1.0"  // 版本名称
}
```

### 生成变更日志

记录每个版本的更新内容，用于应用商店发布。

## 🎯 最佳实践

1. **代码审查**：提交前进行代码审查
2. **自动化测试**：编写单元测试和 UI 测试
3. **持续集成**：使用 GitHub Actions 或 CI/CD
4. **版本控制**：合理使用 Git 分支
5. **文档更新**：及时更新文档

## 🆘 获取帮助

- Android Studio 文档：https://developer.android.com/studio
- Gradle 文档：https://docs.gradle.org/
- Jetpack Compose 文档：https://developer.android.com/jetpack/compose

---

**构建工具版本**：Android Studio Hedgehog 2023.1.1
**最低支持版本**：Android 7.0 (API 24)
**目标版本**：Android 14 (API 34)
