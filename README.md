# 简单记账 - 微信小程序

一款界面简洁、操作便捷的记账小程序，适用于安卓和iOS平台。

## ✨ 功能特点

- 📝 **快速记账**：简洁的记账界面，一键添加收支记录
- 📊 **数据统计**：支持周、月、年多维度统计分析
- 🎨 **界面美观**：简约明朗的设计风格，清新舒适
- 📈 **图表展示**：直观的饼图展示收支分类占比
- 💾 **本地存储**：数据保存在本地，保护隐私
- 📤 **数据导出**：支持导出CSV格式数据
- 🗑️ **数据管理**：支持编辑和删除记录

## 🏗️ 项目结构

```
记账/
├── app.js                 # 小程序逻辑
├── app.json              # 小程序配置
├── app.wxss              # 全局样式
├── sitemap.json          # 站点地图配置
├── project.config.json   # 项目配置
├── project.private.config.json  # 项目私有配置
├── pages/                # 页面目录
│   ├── index/            # 首页（账目列表）
│   │   ├── index.wxml
│   │   ├── index.js
│   │   ├── index.wxss
│   │   └── index.json
│   ├── add/              # 添加/编辑页面
│   │   ├── add.wxml
│   │   ├── add.js
│   │   ├── add.wxss
│   │   └── add.json
│   ├── statistics/       # 统计页面
│   │   ├── statistics.wxml
│   │   ├── statistics.js
│   │   ├── statistics.wxss
│   │   └── statistics.json
│   └── mine/             # 我的页面
│       ├── mine.wxml
│       ├── mine.js
│       ├── mine.wxss
│       └── mine.json
└── images/               # 图片资源
    ├── tab-home.png
    ├── tab-home-active.png
    ├── tab-stats.png
    ├── tab-stats-active.png
    ├── tab-mine.png
    └── tab-mine-active.png
```

## 🚀 快速开始

### 环境要求

- 微信开发者工具
- 微信开发者账号（用于测试和发布）

### 安装步骤

1. **下载项目**

   克隆或下载本项目到本地

2. **安装微信开发者工具**

   访问 [微信开发者工具官网](https://developers.weixin.qq.com/miniprogram/dev/devtools/download.html) 下载并安装

3. **导入项目**

   - 打开微信开发者工具
   - 选择"导入项目"
   - 选择项目目录（记账文件夹）
   - 填写项目名称和AppID（可以使用测试号）

4. **准备图标资源**

   项目需要准备以下图标文件（81x81像素）：
   - `images/tab-home.png` - 首页标签图标
   - `images/tab-home-active.png` - 首页选中图标
   - `images/tab-stats.png` - 统计标签图标
   - `images/tab-stats-active.png` - 统计选中图标
   - `images/tab-mine.png` - 我的标签图标
   - `images/tab-mine-active.png` - 我的选中图标

   可以使用[图标库](https://www.iconfont.cn/)或自行设计

5. **运行项目**

   点击"编译"按钮即可在模拟器中预览

## 📖 使用说明

### 首页 - 账目

- 查看本月收支总览
- 筛选全部/支出/收入记录
- 点击账目可查看详情或编辑
- 点击右下角"+"按钮添加新记录

### 添加/编辑页面

- 切换支出/收入类型
- 输入金额
- 选择类别（餐饮、交通、购物等）
- 添加备注
- 选择日期
- 保存或删除记录

### 统计页面

- 切换本周/本月/本年统计
- 查看收支总览和结余
- 饼图展示分类占比
- 详细的分类统计数据

### 我的页面

- 查看记账统计（笔数、天数、类别）
- 导出数据（CSV格式）
- 清空所有数据
- 查看使用提示

## 🎨 技术栈

- **前端框架**：微信小程序原生框架
- **样式**：WXSS（类似CSS）
- **数据存储**：微信本地存储API
- **图表**：Canvas绘制饼图

## 📝 数据结构

### 账目记录（accountBooks）

```javascript
{
  id: Number,              // 记录ID
  type: String,            // 'expense' 或 'income'
  amount: Number,          // 金额
  categoryId: Number,      // 类别ID
  remark: String,          // 备注
  date: String,            // 日期 'YYYY-MM-DD'
  createTime: String       // 创建时间 ISO格式
}
```

### 类别配置（categories）

```javascript
{
  expense: [               // 支出类别
    { id: 1, name: '餐饮', icon: '🍔' },
    { id: 2, name: '交通', icon: '🚗' },
    // ...
  ],
  income: [                // 收入类别
    { id: 101, name: '工资', icon: '💰' },
    { id: 102, name: '奖金', icon: '🎁' },
    // ...
  ]
}
```

## 🔧 自定义配置

### 修改类别

编辑 `app.js` 中的 `initData()` 方法：

```javascript
const categories = {
  expense: [
    { id: 1, name: '餐饮', icon: '🍔' },
    // 添加或修改支出类别
  ],
  income: [
    { id: 101, name: '工资', icon: '💰' },
    // 添加或修改收入类别
  ]
}
```

### 修改主题色

编辑 `app.wxss` 和各页面的 `.wxss` 文件，替换 `#4A90E2` 为您喜欢的颜色。

## ⚠️ 注意事项

1. **数据备份**：数据保存在本地，建议定期使用"导出数据"功能备份
2. **隐私保护**：所有数据仅存储在本地设备，不会上传到服务器
3. **跨设备同步**：当前版本不支持跨设备同步
4. **图标资源**：需要自行准备tabBar图标才能正常显示底部导航

## 📄 许可证

本项目仅供学习交流使用，未经授权不得用于商业用途。

## 🤝 贡献

欢迎提交Issue和Pull Request！

## 📮 联系方式

如有问题或建议，欢迎反馈。

---

**版本**：1.0.0
**更新日期**：2024
