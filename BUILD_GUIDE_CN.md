# Android应用打包指南

## 环境要求

### 必需工具
1. **JDK 17 或更高版本** - 当前系统检测到 Java 8，需要升级
2. **Android SDK** - Android开发工具包
3. **Android Studio** - 官方IDE（推荐）

### 环境检查
```bash
# 检查Java版本（需要17+）
java -version

# 检查Android SDK（需要配置环境变量）
adb version
```

## 打包方法

### 方法一：使用Android Studio（推荐）

#### 步骤：
1. **打开项目**
   ```
   File -> Open -> 选择项目目录：c:\Users\Admins\Documents\记账
   ```

2. **等待Gradle同步**
   - 打开项目后，Android Studio会自动开始Gradle同步
   - 等待同步完成（右下角显示进度）

3. **配置签名（Release版本需要）**
   
   **3.1 生成密钥库**
   ```bash
   keytool -genkey -v -keystore simple-accounting.keystore -alias simple_accounting -keyalg RSA -keysize 2048 -validity 10000
   ```
   
   **3.2 配置签名信息**
   
   在 `app/build.gradle.kts` 中添加：
   ```kotlin
   android {
       signingConfigs {
           create("release") {
               storeFile = file("simple-accounting.keystore")
               storePassword = "你的密码"
               keyAlias = "simple_accounting"
               keyPassword = "你的密码"
           }
       }
       
       buildTypes {
           release {
               signingConfig = signingConfigs.getByName("release")
               isMinifyEnabled = true
               proguardFiles(
                   getDefaultProguardFile("proguard-android-optimize.txt"),
                   "proguard-rules.pro"
               )
           }
       }
   }
   ```

4. **构建APK**

   **4.1 Debug版本（测试用）**
   ```
   Build -> Build Bundle(s) / APK(s) -> Build APK(s)
   ```
   
   **4.2 Release版本（发布用）**
   ```
   Build -> Generate Signed Bundle / APK
   -> 选择 APK
   -> 创建或选择密钥库
   -> 选择 release 构建类型
   ```

5. **获取APK文件**
   
   构建完成后，点击通知栏中的 "locate" 链接，或手动找到：
   - **Debug版本**: `app/build/outputs/apk/debug/app-debug.apk`
   - **Release版本**: `app/build/outputs/apk/release/app-release.apk`

### 方法二：使用命令行（需要完整环境）

#### 前提条件：
- JDK 17+ 已安装并配置环境变量
- Android SDK 已安装并配置
- Gradle已安装或项目包含gradle wrapper

#### 命令：
```bash
# 进入项目目录
cd c:\Users\Admins\Documents\记账

# 构建Debug版本
.\gradlew.bat assembleDebug

# 构建Release版本（需要配置签名）
.\gradlew.bat assembleRelease

# 或者使用绝对路径
gradle assembleDebug
```

### 方法三：使用命令行构建工具（仅限已配置环境）

```bash
# 设置ANDROID_HOME环境变量（如果未设置）
set ANDROID_HOME=C:\Users\[你的用户名]\AppData\Local\Android\Sdk

# 进入项目目录
cd c:\Users\Admins\Documents\记账

# 构建APK
.\gradlew.bat assembleDebug
```

## 当前问题诊断

### 已检测到的环境问题：
1. ❌ **Java版本过低**：当前Java 8，项目需要Java 17+
2. ❌ **Gradle Wrapper不完整**：缺少 `gradle-wrapper.jar` 文件
3. ❌ **未检测到Android SDK**：环境变量可能未配置

### 解决方案：

#### 方案A：安装Android Studio（最简单）
1. 下载并安装 [Android Studio](https://developer.android.com/studio)
2. 安装时会自动安装所需的所有工具（JDK 17, Android SDK, Gradle）
3. 用Android Studio打开项目即可直接打包

#### 方案B：手动配置环境
1. **安装JDK 17+**
   - 下载 [OpenJDK 17](https://adoptium.net/) 或 [Oracle JDK 17](https://www.oracle.com/java/technologies/downloads/#java17)
   - 安装并配置JAVA_HOME环境变量

2. **安装Android SDK**
   - 下载 [Android SDK Command-line Tools](https://developer.android.com/studio#command-tools)
   - 或通过Android Studio安装SDK

3. **修复Gradle Wrapper**
   ```bash
   # 重新生成gradle wrapper
   gradle wrapper --gradle-version 8.2
   ```

4. **构建项目**
   ```bash
   cd c:\Users\Admins\Documents\记账
   .\gradlew.bat assembleDebug
   ```

## APK文件说明

### Debug版本
- **用途**：开发测试
- **特点**：
  - 未签名（使用debug签名）
  - 体积较大（包含调试信息）
  - 未混淆代码
  - 可直接安装，但不能发布到应用商店

### Release版本
- **用途**：正式发布
- **特点**：
  - 需要正式签名
  - 体积较小（经过优化）
  - 代码已混淆（提高安全性）
  - 可发布到应用商店

## 打包后测试

### 安装测试
```bash
# 使用ADB安装（需要USB调试开启）
adb install app-debug.apk

# 卸载
adb uninstall com.simpleaccounting.app
```

### 功能测试清单
- [ ] 应用能正常启动
- [ ] 首页账目列表显示正常
- [ ] 添加账目功能正常
- [ ] 编辑账目功能正常
- [ ] 删除账目功能正常
- [ ] 统计页面显示正常
- [ ] 数据导出功能正常
- [ ] 数据清空功能正常
- [ ] 界面在不同屏幕尺寸下显示正常

## 发布到应用商店

### Google Play Store
1. 创建开发者账号（$25一次性费用）
2. 创建应用列表
3. 上传签名后的Release APK
4. 填写应用信息
5. 提交审核

### 国内应用商店
- 腾讯应用宝
- 小米应用商店
- 华为应用市场
- OPPO软件商店
- vivo应用商店

### 注意事项
- 每个应用商店有各自的审核标准
- 需要准备应用图标、截图、描述等素材
- 可能需要提供隐私政策

## 故障排除

### Gradle同步失败
```
解决方案：
1. 检查网络连接
2. 清理缓存：File -> Invalidate Caches / Restart
3. 删除.gradle文件夹后重新同步
```

### 构建失败 - Java版本错误
```
解决方案：
1. 检查JAVA_HOME环境变量
2. 确认JDK版本为17或更高
3. 在File -> Project Structure中设置JDK路径
```

### 构建失败 - SDK版本问题
```
解决方案：
1. 打开SDK Manager安装所需SDK版本
2. 在File -> Project Structure中设置SDK路径
```

### APK无法安装
```
可能原因：
1. 签名冲突
2. 版本号未更新
3. 安装空间不足
4. 设备版本过低（需要Android 7.0+）
```

## 快速参考

### 常用Gradle命令
```bash
# 清理构建
.\gradlew.bat clean

# 构建Debug APK
.\gradlew.bat assembleDebug

# 构建Release APK
.\gradlew.bat assembleRelease

# 构建并安装到设备
.\gradlew.bat installDebug

# 查看依赖树
.\gradlew.bat :app:dependencies

# 查看任务列表
.\gradlew.bat tasks
```

### 项目信息
- **包名**: com.simpleaccounting.app
- **最低版本**: Android 7.0 (API 24)
- **目标版本**: Android 14 (API 34)
- **版本号**: 1.0.0 (versionCode: 1)

---

**推荐操作**：使用Android Studio打开项目，这是最简单可靠的方法！

**文档生成时间**: 2026年3月13日
