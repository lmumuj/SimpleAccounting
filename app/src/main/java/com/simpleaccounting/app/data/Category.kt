package com.simpleaccounting.app.data

data class Category(
    val id: Long,
    val name: String,
    val icon: String,
    val type: TransactionType
)

object CategoryDefaults {
    val expenseCategories = listOf(
        Category(1L, "餐饮", "🍔", TransactionType.EXPENSE),
        Category(2L, "交通", "🚗", TransactionType.EXPENSE),
        Category(3L, "购物", "🛒", TransactionType.EXPENSE),
        Category(4L, "娱乐", "🎮", TransactionType.EXPENSE),
        Category(5L, "医疗", "💊", TransactionType.EXPENSE),
        Category(6L, "教育", "📚", TransactionType.EXPENSE),
        Category(7L, "居住", "🏠", TransactionType.EXPENSE),
        Category(8L, "其他", "📦", TransactionType.EXPENSE)
    )

    val incomeCategories = listOf(
        Category(101L, "工资", "💰", TransactionType.INCOME),
        Category(102L, "奖金", "🎁", TransactionType.INCOME),
        Category(103L, "投资", "📈", TransactionType.INCOME),
        Category(104L, "兼职", "💼", TransactionType.INCOME),
        Category(105L, "其他", "📦", TransactionType.INCOME)
    )

    fun getCategoryById(categoryId: Long, type: TransactionType): Category? {
        return when (type) {
            TransactionType.EXPENSE -> expenseCategories.find { it.id == categoryId }
            TransactionType.INCOME -> incomeCategories.find { it.id == categoryId }
        }
    }
}
