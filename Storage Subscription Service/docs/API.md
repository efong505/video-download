# API Documentation

Complete API reference for CloudVault Storage Subscription Service.

## Base URL

```
https://YOUR_API_ID.execute-api.us-east-1.amazonaws.com/prod
```

## Authentication

All protected endpoints require a JWT token in the Authorization header:

```
Authorization: Bearer YOUR_JWT_TOKEN
```

Tokens expire after 30 days.

---

## Authentication API

### Register User

Create a new user account.

**Endpoint**: `POST /auth`

**Request Body**:
```json
{
    "action": "register",
    "name": "John Doe",
    "email": "john@example.com",
    "password": "password123"
}
```

**Response** (200 OK):
```json
{
    "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "userId": "a1b2c3d4e5f6g7h8",
    "email": "john@example.com",
    "name": "John Doe",
    "subscriptionTier": "free"
}
```

**Error Responses**:
- `400`: Missing required fields
- `400`: Email already registered

---

### Login User

Authenticate existing user.

**Endpoint**: `POST /auth`

**Request Body**:
```json
{
    "action": "login",
    "email": "john@example.com",
    "password": "password123"
}
```

**Response** (200 OK):
```json
{
    "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "userId": "a1b2c3d4e5f6g7h8",
    "email": "john@example.com",
    "name": "John Doe",
    "subscriptionTier": "free",
    "storageQuota": 1073741824,
    "storageUsed": 0
}
```

**Error Responses**:
- `400`: Missing email or password
- `401`: Invalid credentials

---

### Verify Token

Verify JWT token validity.

**Endpoint**: `POST /auth`

**Headers**:
```
Authorization: Bearer YOUR_JWT_TOKEN
```

**Request Body**:
```json
{
    "action": "verify"
}
```

**Response** (200 OK):
```json
{
    "valid": true,
    "userId": "a1b2c3d4e5f6g7h8"
}
```

**Error Responses**:
- `401`: No token provided
- `401`: Token expired
- `401`: Invalid token

---

## Storage API

### List Files

Get all files for authenticated user.

**Endpoint**: `GET /storage`

**Headers**:
```
Authorization: Bearer YOUR_JWT_TOKEN
```

**Response** (200 OK):
```json
{
    "files": [
        {
            "fileName": "document.pdf",
            "fileSize": 1048576,
            "lastModified": "2024-01-15T10:30:00.000Z"
        },
        {
            "fileName": "image.jpg",
            "fileSize": 524288,
            "lastModified": "2024-01-14T15:20:00.000Z"
        }
    ],
    "count": 2
}
```

---

### Upload File

Upload a new file.

**Endpoint**: `POST /storage`

**Headers**:
```
Authorization: Bearer YOUR_JWT_TOKEN
Content-Type: application/json
```

**Request Body**:
```json
{
    "fileName": "document.pdf",
    "fileSize": 1048576,
    "fileContent": "BASE64_ENCODED_FILE_CONTENT",
    "fileType": "application/pdf"
}
```

**Response** (200 OK):
```json
{
    "message": "File uploaded successfully",
    "fileName": "document.pdf",
    "fileSize": 1048576,
    "storageUsed": 1048576
}
```

**Error Responses**:
- `400`: Missing fileName or fileContent
- `403`: Storage quota exceeded
- `401`: Invalid token

---

### Download File

Get presigned URL to download file.

**Endpoint**: `GET /storage?fileName=document.pdf`

**Headers**:
```
Authorization: Bearer YOUR_JWT_TOKEN
```

**Response** (200 OK):
```json
{
    "downloadUrl": "https://s3.amazonaws.com/bucket/path?signature=...",
    "fileName": "document.pdf"
}
```

**Error Responses**:
- `404`: File not found
- `401`: Invalid token

---

### Delete File

Delete a file.

**Endpoint**: `DELETE /storage?fileName=document.pdf`

**Headers**:
```
Authorization: Bearer YOUR_JWT_TOKEN
```

**Response** (200 OK):
```json
{
    "message": "File deleted successfully",
    "fileName": "document.pdf"
}
```

**Error Responses**:
- `400`: Missing fileName parameter
- `404`: File not found
- `401`: Invalid token

---

## Subscription API

### Get Subscription Status

Get current subscription details.

**Endpoint**: `GET /subscription?action=get_status`

**Headers**:
```
Authorization: Bearer YOUR_JWT_TOKEN
```

**Response** (200 OK):
```json
{
    "tier": "pro",
    "status": "active",
    "storageQuota": 107374182400,
    "storageUsed": 5368709120,
    "storagePercent": 5.0
}
```

---

### Create Checkout Session

Create Stripe checkout session for subscription upgrade.

**Endpoint**: `POST /subscription`

**Headers**:
```
Authorization: Bearer YOUR_JWT_TOKEN
Content-Type: application/json
```

**Request Body**:
```json
{
    "action": "create_checkout",
    "tier": "pro",
    "successUrl": "https://yourdomain.com/success",
    "cancelUrl": "https://yourdomain.com/cancel"
}
```

**Response** (200 OK):
```json
{
    "sessionId": "cs_test_a1b2c3d4e5f6g7h8",
    "url": "https://checkout.stripe.com/pay/cs_test_..."
}
```

**Error Responses**:
- `400`: Invalid tier
- `401`: Invalid token

---

### Cancel Subscription

Cancel active subscription.

**Endpoint**: `POST /subscription`

**Headers**:
```
Authorization: Bearer YOUR_JWT_TOKEN
Content-Type: application/json
```

**Request Body**:
```json
{
    "action": "cancel"
}
```

**Response** (200 OK):
```json
{
    "message": "Subscription cancelled successfully"
}
```

**Error Responses**:
- `400`: No active subscription
- `401`: Invalid token

---

### Stripe Webhook

Handle Stripe webhook events (internal use).

**Endpoint**: `POST /subscription`

**Headers**:
```
Stripe-Signature: WEBHOOK_SIGNATURE
```

**Request Body**: Stripe event payload

**Response** (200 OK):
```json
{
    "received": true
}
```

---

## Admin API

All admin endpoints require authentication with an admin email.

### Get All Users

List all users in the system.

**Endpoint**: `GET /admin/users`

**Headers**:
```
Authorization: Bearer ADMIN_JWT_TOKEN
```

**Response** (200 OK):
```json
{
    "users": [
        {
            "email": "john@example.com",
            "userId": "a1b2c3d4e5f6g7h8",
            "name": "John Doe",
            "subscriptionTier": "pro",
            "storageUsed": 5368709120,
            "storageQuota": 107374182400,
            "subscriptionStatus": "active",
            "createdAt": "2024-01-01T00:00:00.000Z"
        }
    ],
    "count": 1
}
```

**Error Responses**:
- `401`: Invalid token
- `403`: Admin access required

---

### Delete User

Delete a user account.

**Endpoint**: `DELETE /admin/users?email=john@example.com`

**Headers**:
```
Authorization: Bearer ADMIN_JWT_TOKEN
```

**Response** (200 OK):
```json
{
    "message": "User deleted successfully"
}
```

**Error Responses**:
- `400`: Missing email parameter
- `401`: Invalid token
- `403`: Admin access required

---

### Update User

Update user subscription details.

**Endpoint**: `PUT /admin/users`

**Headers**:
```
Authorization: Bearer ADMIN_JWT_TOKEN
Content-Type: application/json
```

**Request Body**:
```json
{
    "email": "john@example.com",
    "updates": {
        "subscriptionTier": "business",
        "storageQuota": 1099511627776,
        "subscriptionStatus": "active"
    }
}
```

**Response** (200 OK):
```json
{
    "message": "User updated successfully"
}
```

**Error Responses**:
- `400`: Missing email
- `401`: Invalid token
- `403`: Admin access required

---

### Get Statistics

Get platform statistics.

**Endpoint**: `GET /admin/stats`

**Headers**:
```
Authorization: Bearer ADMIN_JWT_TOKEN
```

**Response** (200 OK):
```json
{
    "totalUsers": 150,
    "totalStorageUsed": 536870912000,
    "totalStorageUsedGB": 500.0,
    "totalFiles": 1250,
    "tierDistribution": {
        "free": 100,
        "basic": 30,
        "pro": 15,
        "business": 5
    },
    "revenue": 1050
}
```

**Error Responses**:
- `401`: Invalid token
- `403`: Admin access required

---

## Error Responses

All endpoints may return these common errors:

### 400 Bad Request
```json
{
    "error": "Description of what went wrong"
}
```

### 401 Unauthorized
```json
{
    "error": "Invalid token" | "No token provided" | "Token expired"
}
```

### 403 Forbidden
```json
{
    "error": "Admin access required" | "Storage quota exceeded"
}
```

### 404 Not Found
```json
{
    "error": "File not found" | "User not found"
}
```

### 500 Internal Server Error
```json
{
    "error": "Internal server error description"
}
```

---

## Rate Limits

- **Authentication**: 10 requests per minute per IP
- **File Upload**: 20 requests per minute per user
- **File Download**: 100 requests per minute per user
- **Admin API**: 60 requests per minute per admin

Rate limits are enforced at the API Gateway level.

---

## CORS Configuration

All endpoints support CORS with:
- **Allowed Origins**: `*` (configure for production)
- **Allowed Methods**: GET, POST, PUT, DELETE, OPTIONS
- **Allowed Headers**: Content-Type, Authorization, Stripe-Signature

---

## Testing

### Using cURL

**Register**:
```bash
curl -X POST https://API_URL/prod/auth \
  -H "Content-Type: application/json" \
  -d '{"action":"register","name":"Test User","email":"test@example.com","password":"password123"}'
```

**Login**:
```bash
curl -X POST https://API_URL/prod/auth \
  -H "Content-Type: application/json" \
  -d '{"action":"login","email":"test@example.com","password":"password123"}'
```

**List Files**:
```bash
curl -X GET https://API_URL/prod/storage \
  -H "Authorization: Bearer YOUR_TOKEN"
```

### Using Postman

1. Import collection from `postman_collection.json`
2. Set environment variable `API_URL`
3. Set environment variable `TOKEN` after login
4. Run requests

---

## Webhooks

### Stripe Webhooks

Configure in Stripe Dashboard:

**URL**: `https://API_URL/prod/subscription`

**Events**:
- `checkout.session.completed` - Subscription created
- `customer.subscription.deleted` - Subscription cancelled
- `customer.subscription.updated` - Subscription changed

**Verification**: Webhook signature verified using Stripe library

---

## SDK Examples

### JavaScript

```javascript
// Register
const response = await fetch(`${API_URL}/auth`, {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({
        action: 'register',
        name: 'John Doe',
        email: 'john@example.com',
        password: 'password123'
    })
});
const data = await response.json();
localStorage.setItem('token', data.token);

// Upload File
const file = document.getElementById('fileInput').files[0];
const reader = new FileReader();
reader.onload = async (e) => {
    const base64 = e.target.result.split(',')[1];
    await fetch(`${API_URL}/storage`, {
        method: 'POST',
        headers: {
            'Authorization': `Bearer ${token}`,
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            fileName: file.name,
            fileSize: file.size,
            fileContent: base64,
            fileType: file.type
        })
    });
};
reader.readAsDataURL(file);
```

### Python

```python
import requests
import base64

# Register
response = requests.post(f'{API_URL}/auth', json={
    'action': 'register',
    'name': 'John Doe',
    'email': 'john@example.com',
    'password': 'password123'
})
token = response.json()['token']

# Upload File
with open('file.pdf', 'rb') as f:
    file_content = base64.b64encode(f.read()).decode()

requests.post(f'{API_URL}/storage', 
    headers={'Authorization': f'Bearer {token}'},
    json={
        'fileName': 'file.pdf',
        'fileSize': 1048576,
        'fileContent': file_content,
        'fileType': 'application/pdf'
    }
)
```

---

## Changelog

### v1.0.0 (2024-01-15)
- Initial API release
- Authentication endpoints
- Storage management
- Subscription integration
- Admin dashboard

---

## Support

For API issues:
- Check CloudWatch Logs
- Review error responses
- Contact support@yourdomain.com
