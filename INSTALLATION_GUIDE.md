# 简单记账小程序 - 快速安装指南

## 📦 安装前准备

### 必需工具
- **微信开发者工具**（最新版本）
  - 下载地址：https://developers.weixin.qq.com/miniprogram/dev/devtools/download.html

- **微信开发者账号**（用于测试）
  - 注册地址：https://mp.weixin.qq.com/
  - 可使用测试号进行开发

### 图标资源（必需）

在运行项目前，需要准备底部导航栏图标。将以下6个PNG图标文件放入 `images/` 目录：

| 文件名 | 尺寸 | 说明 |
|--------|------|------|
| tab-home.png | 81x81 | 首页图标（未选中，灰色） |
| tab-home-active.png | 81x81 | 首页图标（选中，蓝色） |
| tab-stats.png | 81x81 | 统计图标（未选中，灰色） |
| tab-stats-active.png | 81x81 | 统计图标（选中，蓝色） |
| tab-mine.png | 81x81 | 我的图标（未选中，灰色） |
| tab-mine-active.png | 81x81 | 我的图标（选中，蓝色） |

**获取图标方式：**
1. 访问 [iconfont图标库](https://www.iconfont.cn/)
2. 搜索"账本"、"图表"、"用户"
3. 下载PNG格式，尺寸设置为81x81
4. 分别调整颜色为灰色(#999999)和蓝色(#4A90E2)

**临时方案：**
如果暂时没有图标，可以修改 `app.json` 文件，删除 `tabBar` 配置中的 `iconPath` 和 `selectedIconPath` 字段，将只显示文字标签。

## 🚀 详细安装步骤

### 第一步：下载项目

```bash
# 如果使用Git
git clone <repository-url>
cd 记账

# 或直接下载压缩包并解压到本地目录
```

### 第二步：安装微信开发者工具

1. 访问 [微信开发者工具下载页面](https://developers.weixin.qq.com/miniprogram/dev/devtools/download.html)
2. 根据操作系统选择对应版本（Windows/Mac/Linux）
3. 下载并安装

### 第三步：准备图标资源

1. 在 `images/` 目录中放置6个图标文件
2. 确保文件名与 `app.json` 中配置的名称完全一致
3. 图标尺寸为81x81像素，格式为PNG

**图标资源下载提示：**
- 可以使用在线设计工具如 [Canva](https://www.canva.com/)
- 推荐使用扁平化、简洁的图标风格
- 建议使用矢量图标以保证清晰度

### 第四步：打开项目

1. 启动微信开发者工具
2. 使用微信扫码登录
3. 选择"导入项目"
4. 在弹出的对话框中：
   - 选择项目目录：指向 `记账` 文件夹
   - 项目名称：填写"简单记账"（或自定义）
   - AppID：填写您的AppID，或选择"测试号"
5. 点击"导入"按钮

### 第五步：配置项目（可选）

#### 修改AppID
1. 打开 `project.config.json` 文件
2. 将 `appid` 字段修改为您的AppID

```json
{
  "appid": "wxXXXXXXXXXXXXXXX"
}
```

#### 自定义类别（可选）
1. 打开 `app.js` 文件
2. 找到 `initData()` 方法
3. 修改 `categories` 对象中的类别配置

```javascript
const categories = {
  expense: [
    { id: 1, name: '餐饮', icon: '🍔' },
    { id: 2, name: '交通', icon: '🚗' },
    { id: 3, name: '购物', icon: '🛒' },
    { id: 4, name: '娱乐', icon: '🎮' },
    { id: 5, name: '医疗', icon: '💊' },
    { id: 6, name: '教育', icon: '📚' },
    { id: 7, name: '居住', icon: '🏠' },
    { id: 8, name: '其他', icon: '📦' }
  ],
  income: [
    { id: 101, name: '工资', icon: '💰' },
    { id: 102, name: '奖金', icon: '🎁' },
    { id: 103, name: '投资', icon: '📈' },
    { id: 104, name: '兼职', icon: '💼' },
    { id: 105, name: '其他', icon: '📦' }
  ]
}
```

#### 修改主题颜色（可选）
1. 打开 `app.wxss` 文件
2. 全局替换 `#4A90E2` 为您喜欢的颜色
3. 同时修改各页面 `.wxss` 文件中的对应颜色

### 第六步：编译运行

1. 点击顶部工具栏的"编译"按钮
2. 项目将在模拟器中运行
3. 可以在左侧模拟器中预览和测试

## 📱 测试功能

### 基础功能测试

#### 1. 添加账目
- 点击首页右下角"+"按钮
- 输入金额
- 选择类别
- 添加备注
- 点击保存

#### 2. 查看账目
- 在首页查看账目列表
- 点击账目查看详情
- 筛选支出/收入

#### 3. 编辑账目
- 点击任意账目
- 修改金额或类别
- 点击保存更新

#### 4. 删除账目
- 点击任意账目进入编辑
- 点击"删除"按钮
- 确认删除

#### 5. 查看统计
- 切换到"统计"标签
- 切换时间周期（周/月/年）
- 查看饼图和分类统计

#### 6. 数据管理
- 切换到"我的"标签
- 查看统计信息
- 导出数据
- 清空数据

### 真机调试

1. 在开发者工具中，点击"预览"按钮
2. 使用微信扫描二维码
3. 在手机上打开小程序
4. 进行真机测试

## ⚠️ 常见问题

### Q: 图标显示不出来？
A: 检查以下几点：
1. 图标文件是否已放置在 `images/` 目录
2. 图标文件名是否与 `app.json` 中配置的名称一致
3. 图标格式是否为PNG
4. 图标尺寸是否为81x81像素

### Q: 编译报错？
A: 检查以下几点：
1. 确保使用最新版本的微信开发者工具
2. 检查AppID是否正确配置
3. 清除缓存重新编译

### Q: 数据丢失？
A:
1. 数据存储在本地，不会丢失
2. 但更换设备后数据不会同步
3. 建议定期使用"导出数据"功能备份

### Q: 如何导出数据？
A:
1. 进入"我的"页面
2. 点击"导出数据"
3. 数据会以CSV格式复制到剪贴板
4. 粘贴到文本文件中保存

### Q: 如何发布小程序？
A:
1. 在微信公众平台注册小程序
2. 获取正式AppID
3. 配置服务器信息（如需要）
4. 在开发者工具中上传代码
5. 提交审核
6. 审核通过后发布

## 📚 进阶配置

### 启用ES6转ES5
在 `project.config.json` 中确保以下配置：
```json
{
  "setting": {
    "es6": true
  }
}
```

### 启用代码压缩
```json
{
  "setting": {
    "minified": true
  }
}
```

### 配置上传代码自动忽略
```json
{
  "packOptions": {
    "ignore": [
      {
        "type": "file",
        "value": ".eslintrc.js"
      }
    ]
  }
}
```

## 🎯 下一步

安装完成后，您可以：
1. 自定义界面样式
2. 添加更多功能
3. 测试各种场景
4. 准备发布上线

## 📖 参考文档

- [微信小程序官方文档](https://developers.weixin.qq.com/miniprogram/dev/framework/)
- [微信开发者工具使用指南](https://developers.weixin.qq.com/miniprogram/dev/devtools/download.html)
- [小程序代码规范](https://developers.weixin.qq.com/miniprogram/dev/framework/code-spec/)

---

如有其他问题，请参考项目README.md或提交Issue。
