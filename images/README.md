# 图标资源说明

此目录需要放置小程序底部导航栏的图标文件。

## 需要的图标文件

请准备以下6个图标文件（尺寸：81x81像素）：

### TabBar图标

1. **tab-home.png** - 首页未选中状态
   - 建议使用灰色系（如 #999999）
   - 图标样式：账本或列表图标

2. **tab-home-active.png** - 首页选中状态
   - 使用主题色（如 #4A90E2）
   - 图标样式：账本或列表图标（高亮）

3. **tab-stats.png** - 统计未选中状态
   - 建议使用灰色系（如 #999999）
   - 图标样式：饼图或柱状图

4. **tab-stats-active.png** - 统计选中状态
   - 使用主题色（如 #4A90E2）
   - 图标样式：饼图或柱状图（高亮）

5. **tab-mine.png** - 我的未选中状态
   - 建议使用灰色系（如 #999999）
   - 图标样式：用户图标

6. **tab-mine-active.png** - 我的选中状态
   - 使用主题色（如 #4A90E2）
   - 图标样式：用户图标（高亮）

## 图标资源推荐

### 在线图标库

- [iconfont图标库](https://www.iconfont.cn/) - 阿里巴巴矢量图标库
- [IconPark图标库](https://iconpark.oceanengine.com/) - 字节跳动图标库
- [Flaticon](https://www.flaticon.com/) - 国外免费图标库

### 设计工具

- [Figma](https://www.figma.com/) - 在线设计工具
- [Sketch](https://www.sketch.com/) - 设计软件
- [Adobe XD](https://www.adobe.com/products/xd.html) - 设计软件

## 快速获取图标

### 方案一：使用iconfont

1. 访问 iconfont.cn
2. 搜索需要的图标（账本、图表、用户）
3. 选择图标，调整颜色
4. 下载PNG格式，尺寸设置为81x81

### 方案二：使用Emoji作为临时方案

如果暂时没有图标，可以修改 `app.json` 中的 tabBar 配置，暂时不使用图标：

```json
{
  "tabBar": {
    "color": "#999999",
    "selectedColor": "#4A90E2",
    "backgroundColor": "#FFFFFF",
    "borderStyle": "black",
    "list": [
      {
        "pagePath": "pages/index/index",
        "text": "账目"
      },
      {
        "pagePath": "pages/statistics/statistics",
        "text": "统计"
      },
      {
        "pagePath": "pages/mine/mine",
        "text": "我的"
      }
    ]
  }
}
```

## 图标设计规范

- **尺寸**：81x81像素
- **格式**：PNG（支持透明背景）
- **颜色**：
  - 未选中：#999999（灰色）
  - 选中：#4A90E2（蓝色）
- **风格**：简约、扁平化
- **线条**：清晰，适合小尺寸显示

## 注意事项

- 确保图标文件名与 `app.json` 中配置的名称完全一致
- 图标文件必须是PNG格式
- 建议使用矢量图标以保证在小尺寸下的清晰度
