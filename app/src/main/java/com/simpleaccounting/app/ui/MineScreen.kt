package com.simpleaccounting.app.ui

import android.content.ClipData
import android.content.ClipboardManager
import android.content.Context
import android.widget.Toast
import androidx.compose.foundation.background
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.ChevronRight
import androidx.compose.material.icons.filled.Delete
import androidx.compose.material.icons.filled.ExitToApp
import androidx.compose.material.icons.filled.Info
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import com.simpleaccounting.app.data.*

@Composable
fun MineScreen(viewModel: MainViewModel) {
    val context = LocalContext.current
    val transactions by viewModel.allTransactions.collectAsState()

    val totalRecords = transactions.size
    val uniqueDates = transactions.map { it.getFormattedDate() }.distinct().size
    val usedCategories = transactions.map { it.categoryId }.distinct().size

    var showClearDialog by remember { mutableStateOf(false) }
    var showAboutDialog by remember { mutableStateOf(false) }

    LaunchedEffect(transactions) {
        // Recalculate stats when transactions change
    }

    Column(
        modifier = Modifier
            .fillMaxSize()
            .padding(16.dp)
    ) {
        // User Card
        Card(
            modifier = Modifier.fillMaxWidth(),
            shape = RoundedCornerShape(16.dp),
            colors = CardDefaults.cardColors(
                containerColor = Color(0xFF4A90E2)
            )
        ) {
            Row(
                modifier = Modifier
                    .fillMaxWidth()
                    .padding(32.dp),
                horizontalArrangement = Arrangement.spacedBy(24.dp),
                verticalAlignment = Alignment.CenterVertically
            ) {
                Box(
                    modifier = Modifier
                        .size(80.dp)
                        .background(
                            Color.White.copy(alpha = 0.2f),
                            RoundedCornerShape(40.dp)
                        ),
                    contentAlignment = Alignment.Center
                ) {
                    Text("👤", fontSize = 40.sp)
                }

                Column(
                    verticalArrangement = Arrangement.spacedBy(8.dp)
                ) {
                    Text(
                        text = "简单记账",
                        color = Color.White,
                        fontSize = 24.sp,
                        fontWeight = FontWeight.Bold
                    )
                    Text(
                        text = "记录每一笔开支",
                        color = Color.White.copy(alpha = 0.8f),
                        fontSize = 14.sp
                    )
                }
            }
        }

        Spacer(modifier = Modifier.height(24.dp))

        // Stats Grid
        Row(
            modifier = Modifier.fillMaxWidth(),
            horizontalArrangement = Arrangement.spacedBy(12.dp)
        ) {
            StatCard(
                title = "记账笔数",
                value = totalRecords.toString(),
                modifier = Modifier.weight(1f)
            )
            StatCard(
                title = "记账天数",
                value = uniqueDates.toString(),
                modifier = Modifier.weight(1f)
            )
            StatCard(
                title = "使用类别",
                value = usedCategories.toString(),
                modifier = Modifier.weight(1f)
            )
        }

        Spacer(modifier = Modifier.height(24.dp))

        // Function List
        Card(
            modifier = Modifier.fillMaxWidth(),
            shape = RoundedCornerShape(12.dp)
        ) {
            Column {
                FunctionItem(
                    icon = "📤",
                    title = "导出数据",
                    onClick = {
                        exportData(context, transactions)
                    }
                )
                Divider(color = Color(0xFFF0F0F0))
                FunctionItem(
                    icon = "🗑️",
                    title = "清空数据",
                    onClick = { showClearDialog = true }
                )
                Divider(color = Color(0xFFF0F0F0))
                FunctionItem(
                    icon = "ℹ️",
                    title = "关于我们",
                    onClick = { showAboutDialog = true }
                )
            }
        }

        Spacer(modifier = Modifier.height(24.dp))

        // Tips Card
        Card(
            modifier = Modifier.fillMaxWidth(),
            shape = RoundedCornerShape(12.dp),
            colors = CardDefaults.cardColors(
                containerColor = Color(0xFFFFF9E6)
            )
        ) {
            Column(
                modifier = Modifier.padding(20.dp),
                verticalArrangement = Arrangement.spacedBy(8.dp)
            ) {
                Text(
                    text = "💡 使用提示",
                    fontSize = 16.sp,
                    fontWeight = FontWeight.Bold,
                    color = Color(0xFFFA8C16)
                )
                Text("• 点击账目可查看详情或编辑", fontSize = 13.sp, color = Color(0xFF8C8C8C))
                Text("• 统计页面支持周/月/年切换", fontSize = 13.sp, color = Color(0xFF8C8C8C))
                Text("• 数据保存在本地，请定期备份", fontSize = 13.sp, color = Color(0xFF8C8C8C))
            }
        }

        Spacer(modifier = Modifier.weight(1f))

        // Version Info
        Text(
            text = "版本 1.0.0",
            modifier = Modifier.fillMaxWidth(),
            textAlign = androidx.compose.ui.text.style.TextAlign.Center,
            color = Color.Gray,
            fontSize = 12.sp
        )
    }

    // Clear Dialog
    if (showClearDialog) {
        AlertDialog(
            onDismissRequest = { showClearDialog = false },
            title = { Text("确认清空") },
            text = { Text("确定要清空所有记账数据吗？此操作不可恢复！") },
            confirmButton = {
                TextButton(
                    onClick = {
                        viewModel.deleteAllTransactions()
                        showClearDialog = false
                        Toast.makeText(context, "清空成功", Toast.LENGTH_SHORT).show()
                    }
                ) {
                    Text("确认", color = Color.Red)
                }
            },
            dismissButton = {
                TextButton(onClick = { showClearDialog = false }) {
                    Text("取消")
                }
            }
        )
    }

    // About Dialog
    if (showAboutDialog) {
        AlertDialog(
            onDismissRequest = { showAboutDialog = false },
            title = { Text("关于简单记账") },
            text = {
                Text(
                    "简单记账是一款轻量级的个人记账工具，界面简洁，操作便捷，帮助您轻松管理个人财务。\n\n版本：1.0.0\n\n如果您有任何建议或问题，欢迎反馈！"
                )
            },
            confirmButton = {
                TextButton(onClick = { showAboutDialog = false }) {
                    Text("知道了")
                }
            }
        )
    }
}

@Composable
fun StatCard(
    title: String,
    value: String,
    modifier: Modifier = Modifier
) {
    Card(
        modifier = modifier,
        shape = RoundedCornerShape(12.dp)
    ) {
        Column(
            modifier = Modifier
                .fillMaxWidth()
                .padding(16.dp),
            horizontalAlignment = Alignment.CenterHorizontally,
            verticalArrangement = Arrangement.spacedBy(8.dp)
        ) {
            Text(
                text = value,
                fontSize = 24.sp,
                fontWeight = FontWeight.Bold,
                color = Color(0xFF4A90E2)
            )
            Text(
                text = title,
                fontSize = 12.sp,
                color = Color.Gray
            )
        }
    }
}

@Composable
fun FunctionItem(
    icon: String,
    title: String,
    onClick: () -> Unit
) {
    Row(
        modifier = Modifier
            .fillMaxWidth()
            .clickable { onClick() }
            .padding(20.dp),
        horizontalArrangement = Arrangement.SpaceBetween,
        verticalAlignment = Alignment.CenterVertically
    ) {
        Row(
            horizontalArrangement = Arrangement.spacedBy(16.dp),
            verticalAlignment = Alignment.CenterVertically
        ) {
            Text(icon, fontSize = 24.sp)
            Text(
                text = title,
                fontSize = 16.sp,
                color = MaterialTheme.colorScheme.onSurface
            )
        }
        Icon(Icons.Default.ChevronRight, contentDescription = null, tint = Color.Gray)
    }
}

fun exportData(context: Context, transactions: List<Transaction>) {
    if (transactions.isEmpty()) {
        Toast.makeText(context, "暂无数据可导出", Toast.LENGTH_SHORT).show()
        return
    }

    val csvContent = buildString {
        appendLine("日期,类型,类别,金额,备注")

        transactions.forEach { transaction ->
            val category = CategoryDefaults.getCategoryById(
                transaction.categoryId,
                transaction.type
            )
            val typeText = if (transaction.type == TransactionType.EXPENSE) "支出" else "收入"

            appendLine("${transaction.getFormattedDate()},$typeText,${category?.name},${transaction.amount},${transaction.remark}")
        }
    }

    val clipboard = context.getSystemService(Context.CLIPBOARD_SERVICE) as ClipboardManager
    val clip = ClipData.newPlainText("Accounting Data", csvContent)
    clipboard.setPrimaryClip(clip)

    Toast.makeText(context, "数据已复制到剪贴板", Toast.LENGTH_SHORT).show()
}
