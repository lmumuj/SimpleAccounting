package com.simpleaccounting.app.data

import androidx.room.Entity
import androidx.room.PrimaryKey
import java.text.SimpleDateFormat
import java.util.Date
import java.util.Locale

@Entity(tableName = "transactions")
data class Transaction(
    @PrimaryKey(autoGenerate = true)
    val id: Long = 0,
    val type: TransactionType,
    val amount: Double,
    val categoryId: Long,
    val remark: String,
    val date: Long = System.currentTimeMillis(),
    val createTime: Long = System.currentTimeMillis()
) {
    fun getFormattedDate(): String {
        val sdf = SimpleDateFormat("yyyy-MM-dd", Locale.getDefault())
        return sdf.format(Date(date))
    }

    fun getDisplayDate(): String {
        val sdf = SimpleDateFormat("MM月dd日", Locale.getDefault())
        return sdf.format(Date(date))
    }

    fun getTime(): String {
        val sdf = SimpleDateFormat("HH:mm", Locale.getDefault())
        return sdf.format(Date(date))
    }
}

enum class TransactionType {
    EXPENSE,
    INCOME
}
