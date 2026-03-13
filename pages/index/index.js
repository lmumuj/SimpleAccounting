const app = getApp()

Page({
  data: {
    currentTab: 'all', // all, expense, income
    accountList: [],
    monthExpense: '0.00',
    monthIncome: '0.00'
  },

  onLoad() {
    this.loadData()
  },

  onShow() {
    this.loadData()
  },

  // 加载数据
  loadData() {
    const accountBooks = wx.getStorageSync('accountBooks') || []
    const categories = wx.getStorageSync('categories') || { expense: [], income: [] }

    // 处理账目数据
    const processedList = accountBooks.map(item => {
      const categoryList = item.type === 'expense' ? categories.expense : categories.income
      const category = categoryList.find(c => c.id === item.categoryId) || { name: '其他', icon: '📦' }

      const date = new Date(item.date)
      const dateStr = `${date.getMonth() + 1}月${date.getDate()}日`
      const timeStr = `${date.getHours().toString().padStart(2, '0')}:${date.getMinutes().toString().padStart(2, '0')}`

      return {
        ...item,
        categoryName: category.name,
        categoryIcon: category.icon,
        date: dateStr,
        time: timeStr
      }
    })

    // 按日期倒序排序
    processedList.sort((a, b) => new Date(b.date) - new Date(a.date))

    // 计算本月收支
    this.calculateMonthStats(accountBooks)

    // 根据当前tab筛选
    this.setData({
      accountList: this.filterByTab(processedList)
    })
  },

  // 根据tab筛选数据
  filterByTab(list) {
    if (this.data.currentTab === 'all') return list
    return list.filter(item => item.type === this.data.currentTab)
  },

  // 计算本月收支
  calculateMonthStats(list) {
    const now = new Date()
    const currentMonth = now.getMonth()
    const currentYear = now.getFullYear()

    let expense = 0
    let income = 0

    list.forEach(item => {
      const itemDate = new Date(item.date)
      if (itemDate.getMonth() === currentMonth && itemDate.getFullYear() === currentYear) {
        if (item.type === 'expense') {
          expense += Number(item.amount)
        } else {
          income += Number(item.amount)
        }
      }
    })

    this.setData({
      monthExpense: expense.toFixed(2),
      monthIncome: income.toFixed(2)
    })
  },

  // 切换tab
  switchTab(e) {
    const tab = e.currentTarget.dataset.tab
    this.setData({ currentTab: tab }, () => {
      this.loadData()
    })
  },

  // 查看详情
  viewDetail(e) {
    const id = e.currentTarget.dataset.id
    wx.navigateTo({
      url: `/pages/add/add?id=${id}`
    })
  },

  // 跳转到添加页面
  goToAdd() {
    wx.navigateTo({
      url: '/pages/add/add'
    })
  }
})
