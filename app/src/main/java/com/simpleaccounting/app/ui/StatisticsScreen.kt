package com.simpleaccounting.app.ui

import androidx.compose.foundation.background
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import com.github.mikephil.charting.charts.PieChart
import com.github.mikephil.charting.data.PieData
import com.github.mikephil.charting.data.PieDataSet
import com.github.mikephil.charting.data.PieEntry
import com.github.mikephil.charting.utils.ColorTemplate
import com.simpleaccounting.app.data.*
import java.text.DecimalFormat

@Composable
fun StatisticsScreen(viewModel: MainViewModel) {
    val transactions by viewModel.allTransactions.collectAsState()
    var selectedPeriod by remember { mutableStateOf(PeriodType.MONTH) }

    val filteredTransactions = remember(selectedPeriod, transactions) {
        filterTransactionsByPeriod(transactions, selectedPeriod)
    }

    val expenseTransactions = filteredTransactions.filter { it.type == TransactionType.EXPENSE }
    val incomeTransactions = filteredTransactions.filter { it.type == TransactionType.INCOME }

    val totalExpense = expenseTransactions.sumOf { it.amount }
    val totalIncome = incomeTransactions.sumOf { it.amount }
    val balance = totalIncome - totalExpense

    val expenseStats = calculateCategoryStats(expenseTransactions)
    val incomeStats = calculateCategoryStats(incomeTransactions)

    Column(
        modifier = Modifier
            .fillMaxSize()
            .padding(16.dp)
    ) {
        // Period Selector
        Row(
            modifier = Modifier.fillMaxWidth(),
            horizontalArrangement = Arrangement.spacedBy(12.dp)
        ) {
            FilterChip(
                selected = selectedPeriod == PeriodType.WEEK,
                onClick = { selectedPeriod = PeriodType.WEEK },
                label = { Text("本周") },
                modifier = Modifier.weight(1f)
            )
            FilterChip(
                selected = selectedPeriod == PeriodType.MONTH,
                onClick = { selectedPeriod = PeriodType.MONTH },
                label = { Text("本月") },
                modifier = Modifier.weight(1f)
            )
            FilterChip(
                selected = selectedPeriod == PeriodType.YEAR,
                onClick = { selectedPeriod = PeriodType.YEAR },
                label = { Text("本年") },
                modifier = Modifier.weight(1f)
            )
        }

        Spacer(modifier = Modifier.height(16.dp))

        // Summary Card
        Card(
            modifier = Modifier.fillMaxWidth(),
            shape = RoundedCornerShape(16.dp),
            colors = CardDefaults.cardColors(
                containerColor = Color(0xFF4A90E2)
            )
        ) {
            Column(
                modifier = Modifier.padding(24.dp)
            ) {
                Row(
                    modifier = Modifier.fillMaxWidth(),
                    horizontalArrangement = Arrangement.SpaceAround
                ) {
                    Column(horizontalAlignment = Alignment.CenterHorizontally) {
                        Text(
                            text = "总支出",
                            color = Color.White.copy(alpha = 0.9f),
                            fontSize = 14.sp
                        )
                        Spacer(modifier = Modifier.height(8.dp))
                        Text(
                            text = "¥${DecimalFormat("0.00").format(totalExpense)}",
                            color = Color.White,
                            fontSize = 20.sp,
                            fontWeight = FontWeight.Bold
                        )
                    }
                    Column(horizontalAlignment = Alignment.CenterHorizontally) {
                        Text(
                            text = "总收入",
                            color = Color.White.copy(alpha = 0.9f),
                            fontSize = 14.sp
                        )
                        Spacer(modifier = Modifier.height(8.dp))
                        Text(
                            text = "¥${DecimalFormat("0.00").format(totalIncome)}",
                            color = Color.White,
                            fontSize = 20.sp,
                            fontWeight = FontWeight.Bold
                        )
                    }
                }

                Spacer(modifier = Modifier.height(16.dp))

                Row(
                    modifier = Modifier.fillMaxWidth(),
                    horizontalArrangement = Arrangement.Center,
                    verticalAlignment = Alignment.CenterVertically
                ) {
                    Text(
                        text = "结余 ",
                        color = Color.White.copy(alpha = 0.9f),
                        fontSize = 14.sp
                    )
                    Text(
                        text = "¥${DecimalFormat("0.00").format(balance)}",
                        color = if (balance >= 0) Color(0xFF52C41A) else Color(0xFFFF5252),
                        fontSize = 18.sp,
                        fontWeight = FontWeight.Bold
                    )
                }
            }
        }

        Spacer(modifier = Modifier.height(16.dp))

        LazyColumn(
            verticalArrangement = Arrangement.spacedBy(24.dp)
        ) {
            // Expense Statistics
            if (expenseStats.isNotEmpty()) {
                item {
                    Text(
                        text = "支出分类",
                        fontSize = 18.sp,
                        fontWeight = FontWeight.Bold
                    )
                    Spacer(modifier = Modifier.height(16.dp))
                    CategoryStatsSection(
                        stats = expenseStats,
                        total = totalExpense,
                        type = TransactionType.EXPENSE
                    )
                }
            }

            // Income Statistics
            if (incomeStats.isNotEmpty()) {
                item {
                    Text(
                        text = "收入分类",
                        fontSize = 18.sp,
                        fontWeight = FontWeight.Bold
                    )
                    Spacer(modifier = Modifier.height(16.dp))
                    CategoryStatsSection(
                        stats = incomeStats,
                        total = totalIncome,
                        type = TransactionType.INCOME
                    )
                }
            }
        }
    }
}

@Composable
fun CategoryStatsSection(
    stats: List<CategoryStat>,
    total: Double,
    type: TransactionType
) {
    val df = DecimalFormat("0.00")

    Card(
        modifier = Modifier.fillMaxWidth(),
        shape = RoundedCornerShape(12.dp)
    ) {
        Column(
            modifier = Modifier.padding(16.dp)
        ) {
            LazyColumn(
                verticalArrangement = Arrangement.spacedBy(16.dp)
            ) {
                items(stats) { stat ->
                    CategoryStatItem(stat = stat, total = total)
                }
            }
        }
    }
}

@Composable
fun CategoryStatItem(
    stat: CategoryStat,
    total: Double
) {
    val df = DecimalFormat("0.00")
    val percent = ((stat.amount / total) * 100).toInt()

    Row(
        modifier = Modifier.fillMaxWidth(),
        horizontalArrangement = Arrangement.SpaceBetween,
        verticalAlignment = Alignment.CenterVertically
    ) {
        Row(
            horizontalArrangement = Arrangement.spacedBy(12.dp),
            verticalAlignment = Alignment.CenterVertically
        ) {
            Box(
                modifier = Modifier
                    .size(40.dp)
                    .background(stat.color.copy(alpha = 0.2f), RoundedCornerShape(8.dp)),
                contentAlignment = Alignment.Center
            ) {
                Text(stat.icon, fontSize = 20.sp)
            }

            Column {
                Text(
                    text = stat.name,
                    fontSize = 14.sp,
                    fontWeight = FontWeight.Medium
                )
                Text(
                    text = "$percent%",
                    fontSize = 12.sp,
                    color = MaterialTheme.colorScheme.onSurfaceVariant
                )
            }
        }

        Column(
            horizontalAlignment = Alignment.End,
            modifier = Modifier.widthIn(max = 120.dp)
        ) {
            Text(
                text = "¥${df.format(stat.amount)}",
                fontSize = 14.sp,
                fontWeight = FontWeight.Medium
            )
            Box(
                modifier = Modifier
                    .fillMaxWidth()
                    .height(4.dp)
                    .background(
                        Color(0xFFF0F0F0),
                        RoundedCornerShape(2.dp)
                    )
            ) {
                Box(
                    modifier = Modifier
                        .fillMaxWidth(percent / 100f)
                        .height(4.dp)
                        .background(
                            stat.color,
                            RoundedCornerShape(2.dp)
                        )
                )
            }
        }
    }
}

fun filterTransactionsByPeriod(
    transactions: List<Transaction>,
    period: PeriodType
): List<Transaction> {
    val now = System.currentTimeMillis()
    val calendar = java.util.Calendar.getInstance()

    return when (period) {
        PeriodType.WEEK -> {
            calendar.timeInMillis = now
            calendar.set(java.util.Calendar.DAY_OF_WEEK, java.util.Calendar.MONDAY)
            val weekStart = calendar.timeInMillis
            transactions.filter { it.date >= weekStart }
        }
        PeriodType.MONTH -> {
            calendar.timeInMillis = now
            calendar.set(java.util.Calendar.DAY_OF_MONTH, 1)
            calendar.set(java.util.Calendar.HOUR_OF_DAY, 0)
            calendar.set(java.util.Calendar.MINUTE, 0)
            calendar.set(java.util.Calendar.SECOND, 0)
            val monthStart = calendar.timeInMillis
            transactions.filter { it.date >= monthStart }
        }
        PeriodType.YEAR -> {
            calendar.timeInMillis = now
            calendar.set(java.util.Calendar.DAY_OF_YEAR, 1)
            calendar.set(java.util.Calendar.HOUR_OF_DAY, 0)
            calendar.set(java.util.Calendar.MINUTE, 0)
            calendar.set(java.util.Calendar.SECOND, 0)
            val yearStart = calendar.timeInMillis
            transactions.filter { it.date >= yearStart }
        }
    }
}

fun calculateCategoryStats(transactions: List<Transaction>): List<CategoryStat> {
    val colors = listOf(
        Color(0xFF4A90E2),
        Color(0xFF50E3C2),
        Color(0xFFFFD300),
        Color(0xFFFF5252),
        Color(0xFF9B59B6),
        Color(0xFFFF9800),
        Color(0xFF00BCD4),
        Color(0xFF8BC34A)
    )

    val grouped = transactions.groupBy { it.categoryId }
    val stats = grouped.entries.mapIndexed { index, entry ->
        val category = CategoryDefaults.getCategoryById(
            entry.key,
            entry.value.first().type
        )
        CategoryStat(
            name = category?.name ?: "其他",
            icon = category?.icon ?: "📦",
            amount = entry.value.sumOf { it.amount },
            color = colors[index % colors.size]
        )
    }.sortedByDescending { it.amount }

    return stats
}

enum class PeriodType {
    WEEK, MONTH, YEAR
}

data class CategoryStat(
    val name: String,
    val icon: String,
    val amount: Double,
    val color: Color
)
