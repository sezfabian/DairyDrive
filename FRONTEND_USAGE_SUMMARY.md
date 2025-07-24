# DairyDrive Farm API - Frontend Usage Summary

## Quick Start Guide for Frontend Developers

### Authentication Setup
```javascript
// Set up authentication headers for all API calls
const API_BASE_URL = '/api/farms/';
const authHeaders = {
  'Authorization': `Token ${userToken}`,
  'Content-Type': 'application/json'
};

// Example fetch wrapper
const apiCall = async (endpoint, options = {}) => {
  const response = await fetch(`${API_BASE_URL}${endpoint}`, {
    ...options,
    headers: {
      ...authHeaders,
      ...options.headers
    }
  });
  
  if (!response.ok) {
    throw new Error(`API Error: ${response.status}`);
  }
  
  return response.json();
};
```

---

## 1. FARM MANAGEMENT

### Get All Farms
```javascript
const getFarms = async () => {
  try {
    const farms = await apiCall('get_farms');
    return farms;
  } catch (error) {
    console.error('Error fetching farms:', error);
    throw error;
  }
};
```

### Get Specific Farm
```javascript
const getFarm = async (farmId) => {
  try {
    const farm = await apiCall(`get_farm/${farmId}`);
    return farm;
  } catch (error) {
    console.error('Error fetching farm:', error);
    throw error;
  }
};
```

### Create Farm
```javascript
const createFarm = async (farmData) => {
  try {
    const newFarm = await apiCall('create_farm', {
      method: 'POST',
      body: JSON.stringify({
        name: farmData.name,
        address: farmData.address,
        phone: farmData.phone,
        size: farmData.size,
        size_unit: farmData.sizeUnit,
        description: farmData.description
      })
    });
    return newFarm;
  } catch (error) {
    console.error('Error creating farm:', error);
    throw error;
  }
};
```

### Edit Farm
```javascript
const editFarm = async (farmId, updates) => {
  try {
    const updatedFarm = await apiCall(`edit_farm/${farmId}`, {
      method: 'POST',
      body: JSON.stringify(updates)
    });
    return updatedFarm;
  } catch (error) {
    console.error('Error updating farm:', error);
    throw error;
  }
};
```

---

## 2. TRANSACTION MANAGEMENT

### Get All Transactions
```javascript
const getTransactions = async (farmId) => {
  try {
    const transactions = await apiCall(`get_transactions/${farmId}`);
    return transactions;
  } catch (error) {
    console.error('Error fetching transactions:', error);
    throw error;
  }
};
```

### Create Transaction
```javascript
const createTransaction = async (farmId, transactionData) => {
  try {
    const newTransaction = await apiCall(`add_transaction/${farmId}`, {
      method: 'POST',
      body: JSON.stringify({
        transaction_type: transactionData.type, // 'incoming' or 'outgoing'
        payment_method: transactionData.paymentMethod,
        amount: transactionData.amount,
        transaction_date: transactionData.date,
        description: transactionData.description
      })
    });
    return newTransaction;
  } catch (error) {
    console.error('Error creating transaction:', error);
    throw error;
  }
};
```

### Get Transaction by ID
```javascript
const getTransactionById = async (farmId, transactionId) => {
  try {
    const transaction = await apiCall(`get_transaction/${farmId}/${transactionId}`);
    return transaction;
  } catch (error) {
    console.error('Error fetching transaction:', error);
    throw error;
  }
};
```

### Edit Transaction
```javascript
const editTransaction = async (farmId, transactionId, updates) => {
  try {
    const updatedTransaction = await apiCall(`edit_transaction/${farmId}/${transactionId}`, {
      method: 'POST',
      body: JSON.stringify(updates)
    });
    return updatedTransaction;
  } catch (error) {
    console.error('Error updating transaction:', error);
    throw error;
  }
};
```

### Delete Transaction
```javascript
const deleteTransaction = async (farmId, transactionId) => {
  try {
    const result = await apiCall(`delete_transaction/${farmId}/${transactionId}`, {
      method: 'POST'
    });
    return result;
  } catch (error) {
    console.error('Error deleting transaction:', error);
    throw error;
  }
};
```

---

## 3. EQUIPMENT MANAGEMENT

### Get All Equipment
```javascript
const getEquipment = async (farmId) => {
  try {
    const equipment = await apiCall(`get_equipment/${farmId}`);
    return equipment;
  } catch (error) {
    console.error('Error fetching equipment:', error);
    throw error;
  }
};
```

### Create Equipment
```javascript
const createEquipment = async (farmId, equipmentData) => {
  try {
    const newEquipment = await apiCall(`add_equipment/${farmId}`, {
      method: 'POST',
      body: JSON.stringify({
        name: equipmentData.name,
        description: equipmentData.description,
        quantity: equipmentData.quantity,
        cost: equipmentData.cost,
        condition: equipmentData.condition,
        purchase_date: equipmentData.purchaseDate,
        last_maintenance_date: equipmentData.lastMaintenanceDate,
        next_maintenance_date: equipmentData.nextMaintenanceDate
      })
    });
    return newEquipment;
  } catch (error) {
    console.error('Error creating equipment:', error);
    throw error;
  }
};
```

### Get Equipment by ID
```javascript
const getEquipmentById = async (farmId, equipmentId) => {
  try {
    const equipment = await apiCall(`get_equipment_item/${farmId}/${equipmentId}`);
    return equipment;
  } catch (error) {
    console.error('Error fetching equipment:', error);
    throw error;
  }
};
```

### Edit Equipment
```javascript
const editEquipment = async (farmId, equipmentId, updates) => {
  try {
    const updatedEquipment = await apiCall(`edit_equipment/${farmId}/${equipmentId}`, {
      method: 'POST',
      body: JSON.stringify(updates)
    });
    return updatedEquipment;
  } catch (error) {
    console.error('Error updating equipment:', error);
    throw error;
  }
};
```

### Delete Equipment
```javascript
const deleteEquipment = async (farmId, equipmentId) => {
  try {
    const result = await apiCall(`delete_equipment/${farmId}/${equipmentId}`, {
      method: 'POST'
    });
    return result;
  } catch (error) {
    console.error('Error deleting equipment:', error);
    throw error;
  }
};
```

---

## 4. EQUIPMENT PURCHASE MANAGEMENT

### Get All Equipment Purchases
```javascript
const getEquipmentPurchases = async (farmId) => {
  try {
    const purchases = await apiCall(`get_equipment_purchases/${farmId}`);
    return purchases;
  } catch (error) {
    console.error('Error fetching equipment purchases:', error);
    throw error;
  }
};
```

### Create Equipment Purchase
```javascript
const createEquipmentPurchase = async (farmId, purchaseData) => {
  try {
    const newPurchase = await apiCall(`add_equipment_purchase/${farmId}`, {
      method: 'POST',
      body: JSON.stringify({
        equipment_name: purchaseData.equipmentName,
        description: purchaseData.description,
        quantity: purchaseData.quantity,
        unit_cost: purchaseData.unitCost,
        supplier: purchaseData.supplier,
        supplier_contact: purchaseData.supplierContact,
        purchase_date: purchaseData.purchaseDate,
        delivery_date: purchaseData.deliveryDate,
        warranty_expiry: purchaseData.warrantyExpiry,
        payment_method: purchaseData.paymentMethod,
        due_date: purchaseData.dueDate,
        notes: purchaseData.notes
      })
    });
    return newPurchase;
  } catch (error) {
    console.error('Error creating equipment purchase:', error);
    throw error;
  }
};
```

### Get Equipment Purchase by ID
```javascript
const getEquipmentPurchaseById = async (farmId, purchaseId) => {
  try {
    const purchase = await apiCall(`get_equipment_purchase/${farmId}/${purchaseId}`);
    return purchase;
  } catch (error) {
    console.error('Error fetching equipment purchase:', error);
    throw error;
  }
};
```

### Edit Equipment Purchase
```javascript
const editEquipmentPurchase = async (farmId, purchaseId, updates) => {
  try {
    const updatedPurchase = await apiCall(`edit_equipment_purchase/${farmId}/${purchaseId}`, {
      method: 'POST',
      body: JSON.stringify(updates)
    });
    return updatedPurchase;
  } catch (error) {
    console.error('Error updating equipment purchase:', error);
    throw error;
  }
};
```

### Delete Equipment Purchase
```javascript
const deleteEquipmentPurchase = async (farmId, purchaseId) => {
  try {
    const result = await apiCall(`delete_equipment_purchase/${farmId}/${purchaseId}`, {
      method: 'POST'
    });
    return result;
  } catch (error) {
    console.error('Error deleting equipment purchase:', error);
    throw error;
  }
};
```

### Link Transaction to Equipment Purchase
```javascript
const linkTransactionToPurchase = async (farmId, purchaseId, transactionId) => {
  try {
    const updatedPurchase = await apiCall(`add_equipment_purchase_transaction/${farmId}/${purchaseId}`, {
      method: 'POST',
      body: JSON.stringify({
        transaction_id: transactionId
      })
    });
    return updatedPurchase;
  } catch (error) {
    console.error('Error linking transaction to purchase:', error);
    throw error;
  }
};
```

---

## 5. EXPENSE MANAGEMENT

### Get All Expenses
```javascript
const getExpenses = async (farmId) => {
  try {
    const expenses = await apiCall(`get_expenses/${farmId}`);
    return expenses;
  } catch (error) {
    console.error('Error fetching expenses:', error);
    throw error;
  }
};
```

### Create Expense
```javascript
const createExpense = async (farmId, expenseData) => {
  try {
    const newExpense = await apiCall(`add_expense/${farmId}`, {
      method: 'POST',
      body: JSON.stringify({
        category: expenseData.category,
        description: expenseData.description,
        amount: expenseData.amount,
        due_date: expenseData.dueDate
      })
    });
    return newExpense;
  } catch (error) {
    console.error('Error creating expense:', error);
    throw error;
  }
};
```

### Get Expense by ID
```javascript
const getExpenseById = async (farmId, expenseId) => {
  try {
    const expense = await apiCall(`get_expense/${farmId}/${expenseId}`);
    return expense;
  } catch (error) {
    console.error('Error fetching expense:', error);
    throw error;
  }
};
```

### Edit Expense
```javascript
const editExpense = async (farmId, expenseId, updates) => {
  try {
    const updatedExpense = await apiCall(`edit_expense/${farmId}/${expenseId}`, {
      method: 'POST',
      body: JSON.stringify(updates)
    });
    return updatedExpense;
  } catch (error) {
    console.error('Error updating expense:', error);
    throw error;
  }
};
```

### Delete Expense
```javascript
const deleteExpense = async (farmId, expenseId) => {
  try {
    const result = await apiCall(`delete_expense/${farmId}/${expenseId}`, {
      method: 'POST'
    });
    return result;
  } catch (error) {
    console.error('Error deleting expense:', error);
    throw error;
  }
};
```

### Link Transaction to Expense
```javascript
const linkTransactionToExpense = async (farmId, expenseId, transactionId) => {
  try {
    const updatedExpense = await apiCall(`add_expense_transaction/${farmId}/${expenseId}`, {
      method: 'POST',
      body: JSON.stringify({
        transaction_id: transactionId
      })
    });
    return updatedExpense;
  } catch (error) {
    console.error('Error linking transaction to expense:', error);
    throw error;
  }
};
```

---

## 6. EXPENSE CATEGORIES

### Get Expense Categories
```javascript
const getExpenseCategories = async (farmId) => {
  try {
    const categories = await apiCall(`get_expense_categories/${farmId}`);
    return categories;
  } catch (error) {
    console.error('Error fetching expense categories:', error);
    throw error;
  }
};
```

### Create Expense Category
```javascript
const createExpenseCategory = async (farmId, categoryData) => {
  try {
    const newCategory = await apiCall(`add_expense_category/${farmId}`, {
      method: 'POST',
      body: JSON.stringify({
        name: categoryData.name,
        description: categoryData.description,
        color: categoryData.color || '#3B82F6',
        is_active: categoryData.isActive !== false
      })
    });
    return newCategory;
  } catch (error) {
    console.error('Error creating expense category:', error);
    throw error;
  }
};
```

### Edit Expense Category
```javascript
const editExpenseCategory = async (farmId, categoryId, updates) => {
  try {
    const updatedCategory = await apiCall(`edit_expense_category/${farmId}/${categoryId}`, {
      method: 'POST',
      body: JSON.stringify(updates)
    });
    return updatedCategory;
  } catch (error) {
    console.error('Error updating expense category:', error);
    throw error;
  }
};
```

### Delete Expense Category
```javascript
const deleteExpenseCategory = async (farmId, categoryId) => {
  try {
    const result = await apiCall(`delete_expense_category/${farmId}/${categoryId}`, {
      method: 'POST'
    });
    return result;
  } catch (error) {
    console.error('Error deleting expense category:', error);
    throw error;
  }
};
```

---

## 7. FARM STATISTICS

### Get Comprehensive Farm Statistics
```javascript
// Get statistics for last 30 days (default)
const getFarmStatistics = async (farmId) => {
  try {
    const response = await apiCall(`/farms/get_farm_statistics/${farmId}`, 'GET');
    return response;
  } catch (error) {
    console.error('Error fetching farm statistics:', error);
    throw error;
  }
};

// Get statistics for custom date range
const getFarmStatisticsWithDateRange = async (farmId, startDate, endDate) => {
  try {
    const params = new URLSearchParams({
      start_date: startDate,
      end_date: endDate
    });
    const response = await apiCall(`/farms/get_farm_statistics/${farmId}/?${params}`, 'GET');
    return response;
  } catch (error) {
    console.error('Error fetching farm statistics:', error);
    throw error;
  }
};

// Example usage with date range
const stats = await getFarmStatisticsWithDateRange(1, '2024-01-01', '2024-01-31');
console.log('Farm Summary:', stats.summary);
console.log('Cost Breakdown:', stats.cost_breakdown);
console.log('Revenue Breakdown:', stats.revenue_breakdown);
console.log('Daily Summary:', stats.time_series.daily_summary);
```

### React Component Example - Farm Dashboard
```jsx
import React, { useState, useEffect } from 'react';
import { useQuery } from '@tanstack/vue-query';

const FarmDashboard = ({ farmId }) => {
  const [dateRange, setDateRange] = useState({
    startDate: '',
    endDate: ''
  });

  const { data: statistics, isLoading, error } = useQuery({
    queryKey: ['farmStatistics', farmId, dateRange.startDate, dateRange.endDate],
    queryFn: async () => {
      const params = new URLSearchParams();
      if (dateRange.startDate) params.append('start_date', dateRange.startDate);
      if (dateRange.endDate) params.append('end_date', dateRange.endDate);
      
      const response = await api.get(`/farms/get_farm_statistics/${farmId}/?${params}`);
      return response.data;
    },
    enabled: !!farmId
  });

  if (isLoading) return <div>Loading statistics...</div>;
  if (error) return <div>Error loading statistics: {error.message}</div>;

  return (
    <div className="farm-dashboard">
      <div className="dashboard-header">
        <h2>{statistics.farm_info.farm_name} Dashboard</h2>
        <div className="date-filters">
          <input
            type="date"
            value={dateRange.startDate}
            onChange={(e) => setDateRange(prev => ({ ...prev, startDate: e.target.value }))}
            placeholder="Start Date"
          />
          <input
            type="date"
            value={dateRange.endDate}
            onChange={(e) => setDateRange(prev => ({ ...prev, endDate: e.target.value }))}
            placeholder="End Date"
          />
        </div>
      </div>

      {/* Summary Cards */}
      <div className="summary-cards">
        <div className="card">
          <h3>Total Revenue</h3>
          <p className="amount">${statistics.summary.total_revenue.toFixed(2)}</p>
        </div>
        <div className="card">
          <h3>Total Costs</h3>
          <p className="amount">${statistics.summary.total_costs.toFixed(2)}</p>
        </div>
        <div className="card">
          <h3>Net Income</h3>
          <p className={`amount ${statistics.summary.net_income >= 0 ? 'positive' : 'negative'}`}>
            ${statistics.summary.net_income.toFixed(2)}
          </p>
        </div>
        <div className="card">
          <h3>Profit Margin</h3>
          <p className="amount">{statistics.summary.profit_margin.toFixed(1)}%</p>
        </div>
      </div>

      {/* Cost Breakdown Chart */}
      <div className="chart-section">
        <h3>Cost Breakdown</h3>
        <div className="cost-breakdown">
          {Object.entries(statistics.cost_breakdown).map(([category, data]) => (
            <div key={category} className="cost-item">
              <span className="category">{category.replace('_', ' ').toUpperCase()}</span>
              <span className="amount">${data.amount.toFixed(2)}</span>
              <span className="percentage">({data.percentage.toFixed(1)}%)</span>
            </div>
          ))}
        </div>
      </div>

      {/* Revenue Breakdown Chart */}
      <div className="chart-section">
        <h3>Revenue Breakdown</h3>
        <div className="revenue-breakdown">
          {Object.entries(statistics.revenue_breakdown).map(([source, data]) => (
            <div key={source} className="revenue-item">
              <span className="source">{source.replace('_', ' ').toUpperCase()}</span>
              <span className="amount">${data.amount.toFixed(2)}</span>
              <span className="percentage">({data.percentage.toFixed(1)}%)</span>
            </div>
          ))}
        </div>
      </div>

      {/* Time Series Data */}
      <div className="time-series">
        <h3>Daily Summary (Last 7 Days)</h3>
        <div className="daily-chart">
          {statistics.time_series.daily_summary.map((day, index) => (
            <div key={index} className="day-bar">
              <div className="day-label">{day.day_name}</div>
              <div className="bar-container">
                <div 
                  className="revenue-bar" 
                  style={{ height: `${(day.revenue / Math.max(...statistics.time_series.daily_summary.map(d => d.revenue))) * 100}%` }}
                ></div>
                <div 
                  className="cost-bar" 
                  style={{ height: `${(day.costs / Math.max(...statistics.time_series.daily_summary.map(d => d.costs))) * 100}%` }}
                ></div>
              </div>
              <div className="day-totals">
                <span className="revenue">${day.revenue.toFixed(0)}</span>
                <span className="costs">${day.costs.toFixed(0)}</span>
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Weekly Summary */}
      <div className="weekly-summary">
        <h3>Weekly Summary (Last 8 Weeks)</h3>
        <div className="weekly-chart">
          {statistics.time_series.weekly_summary.map((week, index) => (
            <div key={index} className="week-item">
              <div className="week-label">{week.week_number}</div>
              <div className="week-data">
                <span>Revenue: ${week.revenue.toFixed(0)}</span>
                <span>Costs: ${week.costs.toFixed(0)}</span>
                <span className={`net ${week.net >= 0 ? 'positive' : 'negative'}`}>
                  Net: ${week.net.toFixed(0)}
                </span>
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Monthly Summary */}
      <div className="monthly-summary">
        <h3>Monthly Summary (Last 6 Months)</h3>
        <div className="monthly-chart">
          {statistics.time_series.monthly_summary.map((month, index) => (
            <div key={index} className="month-item">
              <div className="month-label">{month.month}</div>
              <div className="month-data">
                <span>Revenue: ${month.revenue.toFixed(0)}</span>
                <span>Costs: ${month.costs.toFixed(0)}</span>
                <span className={`net ${month.net >= 0 ? 'positive' : 'negative'}`}>
                  Net: ${month.net.toFixed(0)}
                </span>
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Yearly Comparison */}
      <div className="yearly-comparison">
        <h3>Yearly Comparison</h3>
        <div className="yearly-data">
          <div className="year-card">
            <h4>{statistics.time_series.yearly_summary.this_year.year}</h4>
            <p>Revenue: ${statistics.time_series.yearly_summary.this_year.revenue.toFixed(0)}</p>
            <p>Costs: ${statistics.time_series.yearly_summary.this_year.costs.toFixed(0)}</p>
            <p className={`net ${statistics.time_series.yearly_summary.this_year.net >= 0 ? 'positive' : 'negative'}`}>
              Net: ${statistics.time_series.yearly_summary.this_year.net.toFixed(0)}
            </p>
          </div>
          <div className="year-card">
            <h4>{statistics.time_series.yearly_summary.last_year.year}</h4>
            <p>Revenue: ${statistics.time_series.yearly_summary.last_year.revenue.toFixed(0)}</p>
            <p>Costs: ${statistics.time_series.yearly_summary.last_year.costs.toFixed(0)}</p>
            <p className={`net ${statistics.time_series.yearly_summary.last_year.net >= 0 ? 'positive' : 'negative'}`}>
              Net: ${statistics.time_series.yearly_summary.last_year.net.toFixed(0)}
            </p>
          </div>
        </div>
      </div>
    </div>
  );
};
```

### Vue Query Hook for Farm Statistics
```javascript
// Farm Statistics Hook
export function useFarmStatisticsQuery(farmId, startDate = null, endDate = null) {
  const user = useUserStore();
  const actualFarmId = farmId || user.farm.id;
  
  return useQuery({
    queryKey: ['farmStatistics', actualFarmId, startDate, endDate],
    queryFn: async () => {
      const params = new URLSearchParams();
      if (startDate) params.append('start_date', startDate);
      if (endDate) params.append('end_date', endDate);
      
      const response = await api.get(`/farms/get_farm_statistics/${actualFarmId}/?${params}`);
      return response.data;
    },
    enabled: !!actualFarmId,
    staleTime: 1000 * 60 * 5, // 5 minutes
    retry: 1,
  });
}

// Usage example
const { data: statistics, isLoading, error } = useFarmStatisticsQuery(1, '2024-01-01', '2024-01-31');
```

---

## 8. FARM USERS

### Get Farm Users
```javascript
const getFarmUsers = async (farmId) => {
  try {
    const users = await apiCall(`get_farm_users/${farmId}`);
    return users;
  } catch (error) {
    console.error('Error fetching farm users:', error);
    throw error;
  }
};
```

---

## 9. FARM SETTINGS

### Get Farm Settings
```javascript
const getFarmSettings = async (farmId) => {
  try {
    const settings = await apiCall(`get_farm_settings/${farmId}`);
    return settings;
  } catch (error) {
    console.error('Error fetching farm settings:', error);
    throw error;
  }
};
```

### Update Farm Settings
```javascript
const updateFarmSettings = async (farmId, settingsData) => {
  try {
    const updatedSettings = await apiCall(`update_farm_settings/${farmId}`, {
      method: 'POST',
      body: JSON.stringify(settingsData)
    });
    return updatedSettings;
  } catch (error) {
    console.error('Error updating farm settings:', error);
    throw error;
  }
};
```

---

## 10. REACT COMPONENT EXAMPLES

### Farm Dashboard Component
```jsx
import React, { useState, useEffect } from 'react';

const FarmDashboard = ({ farmId }) => {
  const [farm, setFarm] = useState(null);
  const [statistics, setStatistics] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchFarmData = async () => {
      try {
        setLoading(true);
        const [farmData, statsData] = await Promise.all([
          getFarm(farmId),
          getFarmStatistics(farmId)
        ]);
        setFarm(farmData);
        setStatistics(statsData);
      } catch (err) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    };

    if (farmId) {
      fetchFarmData();
    }
  }, [farmId]);

  if (loading) return <div>Loading farm data...</div>;
  if (error) return <div>Error: {error}</div>;
  if (!farm) return <div>Farm not found</div>;

  return (
    <div>
      <h2>{farm.name}</h2>
      <div className="farm-stats">
        <div className="stat-card">
          <h3>Total Income</h3>
          <p>${statistics.total_income}</p>
        </div>
        <div className="stat-card">
          <h3>Total Expenses</h3>
          <p>${statistics.total_expenses}</p>
        </div>
        <div className="stat-card">
          <h3>Net Income</h3>
          <p>${statistics.net_income}</p>
        </div>
        <div className="stat-card">
          <h3>Equipment Count</h3>
          <p>{statistics.total_equipment}</p>
        </div>
      </div>
    </div>
  );
};
```

### Equipment Purchase Form
```jsx
import React, { useState } from 'react';

const EquipmentPurchaseForm = ({ farmId, onSuccess }) => {
  const [formData, setFormData] = useState({
    equipment_name: '',
    description: '',
    quantity: 1,
    unit_cost: '',
    supplier: '',
    supplier_contact: '',
    purchase_date: '',
    delivery_date: '',
    warranty_expiry: '',
    payment_method: 'bank_transfer',
    due_date: '',
    notes: ''
  });

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const newPurchase = await createEquipmentPurchase(farmId, formData);
      onSuccess(newPurchase);
      // Reset form or redirect
    } catch (error) {
      console.error('Error creating purchase:', error);
    }
  };

  return (
    <form onSubmit={handleSubmit}>
      <input
        type="text"
        placeholder="Equipment Name"
        value={formData.equipment_name}
        onChange={(e) => setFormData({...formData, equipment_name: e.target.value})}
        required
      />
      <textarea
        placeholder="Description"
        value={formData.description}
        onChange={(e) => setFormData({...formData, description: e.target.value})}
        required
      />
      <input
        type="number"
        placeholder="Quantity"
        value={formData.quantity}
        onChange={(e) => setFormData({...formData, quantity: parseInt(e.target.value)})}
        min="1"
        required
      />
      <input
        type="number"
        step="0.01"
        placeholder="Unit Cost"
        value={formData.unit_cost}
        onChange={(e) => setFormData({...formData, unit_cost: parseFloat(e.target.value)})}
        required
      />
      <input
        type="date"
        value={formData.purchase_date}
        onChange={(e) => setFormData({...formData, purchase_date: e.target.value})}
        required
      />
      <input
        type="date"
        value={formData.due_date}
        onChange={(e) => setFormData({...formData, due_date: e.target.value})}
        required
      />
      <select
        value={formData.payment_method}
        onChange={(e) => setFormData({...formData, payment_method: e.target.value})}
      >
        <option value="cash">Cash</option>
        <option value="bank_transfer">Bank Transfer</option>
        <option value="mobile_money">Mobile Money</option>
        <option value="cheque">Cheque</option>
        <option value="credit">Credit</option>
        <option value="lease">Lease</option>
        <option value="other">Other</option>
      </select>
      <button type="submit">Create Purchase</button>
    </form>
  );
};
```

### Expense Category Management Component
```jsx
import React, { useState, useEffect } from 'react';

const ExpenseCategoryManager = ({ farmId }) => {
  const [categories, setCategories] = useState([]);
  const [loading, setLoading] = useState(true);
  const [showForm, setShowForm] = useState(false);
  const [editingCategory, setEditingCategory] = useState(null);
  const [formData, setFormData] = useState({
    name: '',
    description: '',
    color: '#3B82F6',
    is_active: true
  });

  useEffect(() => {
    fetchCategories();
  }, [farmId]);

  const fetchCategories = async () => {
    try {
      setLoading(true);
      const data = await getExpenseCategories(farmId);
      setCategories(data);
    } catch (error) {
      console.error('Error fetching categories:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      if (editingCategory) {
        await editExpenseCategory(farmId, editingCategory.id, formData);
      } else {
        await createExpenseCategory(farmId, formData);
      }
      setShowForm(false);
      setEditingCategory(null);
      setFormData({ name: '', description: '', color: '#3B82F6', is_active: true });
      fetchCategories();
    } catch (error) {
      console.error('Error saving category:', error);
    }
  };

  const handleEdit = (category) => {
    setEditingCategory(category);
    setFormData({
      name: category.name,
      description: category.description,
      color: category.color,
      is_active: category.is_active
    });
    setShowForm(true);
  };

  const handleDelete = async (categoryId) => {
    if (window.confirm('Are you sure you want to delete this category?')) {
      try {
        await deleteExpenseCategory(farmId, categoryId);
        fetchCategories();
      } catch (error) {
        console.error('Error deleting category:', error);
      }
    }
  };

  if (loading) return <div>Loading categories...</div>;

  return (
    <div>
      <div className="category-header">
        <h3>Expense Categories</h3>
        <button onClick={() => setShowForm(true)}>Add Category</button>
      </div>

      {showForm && (
        <form onSubmit={handleSubmit} className="category-form">
          <input
            type="text"
            placeholder="Category Name"
            value={formData.name}
            onChange={(e) => setFormData({...formData, name: e.target.value})}
            required
          />
          <textarea
            placeholder="Description"
            value={formData.description}
            onChange={(e) => setFormData({...formData, description: e.target.value})}
          />
          <input
            type="color"
            value={formData.color}
            onChange={(e) => setFormData({...formData, color: e.target.value})}
          />
          <label>
            <input
              type="checkbox"
              checked={formData.is_active}
              onChange={(e) => setFormData({...formData, is_active: e.target.checked})}
            />
            Active
          </label>
          <button type="submit">
            {editingCategory ? 'Update Category' : 'Create Category'}
          </button>
          <button type="button" onClick={() => {
            setShowForm(false);
            setEditingCategory(null);
            setFormData({ name: '', description: '', color: '#3B82F6', is_active: true });
          }}>
            Cancel
          </button>
        </form>
      )}

      <div className="categories-list">
        {categories.map(category => (
          <div key={category.id} className="category-item" style={{borderLeftColor: category.color}}>
            <div className="category-info">
              <h4>{category.name}</h4>
              <p>{category.description}</p>
              <span className="expense-count">{category.expense_count} expenses</span>
            </div>
            <div className="category-actions">
              <button onClick={() => handleEdit(category)}>Edit</button>
              <button onClick={() => handleDelete(category.id)} disabled={category.expense_count > 0}>
                Delete
              </button>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};
```

---

## 11. DATA STRUCTURES

### Farm Object
```javascript
{
  id: 1,
  name: "Sunshine Dairy Farm",
  address: "123 Farm Road, Dairy County",
  phone: "+1234567890",
  coordinates: "40.7128,-74.0060",
  size: "100",
  size_unit: "acres",
  description: "A modern dairy farm with 200 cows",
  code: "SF1234",
  image: "farm_image_url",
  image_refference: "image_reference",
  created_by: {
    id: 1,
    username: "farmer_john",
    email: "john@example.com"
  },
  created_at: "2024-01-15T10:30:00Z",
  updated_at: "2024-01-15T10:30:00Z"
}
```

### Equipment Purchase Object
```javascript
{
  id: 1,
  farm: 1,
  farm_name: "Sunshine Dairy Farm",
  equipment_name: "Industrial Milking System",
  description: "Complete automated milking system with 20 stations",
  quantity: 1,
  unit_cost: "25000.00",
  total_cost: "25000.00",
  supplier: "Dairy Equipment Co.",
  supplier_contact: "+1234567890",
  purchase_date: "2024-01-15",
  delivery_date: "2024-02-01",
  warranty_expiry: "2027-01-15",
  payment_method: "bank_transfer",
  payment_status: "partial",
  due_date: "2024-02-15",
  payment_date: null,
  total_paid: "15000.00",
  pending_amount: "10000.00",
  transactions: [...],
  notes: "Installation scheduled for February 1st",
  created_by: 1,
  created_by_name: "John Doe",
  created_at: "2024-01-15T10:30:00Z",
  updated_at: "2024-01-15T10:30:00Z"
}
```

### Farm Statistics Object
```javascript
{
  total_income: "50000.00",
  total_expenses: "30000.00",
  net_income: "20000.00",
  total_equipment: 15,
  total_expense_records: 25,
  farm_name: "Sunshine Dairy Farm",
  farm_id: 1
}
```

### ExpenseCategory Object
```javascript
{
  id: 1,
  farm: 1,
  farm_name: "Sunshine Dairy Farm",
  name: "Maintenance",
  description: "Equipment maintenance and repairs",
  color: "#10B981",
  is_active: true,
  expense_count: 5,
  created_by: 1,
  created_by_name: "John Doe",
  created_at: "2024-01-15T10:30:00Z",
  updated_at: "2024-01-15T10:30:00Z"
}
```

---

## 12. ERROR HANDLING

### Global Error Handler
```javascript
const handleApiError = (error, context) => {
  console.error(`Error in ${context}:`, error);
  
  if (error.status === 401) {
    // Handle authentication error
    redirectToLogin();
  } else if (error.status === 400) {
    // Handle validation errors
    showValidationErrors(error.data);
  } else if (error.status === 404) {
    // Handle not found
    showNotFoundMessage();
  } else {
    // Handle general errors
    showErrorMessage('An unexpected error occurred. Please try again.');
  }
};
```

### Form Validation
```javascript
const validateEquipmentPurchase = (data) => {
  const errors = {};
  
  if (!data.equipment_name) {
    errors.equipment_name = 'Equipment name is required';
  }
  
  if (!data.unit_cost || data.unit_cost <= 0) {
    errors.unit_cost = 'Valid unit cost is required';
  }
  
  if (!data.purchase_date) {
    errors.purchase_date = 'Purchase date is required';
  }
  
  if (!data.due_date) {
    errors.due_date = 'Due date is required';
  }
  
  if (new Date(data.due_date) < new Date(data.purchase_date)) {
    errors.due_date = 'Due date cannot be before purchase date';
  }
  
  return errors;
};
```

---

## 13. STATE MANAGEMENT (Redux/Context)

### Equipment Purchase Actions
```javascript
// Actions
export const fetchEquipmentPurchases = (farmId) => async (dispatch) => {
  dispatch({ type: 'FETCH_PURCHASES_START' });
  try {
    const purchases = await getEquipmentPurchases(farmId);
    dispatch({ type: 'FETCH_PURCHASES_SUCCESS', payload: purchases });
  } catch (error) {
    dispatch({ type: 'FETCH_PURCHASES_ERROR', payload: error.message });
  }
};

export const createEquipmentPurchase = (farmId, purchaseData) => async (dispatch) => {
  dispatch({ type: 'CREATE_PURCHASE_START' });
  try {
    const newPurchase = await createEquipmentPurchase(farmId, purchaseData);
    dispatch({ type: 'CREATE_PURCHASE_SUCCESS', payload: newPurchase });
    return newPurchase;
  } catch (error) {
    dispatch({ type: 'CREATE_PURCHASE_ERROR', payload: error.message });
    throw error;
  }
};
```

---

## 14. BEST PRACTICES FOR FRONTEND

1. **Authentication**: Always include your authentication token in requests
2. **Farm Scoping**: All operations are farm-scoped - always include farm_id in URLs
3. **Error Handling**: Always implement proper error handling for API calls
4. **Loading States**: Show loading indicators during API operations
5. **Form Validation**: Validate data on both client and server side
6. **Optimistic Updates**: Update UI immediately, then sync with server
7. **Caching**: Cache frequently accessed data to reduce API calls
8. **Pagination**: Implement pagination for large datasets
9. **Real-time Updates**: Consider WebSocket connections for real-time data
10. **Mobile Responsiveness**: Ensure forms work well on mobile devices
11. **Accessibility**: Follow WCAG guidelines for accessibility
12. **Testing**: Write unit and integration tests for API interactions

---

## 15. COMMON PATTERNS

### CRUD Operations Pattern
```javascript
// Create
const create = async (farmId, data) => {
  const result = await apiCall(`create_endpoint/${farmId}`, {
    method: 'POST',
    body: JSON.stringify(data)
  });
  return result;
};

// Read
const getAll = async (farmId) => {
  return await apiCall(`get_endpoint/${farmId}`);
};

const getById = async (farmId, id) => {
  return await apiCall(`get_endpoint/${farmId}/${id}`);
};

// Update
const update = async (farmId, id, data) => {
  return await apiCall(`edit_endpoint/${farmId}/${id}`, {
    method: 'POST',
    body: JSON.stringify(data)
  });
};

// Delete
const remove = async (farmId, id) => {
  return await apiCall(`delete_endpoint/${farmId}/${id}`, {
    method: 'POST'
  });
};
```

### Farm-Scoped Hook Pattern
```javascript
const useFarmData = (farmId, endpoint) => {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchData = async () => {
      try {
        setLoading(true);
        const result = await apiCall(`${endpoint}/${farmId}`);
        setData(result);
      } catch (err) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    };

    if (farmId) {
      fetchData();
    }
  }, [farmId, endpoint]);

  return { data, loading, error };
};
```

This summary provides everything a frontend developer needs to integrate with the DairyDrive Farm API, including practical examples, error handling, and best practices for farm-scoped operations. 