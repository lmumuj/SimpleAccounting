package com.simpleaccounting.app.ui

import android.app.Application
import androidx.lifecycle.AndroidViewModel
import androidx.lifecycle.viewModelScope
import com.simpleaccounting.app.data.*
import kotlinx.coroutines.flow.*
import kotlinx.coroutines.launch

class MainViewModel(application: Application) : AndroidViewModel(application) {
    private val repository: TransactionRepository

    val allTransactions: StateFlow<List<Transaction>> = MutableStateFlow(emptyList())
    val filteredTransactions: StateFlow<List<Transaction>> = MutableStateFlow(emptyList())
    val monthlyExpense: StateFlow<Double> = MutableStateFlow(0.0)
    val monthlyIncome: StateFlow<Double> = MutableStateFlow(0.0)

    private val _filterType = MutableStateFlow<FilterType>(FilterType.ALL)
    val filterType: StateFlow<FilterType> = _filterType.asStateFlow()

    init {
        val database = AppDatabase.getDatabase(application)
        repository = TransactionRepository(database.transactionDao())

        loadTransactions()
    }

    private fun loadTransactions() {
        viewModelScope.launch {
            repository.getAllTransactions().collect { transactions ->
                allTransactions.value = transactions
                applyFilter()

                // Calculate monthly totals
                monthlyExpense.value = repository.getMonthlyTotalByType(TransactionType.EXPENSE) ?: 0.0
                monthlyIncome.value = repository.getMonthlyTotalByType(TransactionType.INCOME) ?: 0.0
            }
        }
    }

    fun setFilterType(type: FilterType) {
        _filterType.value = type
        applyFilter()
    }

    private fun applyFilter() {
        val type = _filterType.value
        filteredTransactions.value = when (type) {
            FilterType.ALL -> allTransactions.value
            FilterType.EXPENSE -> allTransactions.value.filter { it.type == TransactionType.EXPENSE }
            FilterType.INCOME -> allTransactions.value.filter { it.type == TransactionType.INCOME }
        }
    }

    fun deleteTransaction(transaction: Transaction) {
        viewModelScope.launch {
            repository.delete(transaction)
        }
    }

    fun deleteAllTransactions() {
        viewModelScope.launch {
            repository.deleteAll()
        }
    }

    suspend fun getTransactionById(id: Long): Transaction? {
        return repository.getTransactionById(id)
    }

    fun insertTransaction(transaction: Transaction) {
        viewModelScope.launch {
            repository.insert(transaction)
        }
    }

    fun updateTransaction(transaction: Transaction) {
        viewModelScope.launch {
            repository.update(transaction)
        }
    }
}

enum class FilterType {
    ALL, EXPENSE, INCOME
}
