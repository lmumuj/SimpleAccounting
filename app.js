App({
  onLaunch() {
    // 展示本地存储能力
    const logs = wx.getStorageSync('logs') || []
    logs.unshift(Date.now())
    wx.setStorageSync('logs', logs)

    // 初始化账目数据
    this.initData()
  },

  // 初始化账目数据
  initData() {
    const accountBooks = wx.getStorageSync('accountBooks')
    if (!accountBooks) {
      wx.setStorageSync('accountBooks', [])
    }

    // 设置默认类别
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

    wx.setStorageSync('categories', categories)
  },

  globalData: {
    userInfo: null
  }
})
