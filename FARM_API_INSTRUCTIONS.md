# DairyDrive Farm Management API Instructions

## Overview
The DairyDrive Farm Management API provides comprehensive endpoints for managing farms, transactions, equipment, equipment purchases, and expenses. All endpoints require authentication and are designed to work with user-specific data. All endpoints are now farm-scoped, requiring a farm_id parameter.

## Base URL
```
/api/farms/
```

## Authentication
All endpoints require authentication. Include your authentication token in the request headers:
```
Authorization: Token your_auth_token_here
```

## URL Pattern
All endpoints follow the pattern: `/api/farms/{endpoint}/{farm_id}` or `/api/farms/{endpoint}/{farm_id}/{id}`

---

## 1. FARM MANAGEMENT ENDPOINTS

### 1.1 Get All Farms
**Endpoint:** `GET /api/farms/get_farms`

**Description:** Retrieve all farms for the authenticated user.

**Response:**
```json
[
  {
    "id": 1,
    "name": "Sunshine Dairy Farm",
    "address": "123 Farm Road, Dairy County",
    "phone": "+1234567890",
    "coordinates": "40.7128,-74.0060",
    "size": "100",
    "size_unit": "acres",
    "description": "A modern dairy farm with 200 cows",
    "code": "SF1234",
    "image": "farm_image_url",
    "image_refference": "image_reference",
    "created_by": {
      "id": 1,
      "username": "farmer_john",
      "email": "john@example.com"
    },
    "created_at": "2024-01-15T10:30:00Z",
    "updated_at": "2024-01-15T10:30:00Z"
  }
]
```

### 1.2 Create Farm
**Endpoint:** `POST /api/farms/create_farm`

**Description:** Create a new farm. The system automatically generates a farm code and assigns the current user as creator.

**Request Body:**
```json
{
  "name": "Sunshine Dairy Farm",
  "address": "123 Farm Road, Dairy County",
  "phone": "+1234567890",
  "coordinates": "40.7128,-74.0060",
  "size": "100",
  "size_unit": "acres",
  "description": "A modern dairy farm with 200 cows",
  "image": "farm_image_url",
  "image_refference": "image_reference"
}
```

**Required Fields:**
- `name` (string, max 255 chars, unique)
- `address` (string, max 255 chars)

**Optional Fields:**
- `phone` (string, max 50 chars)
- `coordinates` (string, max 255 chars)
- `size` (string, max 255 chars)
- `size_unit` (string, max 255 chars)
- `description` (string, max 255 chars)
- `image` (string, max 255 chars)
- `image_refference` (string, max 255 chars)

**Response:** Returns the created farm object with auto-generated `code` and `created_by` fields.

### 1.3 Get Specific Farm
**Endpoint:** `GET /api/farms/get_farm/{farm_id}`

**Description:** Retrieve a specific farm by ID.

**Response:** Returns the farm object.

### 1.4 Edit Farm
**Endpoint:** `POST /api/farms/edit_farm/{farm_id}`

**Description:** Update an existing farm. All fields are optional for partial updates.

**Request Body:** (Same structure as create_farm, all fields optional)
```json
{
  "name": "Updated Farm Name",
  "address": "456 New Farm Road",
  "phone": "+1987654321"
}
```

**Response:** Returns the updated farm object.

### 1.5 Delete Farm
**Endpoint:** `POST /api/farms/delete_farm/{farm_id}`

**Description:** Delete a farm by ID.

**Response:**
```json
{
  "message": "Farm id:1 deleted successfully"
}
```

---

## 2. TRANSACTION MANAGEMENT ENDPOINTS

### 2.1 Get All Transactions
**Endpoint:** `GET /api/farms/get_transactions/{farm_id}`

**Description:** Retrieve all transactions for a specific farm.

**Response:**
```json
[
  {
    "id": 1,
    "farm": 1,
    "transaction_type": "incoming",
    "payment_method": "bank_transfer",
    "amount": "5000.00",
    "transaction_date": "2024-01-15T10:30:00Z",
    "transaction_code": "TXN123456",
    "description": "Milk sales payment",
    "created_by": 1,
    "created_at": "2024-01-15T10:30:00Z",
    "updated_at": "2024-01-15T10:30:00Z"
  }
]
```

### 2.2 Create Transaction
**Endpoint:** `POST /api/farms/add_transaction/{farm_id}`

**Description:** Create a new transaction for a specific farm.

**Request Body:**
```json
{
  "transaction_type": "incoming",
  "payment_method": "bank_transfer",
  "amount": "5000.00",
  "transaction_date": "2024-01-15T10:30:00Z",
  "description": "Milk sales payment"
}
```

**Required Fields:**
- `transaction_type` (string - "incoming" or "outgoing")
- `payment_method` (string - "cash", "bank_transfer", "mobile_money", "cheque", "other")
- `amount` (decimal - max 10 digits, 2 decimal places)
- `transaction_date` (datetime)

**Optional Fields:**
- `description` (text)

**Transaction Types:**
- `incoming`: Money received
- `outgoing`: Money spent

**Payment Methods:**
- `cash`: Cash payment
- `bank_transfer`: Bank transfer
- `mobile_money`: Mobile money transfer
- `cheque`: Check payment
- `other`: Other payment methods

### 2.3 Edit Transaction
**Endpoint:** `POST /api/farms/edit_transaction/{farm_id}/{pk}`

**Description:** Update an existing transaction.

**Request Body:** (Same structure as create_transaction, all fields optional)

### 2.4 Delete Transaction
**Endpoint:** `POST /api/farms/delete_transaction/{farm_id}/{pk}`

**Description:** Delete a transaction by ID.

### 2.5 Get Transaction Detail
**Endpoint:** `GET /api/farms/get_transaction/{farm_id}/{pk}`

**Description:** Retrieve a specific transaction by ID.

---

## 3. EQUIPMENT MANAGEMENT ENDPOINTS

### 3.1 Get All Equipment
**Endpoint:** `GET /api/farms/get_equipment/{farm_id}`

**Description:** Retrieve all equipment for a specific farm.

**Response:**
```json
[
  {
    "id": 1,
    "farm": 1,
    "farm_name": "Sunshine Dairy Farm",
    "name": "Milking Machine",
    "description": "Automated milking system",
    "quantity": 2,
    "cost": "15000.00",
    "condition": "good",
    "purchase_date": "2023-06-15",
    "last_maintenance_date": "2024-01-01",
    "next_maintenance_date": "2024-07-01",
    "created_by": 1,
    "created_by_name": "John Doe",
    "created_at": "2024-01-15T10:30:00Z",
    "updated_at": "2024-01-15T10:30:00Z"
  }
]
```

### 3.2 Create Equipment
**Endpoint:** `POST /api/farms/add_equipment/{farm_id}`

**Description:** Create new equipment for a specific farm.

**Request Body:**
```json
{
  "name": "Milking Machine",
  "description": "Automated milking system",
  "quantity": 2,
  "cost": "15000.00",
  "condition": "good",
  "purchase_date": "2023-06-15",
  "last_maintenance_date": "2024-01-01",
  "next_maintenance_date": "2024-07-01"
}
```

**Required Fields:**
- `name` (string, max 255 chars)
- `cost` (decimal - max 10 digits, 2 decimal places)

**Optional Fields:**
- `description` (text)
- `quantity` (positive integer, default: 1)
- `condition` (string - "new", "good", "fair", "poor", "maintenance", default: "good")
- `purchase_date` (date)
- `last_maintenance_date` (date)
- `next_maintenance_date` (date)

**Equipment Conditions:**
- `new`: Brand new equipment
- `good`: Good working condition
- `fair`: Fair condition, some wear
- `poor`: Poor condition, needs replacement
- `maintenance`: Needs maintenance

### 3.3 Edit Equipment
**Endpoint:** `POST /api/farms/edit_equipment/{farm_id}/{pk}`

**Description:** Update existing equipment.

### 3.4 Delete Equipment
**Endpoint:** `POST /api/farms/delete_equipment/{farm_id}/{pk}`

**Description:** Delete equipment by ID.

### 3.5 Get Equipment Detail
**Endpoint:** `GET /api/farms/get_equipment_item/{farm_id}/{pk}`

**Description:** Retrieve specific equipment details.

---

## 4. EQUIPMENT PURCHASE MANAGEMENT ENDPOINTS

### 4.1 Get All Equipment Purchases
**Endpoint:** `GET /api/farms/get_equipment_purchases/{farm_id}`

**Description:** Retrieve all equipment purchases for a specific farm.

**Response:**
```json
[
  {
    "id": 1,
    "farm": 1,
    "farm_name": "Sunshine Dairy Farm",
    "equipment_name": "Industrial Milking System",
    "description": "Complete automated milking system with 20 stations",
    "quantity": 1,
    "unit_cost": "25000.00",
    "total_cost": "25000.00",
    "supplier": "Dairy Equipment Co.",
    "supplier_contact": "+1234567890",
    "purchase_date": "2024-01-15",
    "delivery_date": "2024-02-01",
    "warranty_expiry": "2027-01-15",
    "payment_method": "bank_transfer",
    "payment_status": "partial",
    "due_date": "2024-02-15",
    "payment_date": null,
    "total_paid": "15000.00",
    "pending_amount": "10000.00",
    "transactions": [...],
    "notes": "Installation scheduled for February 1st",
    "created_by": 1,
    "created_by_name": "John Doe",
    "created_at": "2024-01-15T10:30:00Z",
    "updated_at": "2024-01-15T10:30:00Z"
  }
]
```

### 4.2 Create Equipment Purchase
**Endpoint:** `POST /api/farms/add_equipment_purchase/{farm_id}`

**Description:** Create a new equipment purchase for a specific farm.

**Request Body:**
```json
{
  "equipment_name": "Industrial Milking System",
  "description": "Complete automated milking system with 20 stations",
  "quantity": 1,
  "unit_cost": "25000.00",
  "supplier": "Dairy Equipment Co.",
  "supplier_contact": "+1234567890",
  "purchase_date": "2024-01-15",
  "delivery_date": "2024-02-01",
  "warranty_expiry": "2027-01-15",
  "payment_method": "bank_transfer",
  "due_date": "2024-02-15",
  "notes": "Installation scheduled for February 1st"
}
```

**Required Fields:**
- `equipment_name` (string, max 255 chars)
- `description` (text)
- `quantity` (positive integer, default: 1)
- `unit_cost` (decimal - max 10 digits, 2 decimal places)
- `purchase_date` (date)
- `due_date` (date)

**Optional Fields:**
- `supplier` (string, max 255 chars)
- `supplier_contact` (string, max 255 chars)
- `delivery_date` (date)
- `warranty_expiry` (date)
- `payment_method` (string - "cash", "bank_transfer", "mobile_money", "cheque", "credit", "lease", "other", default: "bank_transfer")
- `notes` (text)

**Payment Methods:**
- `cash`: Cash payment
- `bank_transfer`: Bank transfer
- `mobile_money`: Mobile money transfer
- `cheque`: Check payment
- `credit`: Credit payment
- `lease`: Lease payment
- `other`: Other payment methods

**Payment Status (Auto-calculated):**
- `pending`: No payments made
- `partial`: Partial payment made
- `paid`: Fully paid
- `overdue`: Past due date with no payment
- `cancelled`: Purchase cancelled

### 4.3 Edit Equipment Purchase
**Endpoint:** `POST /api/farms/edit_equipment_purchase/{farm_id}/{pk}`

**Description:** Update existing equipment purchase.

### 4.4 Delete Equipment Purchase
**Endpoint:** `POST /api/farms/delete_equipment_purchase/{farm_id}/{pk}`

**Description:** Delete equipment purchase by ID.

### 4.5 Get Equipment Purchase Detail
**Endpoint:** `GET /api/farms/get_equipment_purchase/{farm_id}/{pk}`

**Description:** Retrieve specific equipment purchase details.

### 4.6 Add Transaction to Equipment Purchase
**Endpoint:** `POST /api/farms/add_equipment_purchase_transaction/{farm_id}/{pk}`

**Description:** Link a transaction to an equipment purchase for payment tracking.

**Request Body:**
```json
{
  "transaction_id": 1
}
```

**Required Fields:**
- `transaction_id` (integer - existing transaction ID)

**Note:** The transaction must be from the same farm as the equipment purchase.

### 4.7 Remove Transaction from Equipment Purchase
**Endpoint:** `POST /api/farms/remove_equipment_purchase_transaction/{farm_id}/{pk}`

**Description:** Unlink a transaction from an equipment purchase.

**Request Body:**
```json
{
  "transaction_id": 1
}
```

---

## 5. EXPENSE MANAGEMENT ENDPOINTS

### 5.1 Get All Expenses
**Endpoint:** `GET /api/farms/get_expenses/{farm_id}`

**Description:** Retrieve all expenses for a specific farm.

**Response:**
```json
[
  {
    "id": 1,
    "farm": 1,
    "farm_name": "Sunshine Dairy Farm",
    "category": "maintenance",
    "description": "Equipment maintenance and repairs",
    "amount": "2500.00",
    "payment_status": "partial",
    "due_date": "2024-02-15",
    "payment_date": null,
    "total_paid": "1500.00",
    "pending_amount": "1000.00",
    "transactions": [...],
    "created_by": 1,
    "created_by_name": "John Doe",
    "created_at": "2024-01-15T10:30:00Z",
    "updated_at": "2024-01-15T10:30:00Z"
  }
]
```

### 5.2 Create Expense
**Endpoint:** `POST /api/farms/add_expense/{farm_id}`

**Description:** Create a new expense for a specific farm.

**Request Body:**
```json
{
  "category": "maintenance",
  "description": "Equipment maintenance and repairs",
  "amount": "2500.00",
  "due_date": "2024-02-15"
}
```

**Required Fields:**
- `category` (string - expense category)
- `description` (text)
- `amount` (decimal - max 10 digits, 2 decimal places)
- `due_date` (date)

**Expense Categories:**
- `labor`: Labor costs
- `utilities`: Utility bills
- `maintenance`: Maintenance and repairs
- `supplies`: Farm supplies
- `equipment`: Equipment purchases
- `transportation`: Transportation costs
- `marketing`: Marketing expenses
- `insurance`: Insurance premiums
- `taxes`: Tax payments
- `other`: Other expenses

**Payment Status (Auto-calculated):**
- `pending`: No payments made
- `partial`: Partial payment made
- `paid`: Fully paid
- `overdue`: Past due date with no payment

### 5.3 Edit Expense
**Endpoint:** `POST /api/farms/edit_expense/{farm_id}/{pk}`

**Description:** Update existing expense.

### 5.4 Delete Expense
**Endpoint:** `POST /api/farms/delete_expense/{farm_id}/{pk}`

**Description:** Delete expense by ID.

### 5.5 Get Expense Detail
**Endpoint:** `GET /api/farms/get_expense/{farm_id}/{pk}`

**Description:** Retrieve specific expense details.

### 5.6 Add Transaction to Expense
**Endpoint:** `POST /api/farms/add_expense_transaction/{farm_id}/{pk}`

**Description:** Link a transaction to an expense for payment tracking.

**Request Body:**
```json
{
  "transaction_id": 1
}
```

**Required Fields:**
- `transaction_id` (integer - existing transaction ID)

**Note:** The transaction must be from the same farm as the expense.

### 5.7 Remove Transaction from Expense
**Endpoint:** `POST /api/farms/remove_expense_transaction/{farm_id}/{pk}`

**Description:** Unlink a transaction from an expense.

**Request Body:**
```json
{
  "transaction_id": 1
}
```

---

## 6. EXPENSE CATEGORIES ENDPOINTS

### 6.1 Get Expense Categories
**Endpoint:** `GET /api/farms/get_expense_categories/{farm_id}`

**Description:** Get available expense categories for a specific farm.

**Response:**
```json
[
  {"value": "labor", "label": "Labor"},
  {"value": "utilities", "label": "Utilities"},
  {"value": "maintenance", "label": "Maintenance"},
  {"value": "supplies", "label": "Supplies"},
  {"value": "equipment", "label": "Equipment"},
  {"value": "transportation", "label": "Transportation"},
  {"value": "marketing", "label": "Marketing"},
  {"value": "insurance", "label": "Insurance"},
  {"value": "taxes", "label": "Taxes"},
  {"value": "other", "label": "Other"}
]
```

---

## 7. FARM STATISTICS ENDPOINTS

### 7.1 Get Farm Statistics
**Endpoint:** `GET /api/farms/get_farm_statistics/{farm_id}`

**Description:** Get comprehensive statistics for a specific farm.

**Response:**
```json
{
  "total_income": "50000.00",
  "total_expenses": "30000.00",
  "net_income": "20000.00",
  "total_equipment": 15,
  "total_expense_records": 25,
  "farm_name": "Sunshine Dairy Farm",
  "farm_id": 1
}
```

### 7.2 Get Farm Income
**Endpoint:** `GET /api/farms/get_farm_income/{farm_id}`

**Description:** Get all income transactions for a specific farm.

**Response:** Returns array of income transactions.

### 7.3 Get Farm Expenses
**Endpoint:** `GET /api/farms/get_farm_expenses/{farm_id}`

**Description:** Get all expense transactions for a specific farm.

**Response:** Returns array of expense transactions.

---

## 8. FARM USERS ENDPOINTS

### 8.1 Get Farm Users
**Endpoint:** `GET /api/farms/get_farm_users/{farm_id}`

**Description:** Get users associated with a specific farm.

**Response:**
```json
[
  {
    "id": 1,
    "username": "farmer_john",
    "email": "john@example.com",
    "role": "owner"
  }
]
```

### 8.2 Add Farm User
**Endpoint:** `POST /api/farms/add_farm_user/{farm_id}`

**Description:** Add a user to a specific farm (placeholder for future implementation).

### 8.3 Remove Farm User
**Endpoint:** `POST /api/farms/remove_farm_user/{farm_id}/{user_id}`

**Description:** Remove a user from a specific farm (placeholder for future implementation).

---

## 9. FARM SETTINGS ENDPOINTS

### 9.1 Get Farm Settings
**Endpoint:** `GET /api/farms/get_farm_settings/{farm_id}`

**Description:** Get settings for a specific farm.

**Response:**
```json
{
  "farm_id": 1,
  "name": "Sunshine Dairy Farm",
  "address": "123 Farm Road, Dairy County",
  "phone": "+1234567890",
  "coordinates": "40.7128,-74.0060",
  "size": "100",
  "size_unit": "acres",
  "description": "A modern dairy farm with 200 cows",
  "code": "SF1234",
  "image": "farm_image_url",
  "image_reference": "image_reference"
}
```

### 9.2 Update Farm Settings
**Endpoint:** `POST /api/farms/update_farm_settings/{farm_id}`

**Description:** Update settings for a specific farm.

**Request Body:** (Same structure as farm fields, all fields optional)

---

## 10. VIEWSET ENDPOINTS (RESTful)

### 10.1 Farm ViewSet
**Base URL:** `/api/farms/farms/`

**Available Actions:**
- `GET /api/farms/farms/` - List all farms
- `POST /api/farms/farms/` - Create farm
- `GET /api/farms/farms/{id}/` - Get specific farm
- `PUT /api/farms/farms/{id}/` - Update farm
- `PATCH /api/farms/farms/{id}/` - Partial update farm
- `DELETE /api/farms/farms/{id}/` - Delete farm

### 10.2 Transaction ViewSet
**Base URL:** `/api/farms/transactions/`

**Available Actions:**
- `GET /api/farms/transactions/` - List all transactions
- `POST /api/farms/transactions/` - Create transaction
- `GET /api/farms/transactions/{id}/` - Get specific transaction
- `PUT /api/farms/transactions/{id}/` - Update transaction
- `PATCH /api/farms/transactions/{id}/` - Partial update transaction
- `DELETE /api/farms/transactions/{id}/` - Delete transaction

---

## 11. ERROR RESPONSES

### Common Error Codes:
- `400 Bad Request`: Invalid data provided
- `401 Unauthorized`: Authentication required
- `403 Forbidden`: Insufficient permissions
- `404 Not Found`: Resource not found
- `500 Internal Server Error`: Server error

### Error Response Format:
```json
{
  "message": "Error description",
  "field_name": ["Specific field error"]
}
```

---

## 12. USAGE EXAMPLES

### Example 1: Complete Farm Setup
```bash
# 1. Create a farm
curl -X POST /api/farms/create_farm \
  -H "Authorization: Token your_token" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Green Valley Dairy",
    "address": "456 Valley Road, Farm County",
    "phone": "+1234567890",
    "size": "150",
    "size_unit": "acres",
    "description": "Organic dairy farm"
  }'

# 2. Add equipment
curl -X POST /api/farms/add_equipment/1 \
  -H "Authorization: Token your_token" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Milk Cooler",
    "description": "Industrial milk cooling system",
    "cost": "8000.00",
    "condition": "new"
  }'

# 3. Record income
curl -X POST /api/farms/add_transaction/1 \
  -H "Authorization: Token your_token" \
  -H "Content-Type: application/json" \
  -d '{
    "transaction_type": "incoming",
    "payment_method": "bank_transfer",
    "amount": "12000.00",
    "transaction_date": "2024-01-15T10:30:00Z",
    "description": "Monthly milk sales"
  }'
```

### Example 2: Equipment Purchase Workflow
```bash
# 1. Create equipment purchase
curl -X POST /api/farms/add_equipment_purchase/1 \
  -H "Authorization: Token your_token" \
  -H "Content-Type: application/json" \
  -d '{
    "equipment_name": "Automated Feed System",
    "description": "Computerized feed distribution system",
    "quantity": 1,
    "unit_cost": "18000.00",
    "supplier": "FarmTech Solutions",
    "supplier_contact": "+1987654321",
    "purchase_date": "2024-01-20",
    "delivery_date": "2024-02-10",
    "warranty_expiry": "2027-01-20",
    "payment_method": "credit",
    "due_date": "2024-03-20",
    "notes": "Installation included in price"
  }'

# 2. Make down payment transaction
curl -X POST /api/farms/add_transaction/1 \
  -H "Authorization: Token your_token" \
  -H "Content-Type: application/json" \
  -d '{
    "transaction_type": "outgoing",
    "payment_method": "bank_transfer",
    "amount": "9000.00",
    "transaction_date": "2024-01-20T14:00:00Z",
    "description": "Down payment for automated feed system"
  }'

# 3. Link transaction to equipment purchase
curl -X POST /api/farms/add_equipment_purchase_transaction/1/1 \
  -H "Authorization: Token your_token" \
  -H "Content-Type: application/json" \
  -d '{
    "transaction_id": 2
  }'
```

### Example 3: Expense Management
```bash
# 1. Create expense
curl -X POST /api/farms/add_expense/1 \
  -H "Authorization: Token your_token" \
  -H "Content-Type: application/json" \
  -d '{
    "category": "utilities",
    "description": "Electricity bill for January",
    "amount": "500.00",
    "due_date": "2024-02-01"
  }'

# 2. Make payment transaction
curl -X POST /api/farms/add_transaction/1 \
  -H "Authorization: Token your_token" \
  -H "Content-Type: application/json" \
  -d '{
    "transaction_type": "outgoing",
    "payment_method": "bank_transfer",
    "amount": "500.00",
    "transaction_date": "2024-01-25T14:00:00Z",
    "description": "Electricity bill payment"
  }'

# 3. Link transaction to expense
curl -X POST /api/farms/add_expense_transaction/1/1 \
  -H "Authorization: Token your_token" \
  -H "Content-Type: application/json" \
  -d '{
    "transaction_id": 2
  }'
```

### Example 4: Get Farm Statistics
```bash
# Get comprehensive farm statistics
curl -X GET /api/farms/get_farm_statistics/1 \
  -H "Authorization: Token your_token"

# Get farm income
curl -X GET /api/farms/get_farm_income/1 \
  -H "Authorization: Token your_token"

# Get farm expenses
curl -X GET /api/farms/get_farm_expenses/1 \
  -H "Authorization: Token your_token"
```

---

## 13. BEST PRACTICES

1. **Authentication**: Always include your authentication token in requests
2. **Farm Scoping**: All operations are farm-scoped - always include farm_id in URLs
3. **Data Validation**: Ensure all required fields are provided
4. **Error Handling**: Check response status codes and handle errors appropriately
5. **Date Formats**: Use ISO 8601 format for dates (YYYY-MM-DDTHH:MM:SSZ)
6. **Decimal Precision**: Use 2 decimal places for monetary amounts
7. **Payment Tracking**: Use expense-transaction linking for accurate payment tracking
8. **Equipment Purchases**: Track large equipment purchases separately from regular expenses
9. **Warranty Management**: Keep track of warranty expiry dates for equipment purchases
10. **Statistics**: Use farm statistics endpoints for dashboard and reporting features

---

## 14. RATE LIMITING

The API implements rate limiting to ensure fair usage. If you exceed the rate limit, you'll receive a `429 Too Many Requests` response.

---

## 15. SUPPORT

For technical support or questions about the API, please contact the development team or refer to the API documentation. 