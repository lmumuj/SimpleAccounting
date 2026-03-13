package com.simpleaccounting.app.ui

import android.app.Application
import androidx.lifecycle.AndroidViewModel
import androidx.lifecycle.viewModelScope
import com.simpleaccounting.app.data.*
import kotlinx.coroutines.flow.*
import kotlinx.coroutines.launch

class MainViewModel(application: Application) : AndroidViewModel(application) {
    private val repository: TransactionRepository

    private val _allTransactions = MutableStateFlow<List<Transaction>>(emptyList())
    val allTransactions: StateFlow<List<Transaction>> = _allTransactions.asStateFlow()

    private val _filteredTransactions = MutableStateFlow<List<Transaction>>(emptyList())
    val filteredTransactions: StateFlow<List<Transaction>> = _filteredTransactions.asStateFlow()

    private val _monthlyExpense = MutableStateFlow(0.0)
    val monthlyExpense: StateFlow<Double> = _monthlyExpense.asStateFlow()

    private val _monthlyIncome = MutableStateFlow(0.0)
    val monthlyIncome: StateFlow<Double> = _monthlyIncome.asStateFlow()

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
                _allTransactions.value = transactions
                applyFilter()

                // Calculate monthly totals
                _monthlyExpense.value = repository.getMonthlyTotalByType(TransactionType.EXPENSE) ?: 0.0
                _monthlyIncome.value = repository.getMonthlyTotalByType(TransactionType.INCOME) ?: 0.0
            }
        }
    }

    fun setFilterType(type: FilterType) {
        _filterType.value = type
        applyFilter()
    }

    private fun applyFilter() {
        val type = _filterType.value
        _filteredTransactions.value = when (type) {
            FilterType.ALL -> _allTransactions.value
            FilterType.EXPENSE -> _allTransactions.value.filter { it.type == TransactionType.EXPENSE }
            FilterType.INCOME -> _allTransactions.value.filter { it.type == TransactionType.INCOME }
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
