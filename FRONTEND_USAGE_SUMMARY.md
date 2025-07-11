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

---

## 7. FARM STATISTICS

### Get Farm Statistics
```javascript
const getFarmStatistics = async (farmId) => {
  try {
    const statistics = await apiCall(`get_farm_statistics/${farmId}`);
    return statistics;
  } catch (error) {
    console.error('Error fetching farm statistics:', error);
    throw error;
  }
};
```

### Get Farm Income
```javascript
const getFarmIncome = async (farmId) => {
  try {
    const income = await apiCall(`get_farm_income/${farmId}`);
    return income;
  } catch (error) {
    console.error('Error fetching farm income:', error);
    throw error;
  }
};
```

### Get Farm Expenses
```javascript
const getFarmExpenses = async (farmId) => {
  try {
    const expenses = await apiCall(`get_farm_expenses/${farmId}`);
    return expenses;
  } catch (error) {
    console.error('Error fetching farm expenses:', error);
    throw error;
  }
};
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