const app = getApp()

Page({
  data: {
    formData: {
      type: 'expense',
      amount: '',
      categoryId: 1,
      remark: '',
      date: ''
    },
    editId: null,
    isFocus: true,
    currentCategories: []
  },

  onLoad(options) {
    // 设置默认日期为今天
    const today = new Date()
    const dateStr = `${today.getFullYear()}-${(today.getMonth() + 1).toString().padStart(2, '0')}-${today.getDate().toString().padStart(2, '0')}`

    this.setData({
      'formData.date': dateStr
    })

    // 加载类别
    this.loadCategories()

    // 如果是编辑模式
    if (options.id) {
      this.loadRecord(options.id)
    }
  },

  // 加载类别
  loadCategories() {
    const categories = wx.getStorageSync('categories') || { expense: [], income: [] }
    this.setData({
      currentCategories: categories.expense
    })
  },

  // 加载记录（编辑模式）
  loadRecord(id) {
    const accountBooks = wx.getStorageSync('accountBooks') || []
    const record = accountBooks.find(item => item.id === id)

    if (record) {
      const categories = wx.getStorageSync('categories')
      const categoryList = record.type === 'expense' ? categories.expense : categories.income

      this.setData({
        formData: {
          type: record.type,
          amount: record.amount,
          categoryId: record.categoryId,
          remark: record.remark,
          date: record.date.split(' ')[0]
        },
        editId: id,
        currentCategories: categoryList,
        isFocus: false
      })
    }
  },

  // 切换类型
  switchType(e) {
    const type = e.currentTarget.dataset.type
    const categories = wx.getStorageSync('categories') || { expense: [], income: [] }
    const categoryList = type === 'expense' ? categories.expense : categories.income

    this.setData({
      'formData.type': type,
      'formData.categoryId': categoryList[0]?.id || 1,
      currentCategories: categoryList
    })
  },

  // 金额输入
  onAmountInput(e) {
    let value = e.detail.value

    // 限制只能输入数字和小数点
    value = value.replace(/[^\d.]/g, '')

    // 只能有一个小数点
    const parts = value.split('.')
    if (parts.length > 2) {
      value = parts[0] + '.' + parts.slice(1).join('')
    }

    // 小数点后最多两位
    if (parts.length === 2 && parts[1].length > 2) {
      value = parts[0] + '.' + parts[1].substring(0, 2)
    }

    this.setData({
      'formData.amount': value
    })
  },

  // 类别选择
  selectCategory(e) {
    const categoryId = e.currentTarget.dataset.id
    this.setData({
      'formData.categoryId': categoryId
    })
  },

  // 备注输入
  onRemarkInput(e) {
    this.setData({
      'formData.remark': e.detail.value
    })
  },

  // 日期选择
  onDateChange(e) {
    this.setData({
      'formData.date': e.detail.value
    })
  },

  // 保存记录
  saveRecord() {
    const { formData, editId } = this.data

    // 验证
    if (!formData.amount || Number(formData.amount) <= 0) {
      wx.showToast({
        title: '请输入有效金额',
        icon: 'none'
      })
      return
    }

    if (!formData.date) {
      wx.showToast({
        title: '请选择日期',
        icon: 'none'
      })
      return
    }

    // 构建记录对象
    const record = {
      id: editId || Date.now(),
      type: formData.type,
      amount: Number(formData.amount),
      categoryId: formData.categoryId,
      remark: formData.remark,
      date: formData.date,
      createTime: editId ? this.getRecordCreateTime(editId) : new Date().toISOString()
    }

    // 获取现有记录
    let accountBooks = wx.getStorageSync('accountBooks') || []

    if (editId) {
      // 更新记录
      const index = accountBooks.findIndex(item => item.id === editId)
      if (index !== -1) {
        accountBooks[index] = record
      }
      wx.showToast({
        title: '更新成功',
        icon: 'success'
      })
    } else {
      // 添加新记录
      accountBooks.unshift(record)
      wx.showToast({
        title: '添加成功',
        icon: 'success'
      })
    }

    // 保存到本地
    wx.setStorageSync('accountBooks', accountBooks)

    // 延迟返回上一页
    setTimeout(() => {
      wx.navigateBack()
    }, 1500)
  },

  // 获取记录的创建时间
  getRecordCreateTime(id) {
    const accountBooks = wx.getStorageSync('accountBooks') || []
    const record = accountBooks.find(item => item.id === id)
    return record ? record.createTime : new Date().toISOString()
  },

  // 删除记录
  deleteRecord() {
    const { editId } = this.data

    wx.showModal({
      title: '确认删除',
      content: '确定要删除这条记录吗？',
      success: (res) => {
        if (res.confirm) {
          let accountBooks = wx.getStorageSync('accountBooks') || []
          accountBooks = accountBooks.filter(item => item.id !== editId)
          wx.setStorageSync('accountBooks', accountBooks)

          wx.showToast({
            title: '删除成功',
            icon: 'success'
          })

          setTimeout(() => {
            wx.navigateBack()
          }, 1500)
        }
      }
    })
  }
})
