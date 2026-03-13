# 简单记账 - Android原生应用

一款界面简洁、操作便捷的记账Android原生应用，采用最新的Jetpack Compose技术栈开发。

## ✨ 功能特点

- 📝 **快速记账**：简洁的记账界面，一键添加收支记录
- 📊 **数据统计**：支持周、月、年多维度统计分析
- 🎨 **界面美观**：简约明朗的设计风格，Material Design 3
- 💾 **本地存储**：使用Room数据库，数据安全可靠
- 📤 **数据导出**：支持导出CSV格式数据
- 🗑️ **数据管理**：支持编辑和删除记录
- 🎯 **现代技术**：Kotlin + Jetpack Compose + Room

## 🏗️ 技术栈

- **语言**：Kotlin
- **UI框架**：Jetpack Compose (Material 3)
- **架构**：MVVM
- **数据库**：Room
- **依赖注入**：ViewModel + StateFlow
- **异步处理**：Kotlin Coroutines
- **最低版本**：Android 7.0 (API 24)
- **目标版本**：Android 14 (API 34)

## 📁 项目结构

```
记账/
├── app/
│   ├── src/
│   │   └── main/
│   │       ├── java/com/simpleaccounting/app/
│   │       │   ├── data/              # 数据层
│   │       │   │   ├── Transaction.kt      # 账目实体
│   │       │   │   ├── Category.kt         # 类别定义
│   │       │   │   ├── TransactionDao.kt   # 数据访问对象
│   │       │   │   ├── AppDatabase.kt      # Room数据库
│   │       │   │   └── TransactionRepository.kt
│   │       │   ├── ui/                # UI层
│   │       │   │   ├── MainActivity.kt    # 主Activity
│   │       │   │   ├── MainViewModel.kt    # 主ViewModel
│   │       │   │   ├── HomeScreen.kt       # 首页
│   │       │   │   ├── AddEditScreen.kt    # 添加/编辑页面
│   │       │   │   ├── StatisticsScreen.kt # 统计页面
│   │       │   │   └── MineScreen.kt       # 我的页面
│   │       │   └── ...                  # 其他配置
│   │       ├── res/                    # 资源文件
│   │       │   ├── values/
│   │       │   │   ├── strings.xml
│   │       │   │   └── themes.xml
│   │       │   ├── mipmap/             # 应用图标
│   │       │   └── xml/                # 配置文件
│   │       └── AndroidManifest.xml
│   └── build.gradle.kts                # 应用级构建配置
├── build.gradle.kts                    # 项目级构建配置
├── settings.gradle.kts                 # Gradle设置
├── gradle.properties                   # Gradle属性
└── README_ANDROID.md                   # 项目说明文档
```

## 🚀 快速开始

### 环境要求

- **Android Studio**：最新稳定版（推荐 Hedgehog或更高）
- **JDK**：17或更高版本
- **Android SDK**：API 24 或更高
- **Gradle**：8.2

### 安装步骤

#### 1. 克隆项目

```bash
git clone <repository-url>
cd 记账
```

#### 2. 打开项目

1. 启动 Android Studio
2. 选择 "File" -> "Open"
3. 选择项目根目录（记账文件夹）
4. 等待 Gradle 同步完成

#### 3. 配置签名（可选）

如需发布正式版本，需要配置签名：

1. 在 `app/build.gradle.kts` 中配置签名信息
2. 或使用 Build -> Generate Signed Bundle/APK

#### 4. 运行应用

1. 连接Android设备或启动模拟器
2. 点击工具栏的 "Run" 按钮（绿色三角形）
3. 或使用命令行：

```bash
./gradlew installDebug
```

## 📖 使用说明

### 首页 - 账目

- 查看本月收支总览
- 筛选全部/支出/收入记录
- 点击账目可查看详情或编辑
- 点击右下角"+"按钮添加新记录

### 添加/编辑页面

- 切换支出/收入类型
- 输入金额（支持小数点后两位）
- 选择类别（使用Emoji图标）
- 添加备注
- 选择日期
- 保存或删除记录

### 统计页面

- 切换本周/本月/本年统计
- 查看收支总览和结余
- 查看各类别详细统计
- 可视化进度条展示占比

### 我的页面

- 查看记账统计（笔数、天数、类别）
- 导出数据（CSV格式到剪贴板）
- 清空所有数据（需确认）
- 查看使用提示

## 📊 数据结构

### 账目记录（Transaction）

```kotlin
@Entity(tableName = "transactions")
data class Transaction(
    @PrimaryKey(autoGenerate = true)
    val id: Long = 0,
    val type: TransactionType,      // EXPENSE | INCOME
    val amount: Double,             // 金额
    val categoryId: Long,           // 类别ID
    val remark: String,             // 备注
    val date: Long,                 // 日期（时间戳）
    val createTime: Long            // 创建时间（时间戳）
)
```

### 类别配置（Category）

**支出类别（8种）：**
- 🍔 餐饮
- 🚗 交通
- 🛒 购物
- 🎮 娱乐
- 💊 医疗
- 📚 教育
- 🏠 居住
- 📦 其他

**收入类别（5种）：**
- 💰 工资
- 🎁 奖金
- 📈 投资
- 💼 兼职
- 📦 其他

## 🎨 设计规范

### 配色方案
- **主色调**：#4A90E2（蓝色）
- **辅助色**：#357ABD（深蓝）
- **支出色**：#FF5252（红色）
- **收入色**：#52C41A（绿色）
- **背景色**：#F5F5F5（浅灰）

### 组件规范
- 使用 Material Design 3 组件
- 卡片圆角：12-16dp
- 按钮圆角：12dp
- 间距：8/16/24dp

## 🔧 构建和发布

### Debug版本

```bash
./gradlew assembleDebug
```

### Release版本

```bash
./gradlew assembleRelease
```

生成的APK位于：
- Debug: `app/build/outputs/apk/debug/app-debug.apk`
- Release: `app/build/outputs/apk/release/app-release.apk`

### 生成签名APK

1. Build -> Generate Signed Bundle/APK
2. 选择 APK
3. 创建或选择密钥库
4. 选择 release 构建类型
5. 完成签名

## ⚙️ 自定义配置

### 修改类别

编辑 `data/Category.kt` 文件：

```kotlin
object CategoryDefaults {
    val expenseCategories = listOf(
        Category(1L, "餐饮", "🍔", TransactionType.EXPENSE),
        // 添加或修改支出类别
    )

    val incomeCategories = listOf(
        Category(101L, "工资", "💰", TransactionType.INCOME),
        // 添加或修改收入类别
    )
}
```

### 修改主题颜色

编辑 `ui/` 文件夹中的各个 Screen 文件，修改颜色代码：

```kotlin
Color(0xFF4A90E2)  // 修改为您的颜色
```

## ⚠️ 注意事项

1. **数据备份**：数据保存在本地，建议定期使用"导出数据"功能备份
2. **版本兼容**：最低支持 Android 7.0 (API 24)
3. **存储权限**：Android 10以下需要存储权限（已配置）
4. **数据同步**：当前版本不支持跨设备同步

## 🐛 常见问题

### Q: 构建失败？
A: 检查以下几点：
1. JDK版本是否为17或更高
2. Android SDK是否已安装
3. Gradle是否成功同步

### Q: 应用崩溃？
A: 查看Logcat日志，检查数据库初始化和权限配置

### Q: 如何导出数据？
A: 进入"我的"页面，点击"导出数据"，数据会复制到剪贴板

### Q: 数据会丢失吗？
A: 数据保存在本地，不会丢失。但卸载应用后数据会删除

## 🚀 后续优化

### 功能扩展
- [ ] 支持自定义类别
- [ ] 添加预算管理
- [ ] 支持多账本
- [ ] 添加搜索功能
- [ ] 支持照片附件
- [ ] 添加定时提醒
- [ ] 数据云端同步

### 性能优化
- [ ] 添加数据缓存
- [ ] 优化数据库查询
- [ ] 添加骨架屏加载

### 用户体验
- [ ] 暗黑模式
- [ ] 手势操作
- [ ] 语音输入
- [ ] 快捷金额按钮

## 📄 许可证

本项目仅供学习交流使用，未经授权不得用于商业用途。

## 🤝 贡献

欢迎提交Issue和Pull Request！

## 📞 联系方式

如有问题或建议，欢迎反馈。

---

**版本**：1.0.0
**更新日期**：2024
**开发语言**：Kotlin
**UI框架**：Jetpack Compose
