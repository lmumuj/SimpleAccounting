const app = getApp()

Page({
  data: {
    totalRecords: 0,
    totalDays: 0,
    totalCategories: 0
  },

  onLoad() {
    this.loadStats()
  },

  onShow() {
    this.loadStats()
  },

  // 加载统计数据
  loadStats() {
    const accountBooks = wx.getStorageSync('accountBooks') || []
    const categories = wx.getStorageSync('categories') || { expense: [], income: [] }

    // 记账笔数
    const totalRecords = accountBooks.length

    // 记账天数（去重）
    const uniqueDates = new Set(accountBooks.map(item => item.date.split(' ')[0]))
    const totalDays = uniqueDates.size

    // 使用的类别数量
    const usedCategories = new Set(accountBooks.map(item => item.categoryId))
    const totalCategories = usedCategories.size

    this.setData({
      totalRecords,
      totalDays,
      totalCategories
    })
  },

  // 导出数据
  exportData() {
    const accountBooks = wx.getStorageSync('accountBooks') || []
    const categories = wx.getStorageSync('categories') || { expense: [], income: [] }

    if (accountBooks.length === 0) {
      wx.showToast({
        title: '暂无数据可导出',
        icon: 'none'
      })
      return
    }

    // 生成导出数据
    const exportData = accountBooks.map(item => {
      const categoryList = item.type === 'expense' ? categories.expense : categories.income
      const category = categoryList.find(c => c.id === item.categoryId) || { name: '其他' }
      const typeText = item.type === 'expense' ? '支出' : '收入'

      return `${item.date},${typeText},${category.name},${item.amount},${item.remark || ''}`
    })

    const csvContent = '日期,类型,类别,金额,备注\n' + exportData.join('\n')

    // 复制到剪贴板
    wx.setClipboardData({
      data: csvContent,
      success: () => {
        wx.showModal({
          title: '数据已复制',
          content: 'CSV数据已复制到剪贴板，请粘贴到文本文件中保存',
          showCancel: false
        })
      }
    })
  },

  // 清空数据
  clearData() {
    wx.showModal({
      title: '确认清空',
      content: '确定要清空所有记账数据吗？此操作不可恢复！',
      confirmColor: '#FF5252',
      success: (res) => {
        if (res.confirm) {
          wx.removeStorageSync('accountBooks')

          wx.showToast({
            title: '清空成功',
            icon: 'success'
          })

          setTimeout(() => {
            this.loadStats()
          }, 1500)
        }
      }
    })
  },

  // 关于我们
  showAbout() {
    wx.showModal({
      title: '关于简单记账',
      content: '简单记账是一款轻量级的个人记账工具，界面简洁，操作便捷，帮助您轻松管理个人财务。\n\n版本：1.0.0\n\n如果您有任何建议或问题，欢迎反馈！',
      showCancel: false,
      confirmText: '知道了'
    })
  }
})
