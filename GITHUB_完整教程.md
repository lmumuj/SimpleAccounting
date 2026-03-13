# 🚀 从零开始使用 GitHub Actions 构建 APK

## 📋 方案三完整步骤（无需安装 Android Studio）

这个方案完全在云端构建，你只需要：
1. 安装一个很小的 Git 工具
2. 在 GitHub 上创建仓库
3. 上传代码
4. 等待自动构建并下载 APK

---

## 📥 第一步：安装 Git（约 5 分钟）

### 1.1 下载 Git
- 访问：https://git-scm.com/downloads
- 点击 "Windows" 图标下载
- 文件大小约 50MB

### 1.2 安装 Git
1. 运行下载的安装程序
2. 点击 "Next" 保持默认选项
3. 在 "Adjusting your PATH environment" 步骤：
   - ✅ 选择 **"Git from the command line and also from 3rd-party software"**
4. 继续点击 "Next" 直到安装完成

### 1.3 验证安装
打开命令行（cmd 或 PowerShell），输入：
```bash
git --version
```

如果显示版本号（如 `git version 2.x.x`），说明安装成功！

---

## 🔑 第二步：注册/登录 GitHub（约 2 分钟）

### 2.1 注册账号（如果没有）
1. 访问：https://github.com
2. 点击右上角 "Sign up"
3. 填写：
   - Username（用户名）
   - Email（邮箱）
   - Password（密码）
4. 验证邮箱

### 2.2 登录
如果已有账号，直接登录即可。

---

## 📂 第三步：在 GitHub 上创建仓库（约 2 分钟）

### 3.1 创建新仓库
1. 登录 GitHub 后，点击右上角的 **"+"** 按钮
2. 选择 **"New repository"**
3. 填写仓库信息：
   - **Repository name**: `SimpleAccounting`（建议使用这个名字）
   - **Description**: 简单记账应用
   - **Public / Private**: 选择任意（Public 免费，Private 有限制）
   - ⚠️ **重要**：**不要勾选**以下选项：
     - ❌ Add a README file
     - ❌ Add .gitignore
     - ❌ Choose a license
4. 点击绿色按钮 **"Create repository"**

### 3.2 复制仓库地址
创建成功后，页面会显示仓库地址，格式为：
```
https://github.com/你的用户名/SimpleAccounting.git
```

**记住这个地址！**

---

## 📤 第四步：上传项目代码（约 3 分钟）

### 方法 A：使用自动化脚本（推荐）

#### 4.1 运行脚本

**方式1：双击运行**
```
找到文件：upload_to_github.bat
双击运行
```

**方式2：命令行运行**
```bash
cd c:\Users\Admins\Documents\记账
upload_to_github.bat
```

#### 4.2 按照提示操作

脚本会引导你完成以下步骤：

```
[1/4] 检查 Git 环境
✅ 检测到 Git 环境

[2/4] 初始化 Git 仓库
✅ Git 仓库初始化成功

[3/4] 添加文件到 Git
✅ 文件添加成功

[4/4] 创建初始提交
✅ 提交成功

[5/4] 关联 GitHub 仓库
请输入你的 GitHub 用户名: 你的用户名
请输入仓库名称（默认: SimpleAccounting）: SimpleAccounting

准备连接到：https://github.com/你的用户名/SimpleAccounting.git
```

#### 4.3 输入信息

按照提示输入：
- **GitHub 用户名**：你在 GitHub 注册时的用户名
- **仓库名称**：默认 `SimpleAccounting`，如果改了就输入新名字

#### 4.4 推送代码

脚本会自动执行：
```bash
git push -u origin main
```

**首次推送可能需要身份验证！**

**方式1：用户名 + 密码**
- 用户名：GitHub 用户名
- 密码：**不是登录密码**，需要创建 Personal Access Token

**方式2：Personal Access Token（推荐）**

创建 Token 步骤：
1. 访问：https://github.com/settings/tokens
2. 点击 **"Generate new token"** → **"Generate new token (classic)"**
3. 勾选权限：**repo**（全部勾选）
4. 设置过期时间（如 90 days）
5. 点击 **"Generate token"**
6. **复制 token（只显示一次！）**
7. 使用 token 作为密码

推送成功后，你会看到：
```
✅ 上传成功！
仓库地址：https://github.com/你的用户名/SimpleAccounting.git
```

### 方法 B：手动命令行（备选）

如果脚本运行失败，可以手动执行：

```bash
# 1. 进入项目目录
cd c:\Users\Admins\Documents\记账

# 2. 初始化 Git 仓库
git init

# 3. 添加所有文件
git add .

# 4. 创建提交
git commit -m "Initial commit: Simple Accounting App"

# 5. 关联远程仓库（替换为你的地址）
git remote add origin https://github.com/你的用户名/SimpleAccounting.git

# 6. 重命名分支为 main
git branch -M main

# 7. 推送代码（使用 token 作为密码）
git push -u origin main
```

---

## 🔨 第五步：自动构建 APK（约 5-10 分钟）

### 5.1 查看构建状态

1. 访问你的 GitHub 仓库
   ```
   https://github.com/你的用户名/SimpleAccounting
   ```

2. 点击顶部的 **"Actions"** 标签

3. 你会看到正在运行的构建任务
   - 名称：`Build Android APK`
   - 状态：🟡 黄色圆点（进行中）或 🟢 绿色对勾（完成）

### 5.2 查看构建详情

点击正在运行的任务，你会看到详细的构建步骤：

```
☑️ Checkout code
☑️ Set up JDK 17
☑️ Setup Android SDK
☑️ Grant execute permission for gradlew
🔄 Build Debug APK（正在构建）
⬜ Upload Debug APK
⬜ Build Release APK
⬜ Upload Release APK
```

### 5.3 等待构建完成

**预计时间：**
- 首次构建：8-12 分钟（需要下载依赖）
- 后续构建：3-5 分钟（使用缓存）

构建成功后，所有步骤都会变成 ✅ 绿色对勾。

---

## 📦 第六步：下载 APK

### 6.1 进入构建任务页面

1. 在仓库页面点击 **"Actions"** 标签
2. 点击最近的构建任务（绿色 ✅）
3. 滚动到页面底部

### 6.2 找到 Artifacts 部分

在构建日志下方，你会看到：

```
Artifacts

app-debug           下载    2.5 MB    2 分钟前
app-release         下载    1.8 MB    2 分钟前
```

### 6.3 下载 APK

- **app-debug**: Debug 版本（用于测试）
- **app-release**: Release 版本（未签名，体积小）

点击文件名即可下载到本地！

---

## 📱 第七步：安装 APK 到手机

### 方法 1：使用 ADB（推荐）

**前提：** 已安装 ADB 工具

1. **启用手机 USB 调试**
   - 进入手机"设置"
   - 关于手机 → 连续点击"版本号"7次
   - 返回设置 → 开发者选项
   - 启用"USB 调试"

2. **连接手机**
   - 用 USB 线连接手机和电脑
   - 手机上点击"允许 USB 调试"

3. **安装 APK**
   ```bash
   # 安装 Debug 版本
   adb install app-debug.apk

   # 如果已安装旧版本
   adb install -r app-debug.apk

   # 卸载应用
   adb uninstall com.simpleaccounting.app
   ```

### 方法 2：直接传输（最简单）

1. 将下载的 APK 文件复制到手机
   - 通过 USB
   - 通过微信/QQ等发送
   - 通过网盘/云存储

2. **在手机上安装**
   - 找到 APK 文件并点击
   - 允许"未知来源"安装（如果提示）
   - 点击"安装"

3. **打开应用**
   - 安装完成后，点击"打开"
   - 或在桌面找到"简单记账"图标

---

## 🔄 日常使用流程

### 修改代码后重新构建

```bash
# 1. 修改代码
# （使用任何编辑器修改项目文件）

# 2. 提交更改
cd c:\Users\Admins\Documents\记账
git add .
git commit -m "Fix some issues"

# 3. 推送到 GitHub（自动触发构建）
git push

# 4. 等待 5-10 分钟
# 访问 GitHub → Actions 查看构建

# 5. 下载最新 APK
# 在 Artifacts 部分下载
```

### 手动触发构建

如果不推送代码，也可以手动触发构建：

1. 访问仓库 → Actions 标签
2. 左侧选择 "Build Android APK"
3. 点击右侧的 "Run workflow" 按钮
4. 选择分支（main）
5. 点击 "Run workflow"

---

## 💡 进阶配置（可选）

### 1. 修改构建配置

编辑 `.github/workflows/build.yml` 文件：

```yaml
on:
  push:
    branches: [ main, master, develop ]  # 添加更多分支
  workflow_dispatch:                    # 手动触发
```

### 2. 添加签名配置

需要签名的 Release APK 时：

1. 生成密钥库：
   ```bash
   keytool -genkey -v -keystore release.keystore -alias release -keyalg RSA -keysize 2048 -validity 10000
   ```

2. 在 GitHub 添加 Secrets：
   - 仓库 Settings → Secrets and variables → Actions
   - New repository secret
   - 添加 `KEYSTORE_FILE`（Base64 编码）、`KEYSTORE_PASSWORD` 等

3. 修改 build.yml 添加签名步骤

### 3. 多版本测试

```yaml
strategy:
  matrix:
    api-level: [24, 26, 28, 30, 33]
```

---

## 🎯 时间总览

| 步骤 | 时间 | 累计时间 |
|------|------|---------|
| 安装 Git | 5 分钟 | 5 分钟 |
| 注册 GitHub | 2 分钟 | 7 分钟 |
| 创建仓库 | 2 分钟 | 9 分钟 |
| 上传代码 | 3 分钟 | 12 分钟 |
| 自动构建 | 5-10 分钟 | 17-22 分钟 |
| 下载 APK | 1 分钟 | 18-23 分钟 |

**总计：约 20 分钟**

---

## ❓ 常见问题

### Q1: Git push 提示认证失败？

**解决：**
- 不要使用 GitHub 登录密码
- 使用 Personal Access Token
- 创建方式：Settings → Developer settings → Personal access tokens

### Q2: 构建失败怎么办？

**检查：**
1. 代码是否正确推送
2. `.github/workflows/build.yml` 是否存在
3. Actions 页面的错误日志

### Q3: 如何快速下载最新 APK？

**方法：**
1. 访问仓库 → Actions
2. 点击最新的绿色 ✅ 构建任务
3. 滚动到底部 → Artifacts
4. 点击 APK 文件

### Q4: GitHub Actions 免费吗？

**回答：** 是的！
- 公开仓库：完全免费
- 私有仓库：每月 2000 分钟免费额度
- 构建一次约 5-10 分钟，完全够用

### Q5: 可以在手机上直接安装测试吗？

**回答：**
- Debug APK：可以，直接安装
- Release APK (unsigned)：可以安装，但不能发布到商店
- Release APK (signed)：可以发布到应用商店

---

## 📚 相关文档

项目中已准备的其他文档：

1. **GITHUB_ACTIONS_指南.md** - GitHub Actions 详细说明
2. **打包状态报告.md** - 项目状态和解决方案
3. **打包说明_README.md** - 快速打包说明
4. **BUILD_GUIDE_CN.md** - 详细构建指南

---

## 🎉 总结

### 完整流程
```
1. 安装 Git（5分钟）
   ↓
2. 注册 GitHub（2分钟）
   ↓
3. 创建仓库（2分钟）
   ↓
4. 上传代码（3分钟）
   ↓
5. 自动构建（5-10分钟）
   ↓
6. 下载 APK（1分钟）
   ↓
7. 安装到手机（1分钟）
```

### 优势
- ✅ 无需安装 Android Studio
- ✅ 无需配置 Java、Android SDK
- ✅ 完全免费
- ✅ 云端构建，不占用本地资源
- ✅ 自动化，每次推送自动构建
- ✅ 版本历史管理

### 下一步行动

**立即执行：**
1. 下载并安装 Git
2. 在 GitHub 创建仓库
3. 运行 `upload_to_github.bat` 或 `upload_to_github.py`
4. 等待构建并下载 APK

**预计完成时间：** 20 分钟

---

**文档创建时间：** 2026年3月13日
**配置文件：** `.github/workflows/build.yml`
**状态：** ✅ 已配置，等待上传到 GitHub

**开始吧！按照上面的步骤，20分钟后你就能在手机上安装自己的 APP 了！🎉**
