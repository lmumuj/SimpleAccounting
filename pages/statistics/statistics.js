const app = getApp()

Page({
  data: {
    currentPeriod: 'month',
    totalExpense: '0.00',
    totalIncome: '0.00',
    balance: '0.00',
    expenseData: [],
    incomeData: [],
    chartColors: [
      '#4A90E2', '#50E3C2', '#FFD300', '#FF5252',
      '#9B59B6', '#FF9800', '#00BCD4', '#8BC34A'
    ]
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

    // 根据时间周期筛选数据
    const filteredData = this.filterByPeriod(accountBooks)

    // 计算统计数据
    const stats = this.calculateStats(filteredData, categories)

    // 更新UI
    this.setData({
      totalExpense: stats.expense.toFixed(2),
      totalIncome: stats.income.toFixed(2),
      balance: (stats.income - stats.expense).toFixed(2),
      expenseData: stats.expenseData,
      incomeData: stats.incomeData
    })

    // 绘制图表
    setTimeout(() => {
      this.drawPieChart('expenseChart', stats.expenseData)
      this.drawPieChart('incomeChart', stats.incomeData)
    }, 100)
  },

  // 根据时间周期筛选数据
  filterByPeriod(list) {
    const now = new Date()
    const currentYear = now.getFullYear()
    const currentMonth = now.getMonth()
    const currentDay = now.getDate()
    const currentWeekDay = now.getDay()

    return list.filter(item => {
      const itemDate = new Date(item.date)

      switch (this.data.currentPeriod) {
        case 'week':
          // 本周（从周一开始）
          const weekStart = new Date(now)
          weekStart.setDate(currentDay - currentWeekDay + (currentWeekDay === 0 ? -6 : 1))
          weekStart.setHours(0, 0, 0, 0)
          return itemDate >= weekStart

        case 'month':
          return itemDate.getMonth() === currentMonth && itemDate.getFullYear() === currentYear

        case 'year':
          return itemDate.getFullYear() === currentYear

        default:
          return true
      }
    })
  },

  // 计算统计数据
  calculateStats(list, categories) {
    const expenseMap = new Map()
    const incomeMap = new Map()
    let totalExpense = 0
    let totalIncome = 0

    // 初始化分类数据
    categories.expense.forEach(cat => {
      expenseMap.set(cat.id, { ...cat, amount: 0 })
    })
    categories.income.forEach(cat => {
      incomeMap.set(cat.id, { ...cat, amount: 0 })
    })

    // 统计各类金额
    list.forEach(item => {
      if (item.type === 'expense') {
        const category = expenseMap.get(item.categoryId)
        if (category) {
          category.amount += Number(item.amount)
          totalExpense += Number(item.amount)
        }
      } else {
        const category = incomeMap.get(item.categoryId)
        if (category) {
          category.amount += Number(item.amount)
          totalIncome += Number(item.amount)
        }
      }
    })

    // 转换为数组并计算百分比
    const expenseData = Array.from(expenseMap.values())
      .filter(item => item.amount > 0)
      .map((item, index) => ({
        ...item,
        percent: ((item.amount / totalExpense) * 100).toFixed(1),
        color: this.data.chartColors[index % this.data.chartColors.length]
      }))
      .sort((a, b) => b.amount - a.amount)

    const incomeData = Array.from(incomeMap.values())
      .filter(item => item.amount > 0)
      .map((item, index) => ({
        ...item,
        percent: ((item.amount / totalIncome) * 100).toFixed(1),
        color: this.data.chartColors[index % this.data.chartColors.length]
      }))
      .sort((a, b) => b.amount - a.amount)

    return {
      expense: totalExpense,
      income: totalIncome,
      expenseData,
      incomeData
    }
  },

  // 切换时间周期
  switchPeriod(e) {
    const period = e.currentTarget.dataset.period
    this.setData({ currentPeriod: period }, () => {
      this.loadData()
    })
  },

  // 绘制饼图
  drawPieChart(canvasId, data) {
    const ctx = wx.createCanvasContext(canvasId, this)

    if (data.length === 0) {
      ctx.draw()
      return
    }

    const centerX = 100
    const centerY = 100
    const radius = 70
    let startAngle = 0

    data.forEach(item => {
      const angle = (item.percent / 100) * 2 * Math.PI

      ctx.beginPath()
      ctx.moveTo(centerX, centerY)
      ctx.arc(centerX, centerY, radius, startAngle, startAngle + angle)
      ctx.closePath()
      ctx.setFillStyle(item.color)
      ctx.fill()

      startAngle += angle
    })

    ctx.draw()
  }
})
