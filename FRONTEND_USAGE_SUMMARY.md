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
const getTransactions = async () => {
  try {
    const transactions = await apiCall('get_transactions');
    return transactions;
  } catch (error) {
    console.error('Error fetching transactions:', error);
    throw error;
  }
};
```

### Create Transaction
```javascript
const createTransaction = async (transactionData) => {
  try {
    const newTransaction = await apiCall('create_transaction', {
      method: 'POST',
      body: JSON.stringify({
        farm: transactionData.farmId,
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

---

## 3. EQUIPMENT MANAGEMENT

### Get All Equipment
```javascript
const getEquipment = async () => {
  try {
    const equipment = await apiCall('get_equipment');
    return equipment;
  } catch (error) {
    console.error('Error fetching equipment:', error);
    throw error;
  }
};
```

### Create Equipment
```javascript
const createEquipment = async (equipmentData) => {
  try {
    const newEquipment = await apiCall('create_equipment', {
      method: 'POST',
      body: JSON.stringify({
        farm: equipmentData.farmId,
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

---

## 4. EQUIPMENT PURCHASE MANAGEMENT

### Get All Equipment Purchases
```javascript
const getEquipmentPurchases = async () => {
  try {
    const purchases = await apiCall('get_equipment_purchases');
    return purchases;
  } catch (error) {
    console.error('Error fetching equipment purchases:', error);
    throw error;
  }
};
```

### Create Equipment Purchase
```javascript
const createEquipmentPurchase = async (purchaseData) => {
  try {
    const newPurchase = await apiCall('create_equipment_purchase', {
      method: 'POST',
      body: JSON.stringify({
        farm: purchaseData.farmId,
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

### Link Transaction to Equipment Purchase
```javascript
const linkTransactionToPurchase = async (purchaseId, transactionId) => {
  try {
    const updatedPurchase = await apiCall(`add_equipment_purchase_transaction/${purchaseId}`, {
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
const getExpenses = async () => {
  try {
    const expenses = await apiCall('get_expenses');
    return expenses;
  } catch (error) {
    console.error('Error fetching expenses:', error);
    throw error;
  }
};
```

### Create Expense
```javascript
const createExpense = async (expenseData) => {
  try {
    const newExpense = await apiCall('create_expense', {
      method: 'POST',
      body: JSON.stringify({
        farm: expenseData.farmId,
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

---

## 6. REACT COMPONENT EXAMPLES

### Farm List Component
```jsx
import React, { useState, useEffect } from 'react';

const FarmList = () => {
  const [farms, setFarms] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchFarms = async () => {
      try {
        setLoading(true);
        const farmsData = await getFarms();
        setFarms(farmsData);
      } catch (err) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    };

    fetchFarms();
  }, []);

  if (loading) return <div>Loading farms...</div>;
  if (error) return <div>Error: {error}</div>;

  return (
    <div>
      <h2>My Farms</h2>
      {farms.map(farm => (
        <div key={farm.id} className="farm-card">
          <h3>{farm.name}</h3>
          <p>{farm.address}</p>
          <p>Size: {farm.size} {farm.size_unit}</p>
          <p>Code: {farm.code}</p>
        </div>
      ))}
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
      const newPurchase = await createEquipmentPurchase({
        farmId,
        ...formData
      });
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

## 7. DATA STRUCTURES

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

---

## 8. ERROR HANDLING

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

## 9. STATE MANAGEMENT (Redux/Context)

### Equipment Purchase Actions
```javascript
// Actions
export const fetchEquipmentPurchases = () => async (dispatch) => {
  dispatch({ type: 'FETCH_PURCHASES_START' });
  try {
    const purchases = await getEquipmentPurchases();
    dispatch({ type: 'FETCH_PURCHASES_SUCCESS', payload: purchases });
  } catch (error) {
    dispatch({ type: 'FETCH_PURCHASES_ERROR', payload: error.message });
  }
};

export const createEquipmentPurchase = (purchaseData) => async (dispatch) => {
  dispatch({ type: 'CREATE_PURCHASE_START' });
  try {
    const newPurchase = await createEquipmentPurchase(purchaseData);
    dispatch({ type: 'CREATE_PURCHASE_SUCCESS', payload: newPurchase });
    return newPurchase;
  } catch (error) {
    dispatch({ type: 'CREATE_PURCHASE_ERROR', payload: error.message });
    throw error;
  }
};
```

---

## 10. BEST PRACTICES FOR FRONTEND

1. **Error Handling**: Always implement proper error handling for API calls
2. **Loading States**: Show loading indicators during API operations
3. **Form Validation**: Validate data on both client and server side
4. **Optimistic Updates**: Update UI immediately, then sync with server
5. **Caching**: Cache frequently accessed data to reduce API calls
6. **Pagination**: Implement pagination for large datasets
7. **Real-time Updates**: Consider WebSocket connections for real-time data
8. **Mobile Responsiveness**: Ensure forms work well on mobile devices
9. **Accessibility**: Follow WCAG guidelines for accessibility
10. **Testing**: Write unit and integration tests for API interactions

---

## 11. COMMON PATTERNS

### CRUD Operations Pattern
```javascript
// Create
const create = async (data) => {
  const result = await apiCall('create_endpoint', {
    method: 'POST',
    body: JSON.stringify(data)
  });
  return result;
};

// Read
const getAll = async () => {
  return await apiCall('get_endpoint');
};

const getById = async (id) => {
  return await apiCall(`get_endpoint/${id}`);
};

// Update
const update = async (id, data) => {
  return await apiCall(`edit_endpoint/${id}`, {
    method: 'POST',
    body: JSON.stringify(data)
  });
};

// Delete
const remove = async (id) => {
  return await apiCall(`delete_endpoint/${id}`, {
    method: 'POST'
  });
};
```

This summary provides everything a frontend developer needs to integrate with the DairyDrive Farm API, including practical examples, error handling, and best practices. 