# 🚀 使用 GitHub Actions 自动构建 APK

## 📋 什么是 GitHub Actions？

GitHub Actions 是 GitHub 提供的 CI/CD（持续集成/持续部署）服务，它可以：
- ✅ 在云端自动构建你的 Android 项目
- ✅ 无需本地配置 Java、Android SDK 等环境
- ✅ 每次推送代码自动构建
- ✅ 提供下载链接，直接获取 APK 文件

**核心优势：免费、无需配置环境、自动化构建**

---

## 🔧 第一步：创建 GitHub 仓库

### 1. 注册/登录 GitHub
- 访问：https://github.com
- 如果没有账号，先注册（免费）

### 2. 创建新仓库
- 点击右上角的 "+" 按钮
- 选择 "New repository"
- 填写仓库信息：
  - **Repository name**: `SimpleAccounting`（或你喜欢的名字）
  - **Description**: 简单记账应用
  - **Public/Private**: 选择 Public（公开）或 Private（私有）
- 点击 "Create repository"

---

## 📤 第二步：上传项目到 GitHub

### 方法 A：使用 Git 命令行（推荐）

#### 2.1 安装 Git（如果未安装）
- 下载：https://git-scm.com/downloads
- 安装时选择默认选项即可

#### 2.2 初始化 Git 仓库并上传
```bash
# 1. 进入项目目录
cd c:\Users\Admins\Documents\记账

# 2. 初始化 Git 仓库
git init

# 3. 添加所有文件
git add .

# 4. 创建初始提交
git commit -m "Initial commit: Simple Accounting App"

# 5. 关联远程仓库（替换你的用户名）
git remote add origin https://github.com/你的用户名/SimpleAccounting.git

# 6. 推送代码
git branch -M main
git push -u origin main
```

**说明：**
- 将 `你的用户名` 替换为你的 GitHub 用户名
- 首次推送可能需要输入用户名和密码（或 Personal Access Token）

### 方法 B：使用 GitHub 网页界面上传

1. 打开刚创建的 GitHub 仓库页面
2. 点击 "uploading an existing file" 链接
3. 将整个项目文件夹拖拽到上传区域
4. 填写提交信息："Initial commit"
5. 点击 "Commit changes"

**注意：**这种方式只能上传文件，不能上传文件夹结构，推荐使用方法A。

---

## 🔨 第三步：触发自动构建

### 自动触发（推荐）
代码推送到 GitHub 后，GitHub Actions 会**自动开始构建**

1. 进入仓库页面
2. 点击顶部的 "Actions" 标签
3. 你会看到正在运行的构建任务
4. 等待构建完成（约 5-10 分钟）

### 手动触发
如果配置了 `workflow_dispatch`，可以手动触发构建：

1. 进入仓库页面
2. 点击 "Actions" 标签
3. 选择左侧的 "Build Android APK"
4. 点击右侧的 "Run workflow" 按钮
5. 选择分支（main 或 master）
6. 点击 "Run workflow"

---

## 📦 第四步：下载 APK

### 4.1 查看构建状态

1. 进入仓库页面
2. 点击 "Actions" 标签
3. 点击最近的构建任务（例如：Build Android APK）
4. 等待状态变为 ✅ 绿色对勾

### 4.2 下载 APK

在构建任务页面底部，找到 **Artifacts** 部分：

- **app-debug**: Debug 版本 APK（用于测试）
- **app-release**: Release 版本 APK（未签名，体积小）

点击 APK 文件名即可下载！

---

## 📱 第五步：安装 APK 到手机

### 方法 1：通过 ADB 安装

```bash
# 1. 确保手机已启用 USB 调试
# 2. 用 USB 连接手机和电脑

# 3. 安装 Debug 版本
adb install app-debug.apk

# 如果已安装旧版本，使用 -r 参数
adb install -r app-debug.apk

# 4. 卸载应用（如需）
adb uninstall com.simpleaccounting.app
```

### 方法 2：直接传输安装

1. 将下载的 APK 文件复制到手机
2. 在手机上点击 APK 文件
3. 允许"未知来源"安装
4. 点击"安装"

---

## 🎯 配置文件说明

### GitHub Actions 工作流配置文件

**位置：** `.github/workflows/build.yml`

**功能：**
- 自动检测代码推送
- 使用 JDK 17 和 Android SDK
- 构建 Debug 和 Release APK
- 上传 APK 到 GitHub Artifacts
- 保留 30 天

**关键配置：**
```yaml
on:
  push:
    branches: [ main, master ]  # 推送到这些分支时触发
  workflow_dispatch:           # 允许手动触发
```

### Git 忽略文件

**位置：** `.gitignore`

**作用：** 忽略不需要上传的文件，包括：
- APK 文件（避免仓库过大）
- 构建缓存文件
- 配置文件（本地配置）

---

## 🔄 日常使用流程

### 修改代码后重新构建

```bash
# 1. 修改代码

# 2. 提交更改
git add .
git commit -m "Fix some issues"

# 3. 推送到 GitHub（自动触发构建）
git push
```

### 查看构建进度
```bash
# GitHub Actions 会自动构建
# 在仓库的 Actions 页面查看进度
```

### 下载最新 APK
```bash
# 构建完成后，在 Artifacts 部分下载
# 每次构建都会生成新的 APK
```

---

## ⚙️ 高级配置（可选）

### 1. 添加签名配置

如果需要签名的 Release APK：

**步骤：**
1. 生成密钥库：
   ```bash
   keytool -genkey -v -keystore release.keystore -alias release -keyalg RSA -keysize 2048 -validity 10000
   ```

2. 在 GitHub 仓库中添加 Secrets：
   - 进入仓库 Settings → Secrets and variables → Actions
   - 点击 "New repository secret"
   - 添加以下 Secrets：
     - `KEYSTORE_FILE`: Base64 编码的密钥库文件
     - `KEYSTORE_PASSWORD`: 密钥库密码
     - `KEY_ALIAS`: 密钥别名
     - `KEY_PASSWORD`: 密钥密码

3. 修改 `.github/workflows/build.yml`，添加签名步骤

### 2. 自动发布到 Releases

修改工作流配置，在构建成功后自动创建 Release：

```yaml
- name: Create Release
  uses: softprops/action-gh-release@v1
  if: startsWith(github.ref, 'refs/tags/')
  with:
    files: app/build/outputs/apk/release/app-release-unsigned.apk
  env:
    GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
```

### 3. 多版本构建

添加对不同 Android 版本的测试：
```yaml
strategy:
  matrix:
    api-level: [24, 26, 28, 30, 33]
```

---

## 📊 构建历史和版本管理

### 查看构建历史
1. 进入仓库 → Actions 标签
2. 左侧显示所有构建记录
3. 点击任意构建查看详情

### 下载历史版本
- 每次构建的 APK 都会保留 30 天
- 可以随时下载任意构建的 APK
- 建议下载重要的版本保存到本地

### 版本标签
```bash
# 为重要版本打标签
git tag v1.0.0
git push origin v1.0.0

# 这样可以方便地找到特定版本的构建
```

---

## 💡 常见问题

### Q1: 构建失败怎么办？

**检查：**
1. 代码是否正确推送到 GitHub
2. `.github/workflows/build.yml` 文件是否存在
3. Actions 页面的构建日志中的错误信息

**常见错误：**
- `gradlew permission denied`: 确保添加了 `chmod +x gradlew` 步骤
- `SDK not found`: 确认使用 `android-actions/setup-android@v3`
- `Java version mismatch`: 确认使用 JDK 17

### Q2: 如何快速下载最新的 APK？

**方法：**
1. 进入仓库 → Actions 标签
2. 点击最新的绿色 ✅ 构建任务
3. 滚动到底部，找到 Artifacts
4. 点击 APK 文件下载

### Q3: 构建需要多长时间？

**预计时间：**
- 首次构建：8-12 分钟（需要下载依赖）
- 后续构建：3-5 分钟（使用缓存）

### Q4: 如何查看详细的构建日志？

**方法：**
1. 点击构建任务
2. 点击具体的步骤（如 "Build Debug APK"）
3. 展开后可以看到完整的日志输出

### Q5: 可以免费使用吗？

**回答：** 是的！
- GitHub Actions 对公开仓库完全免费
- 私有仓库有每月 2000 分钟的免费额度
- 构建一次约 5-10 分钟，完全够用

### Q6: APK 可以直接发布到应用商店吗？

**回答：**
- **Debug APK**: 不能，用于测试
- **Release APK (unsigned)**: 不能，需要签名
- **Release APK (signed)**: 可以，需要额外配置签名

---

## 🎉 总结

### 完整流程
```
1. 创建 GitHub 仓库
   ↓
2. 上传项目代码
   ↓
3. 自动触发构建（或手动触发）
   ↓
4. 等待 5-10 分钟
   ↓
5. 下载 APK
   ↓
6. 安装到手机测试
```

### 优势
- ✅ 无需本地配置环境
- ✅ 完全免费
- ✅ 自动化构建
- ✅ 版本历史管理
- ✅ 方便协作

### 注意事项
- ⚠️ 确保网络连接正常
- ⚠️ 首次推送可能需要 Personal Access Token
- ⚠️ Debug APK 不能发布到应用商店
- ⚠️ 私有仓库有免费额度限制

---

## 📞 需要帮助？

**文档资源：**
- GitHub Actions 官方文档：https://docs.github.com/actions
- Git 使用教程：https://git-scm.com/docs

**快速参考：**
- 构建状态：仓库 → Actions
- 下载 APK：构建任务页面 → Artifacts
- 查看日志：点击构建步骤

---

**文档创建时间：** 2026年3月13日
**配置文件：** `.github/workflows/build.yml`
**状态：** ✅ 已配置，等待上传到 GitHub

**下一步：创建 GitHub 仓库并上传代码！**
