package com.simpleaccounting.app.ui

import android.widget.Toast
import androidx.compose.foundation.background
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.lazy.grid.GridCells
import androidx.compose.foundation.lazy.grid.LazyVerticalGrid
import androidx.compose.foundation.lazy.grid.items
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.foundation.text.KeyboardOptions
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.automirrored.filled.ArrowBack
import androidx.compose.material.icons.filled.Delete
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.input.KeyboardType
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import androidx.lifecycle.viewmodel.compose.viewModel
import com.simpleaccounting.app.data.*

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun AddEditScreen(
    transactionId: Long?,
    viewModel: MainViewModel,
    onNavigateBack: () -> Unit
) {
    val context = LocalContext.current
    var type by remember { mutableStateOf(TransactionType.EXPENSE) }
    var amount by remember { mutableStateOf("") }
    var selectedCategoryId by remember { mutableStateOf(1L) }
    var remark by remember { mutableStateOf("") }
    var selectedDate by remember { mutableStateOf(System.currentTimeMillis()) }
    var existingTransaction by remember { mutableStateOf<Transaction?>(null) }

    // Load transaction if editing
    LaunchedEffect(transactionId) {
        transactionId?.let {
            existingTransaction = viewModel.viewModelScope.launch {
                viewModel.getTransactionById(it)?.let { transaction ->
                    type = transaction.type
                    amount = transaction.amount.toString()
                    selectedCategoryId = transaction.categoryId
                    remark = transaction.remark
                    selectedDate = transaction.date
                }
            }.let { }
        }
    }

    val categories = remember(type) {
        when (type) {
            TransactionType.EXPENSE -> CategoryDefaults.expenseCategories
            TransactionType.INCOME -> CategoryDefaults.incomeCategories
        }
    }

    Scaffold(
        topBar = {
            TopAppBar(
                title = { Text(if (transactionId == null) "记账" else "编辑账目") },
                navigationIcon = {
                    IconButton(onClick = onNavigateBack) {
                        Icon(Icons.AutoMirrored.Filled.ArrowBack, contentDescription = "返回")
                    }
                },
                actions = {
                    if (transactionId != null && existingTransaction != null) {
                        IconButton(
                            onClick = {
                                existingTransaction?.let { transaction ->
                                    viewModel.deleteTransaction(transaction)
                                    Toast.makeText(context, "删除成功", Toast.LENGTH_SHORT).show()
                                    onNavigateBack()
                                }
                            }
                        ) {
                            Icon(Icons.Default.Delete, contentDescription = "删除")
                        }
                    }
                }
            )
        }
    ) { padding ->
        Column(
            modifier = Modifier
                .fillMaxSize()
                .padding(padding)
                .padding(16.dp)
        ) {
            // Type Switcher
            Row(
                modifier = Modifier.fillMaxWidth(),
                horizontalArrangement = Arrangement.spacedBy(12.dp)
            ) {
                FilterChip(
                    selected = type == TransactionType.EXPENSE,
                    onClick = {
                        type = TransactionType.EXPENSE
                        selectedCategoryId = CategoryDefaults.expenseCategories.first().id
                    },
                    label = { Text("支出") },
                    modifier = Modifier.weight(1f)
                )
                FilterChip(
                    selected = type == TransactionType.INCOME,
                    onClick = {
                        type = TransactionType.INCOME
                        selectedCategoryId = CategoryDefaults.incomeCategories.first().id
                    },
                    label = { Text("收入") },
                    modifier = Modifier.weight(1f)
                )
            }

            Spacer(modifier = Modifier.height(24.dp))

            // Amount Input
            Card(
                modifier = Modifier.fillMaxWidth(),
                shape = RoundedCornerShape(12.dp)
            ) {
                Row(
                    modifier = Modifier
                        .fillMaxWidth()
                        .padding(24.dp),
                    verticalAlignment = Alignment.CenterVertically,
                    horizontalArrangement = Arrangement.spacedBy(12.dp)
                ) {
                    Text(
                        text = "¥",
                        fontSize = 48.sp,
                        fontWeight = FontWeight.Bold,
                        color = MaterialTheme.colorScheme.primary
                    )
                    TextField(
                        value = amount,
                        onValueChange = {
                            // Only allow digits and decimal point
                            if (it.isEmpty() || it.matches(Regex("^\\d*\\.?\\d{0,2}$"))) {
                                amount = it
                            }
                        },
                        placeholder = { Text("0.00") },
                        modifier = Modifier.weight(1f),
                        colors = TextFieldDefaults.colors(
                            focusedContainerColor = Color.Transparent,
                            unfocusedContainerColor = Color.Transparent,
                            focusedIndicatorColor = Color.Transparent,
                            unfocusedIndicatorColor = Color.Transparent
                        ),
                        textStyle = LocalTextStyle.current.copy(
                            fontSize = 40.sp,
                            fontWeight = FontWeight.Bold
                        ),
                        keyboardOptions = KeyboardOptions(keyboardType = KeyboardType.Decimal)
                    )
                }
            }

            Spacer(modifier = Modifier.height(24.dp))

            // Category Selection
            Text(
                text = "选择类别",
                fontSize = 16.sp,
                fontWeight = FontWeight.Bold
            )
            Spacer(modifier = Modifier.height(12.dp))

            LazyVerticalGrid(
                columns = GridCells.Fixed(4),
                horizontalArrangement = Arrangement.spacedBy(12.dp),
                verticalArrangement = Arrangement.spacedBy(12.dp),
                modifier = Modifier.fillMaxWidth()
            ) {
                items(categories) { category ->
                    CategoryItem(
                        category = category,
                        selected = selectedCategoryId == category.id,
                        onClick = { selectedCategoryId = category.id }
                    )
                }
            }

            Spacer(modifier = Modifier.height(24.dp))

            // Remark Input
            Text(
                text = "备注",
                fontSize = 16.sp,
                fontWeight = FontWeight.Bold
            )
            Spacer(modifier = Modifier.height(8.dp))
            TextField(
                value = remark,
                onValueChange = { remark = it },
                placeholder = { Text("写点什么...") },
                modifier = Modifier.fillMaxWidth(),
                singleLine = true
            )

            Spacer(modifier = Modifier.height(24.dp))

            // Date Picker (Simplified - just display date)
            Text(
                text = "日期",
                fontSize = 16.sp,
                fontWeight = FontWeight.Bold
            )
            Spacer(modifier = Modifier.height(8.dp))

            val sdf = java.text.SimpleDateFormat("yyyy-MM-dd", java.util.Locale.getDefault())
            var showDatePicker by remember { mutableStateOf(false) }

            OutlinedButton(
                onClick = { /* TODO: Add date picker dialog */ },
                modifier = Modifier.fillMaxWidth()
            ) {
                Text(sdf.format(java.util.Date(selectedDate)))
            }

            Spacer(modifier = Modifier.height(32.dp))

            // Save Button
            Button(
                onClick = {
                    val amountValue = amount.toDoubleOrNull()
                    if (amountValue == null || amountValue <= 0) {
                        Toast.makeText(context, "请输入有效金额", Toast.LENGTH_SHORT).show()
                        return@Button
                    }

                    val transaction = Transaction(
                        id = transactionId ?: 0,
                        type = type,
                        amount = amountValue,
                        categoryId = selectedCategoryId,
                        remark = remark,
                        date = selectedDate,
                        createTime = existingTransaction?.createTime ?: System.currentTimeMillis()
                    )

                    viewModel.viewModelScope.launch {
                        if (transactionId == null) {
                            viewModel.insertTransaction(transaction)
                        } else {
                            viewModel.updateTransaction(transaction)
                        }
                        Toast.makeText(context, "保存成功", Toast.LENGTH_SHORT).show()
                        onNavigateBack()
                    }
                },
                modifier = Modifier
                    .fillMaxWidth()
                    .height(56.dp),
                shape = RoundedCornerShape(12.dp)
            ) {
                Text("保存", fontSize = 16.sp, fontWeight = FontWeight.Bold)
            }
        }
    }
}

@Composable
fun CategoryItem(
    category: Category,
    selected: Boolean,
    onClick: () -> Unit
) {
    Column(
        modifier = Modifier
            .width(70.dp)
            .clickable { onClick() },
        horizontalAlignment = Alignment.CenterHorizontally,
        verticalArrangement = Arrangement.spacedBy(8.dp)
    ) {
        Box(
            modifier = Modifier
                .size(56.dp)
                .background(
                    if (selected) Color(0xFFF0F5FF) else Color.Transparent,
                    RoundedCornerShape(12.dp)
                ),
            contentAlignment = Alignment.Center
        ) {
            Text(category.icon, fontSize = 28.sp)
        }
        Text(
            text = category.name,
            fontSize = 12.sp,
            color = if (selected) MaterialTheme.colorScheme.primary else MaterialTheme.colorScheme.onSurface
        )
    }
}
