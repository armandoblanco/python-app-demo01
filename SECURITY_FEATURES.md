# Security Features Documentation

## Overview
This document describes the production security recommendations implemented in the application.

## Implemented Security Features

### 1. JWT Authentication (JSON Web Tokens)
- **Implementation**: Flask-JWT-Extended
- **Purpose**: Secure authentication for protected API endpoints
- **Configuration**: 
  - Token expiration: 1 hour
  - Secret key: Configured via `JWT_SECRET_KEY` environment variable
  
#### Usage:
```bash
# Login to get JWT token
curl -X POST http://localhost:5000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username": "admin", "password": "admin123"}'

# Response:
# {
#   "success": true,
#   "access_token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
#   "token_type": "Bearer"
# }

# Use token to access protected endpoints
curl http://localhost:5000/api/admin/products \
  -H "Authorization: Bearer YOUR_TOKEN_HERE"
```

#### Protected Endpoints:
- `/api/admin/products` - Admin access to product catalog

### 2. Rate Limiting
- **Implementation**: Flask-Limiter
- **Purpose**: Prevent API abuse and DDoS attacks
- **Storage**: In-memory (development), Redis recommended for production
- **Default Limits**:
  - 200 requests per day
  - 50 requests per hour per IP address

**Production Configuration:**
For production, use Redis or database-backed storage to persist rate limits across restarts:
```python
storage_uri="redis://localhost:6379"
```

#### Endpoint-Specific Limits:
- `/api/auth/login`: 5 requests per minute (prevent brute force attacks)
- `/api/products`: 100 requests per minute
- `/api/products/<id>`: 100 requests per minute
- `/api/categories`: 100 requests per minute
- `/api/admin/products`: 50 requests per minute

#### Rate Limit Response:
```json
{
  "success": false,
  "error": "Rate limit exceeded. Please try again later."
}
```
HTTP Status Code: 429 (Too Many Requests)

### 3. HTTPS Enforcement
- **Implementation**: Flask-Talisman
- **Purpose**: Ensure all connections use HTTPS
- **Features**:
  - Automatic HTTP to HTTPS redirect
  - Strict Transport Security (HSTS) headers
  - Only enabled in production environment

#### Configuration:
Set environment variable to enable HTTPS enforcement:
```bash
export FLASK_ENV=production
```

### 4. Content Security Policy (CSP)
- **Implementation**: Flask-Talisman CSP headers
- **Purpose**: Prevent XSS attacks and data injection
- **Policy**:
  ```
  default-src: 'self'
  script-src: 'self' 'unsafe-inline'
  style-src: 'self' 'unsafe-inline'
  img-src: 'self' https: data:
  font-src: 'self'
  connect-src: 'self'
  ```

### 5. Input Validation and Sanitization
- **Implementation**: Bleach library + custom validation
- **Purpose**: Prevent XSS, SQL injection, and other injection attacks

#### Validation Functions:
1. **`sanitize_input(text, max_length=200)`**
   - Removes all HTML tags
   - Limits string length
   - Prevents XSS attacks

2. **`validate_category(category)`**
   - Validates against whitelist of allowed categories
   - Defaults to 'all' for invalid input

#### Protected Parameters:
- Search queries (max 100 characters)
- Category filters (whitelist validation)
- Product IDs (integer validation, must be positive)
- Login credentials (max 50 characters for username)

### 6. Audit Logging
- **Implementation**: Python logging module
- **Purpose**: Track security events and API usage
- **Log File**: `audit.log`

#### Logged Events:
- Login attempts (success/failure)
- API access (all endpoints)
- Input validation failures
- Rate limit violations
- 404/500 errors
- Admin endpoint access

#### Log Format:
```
2024-01-15 10:30:45 - audit - INFO - [192.168.1.1] Action: LOGIN_SUCCESS | User: admin | Details: User logged in: admin | IP: 192.168.1.1
```

#### Audit Event Types:
- `LOGIN_SUCCESS` - Successful authentication
- `LOGIN_FAILED` - Failed authentication attempt
- `LOGIN_ERROR` - Login system error
- `GET_PRODUCTS` - Product list accessed
- `GET_PRODUCT` - Single product accessed
- `GET_PRODUCT_NOT_FOUND` - Product not found
- `GET_CATEGORIES` - Categories accessed
- `ADMIN_GET_PRODUCTS` - Admin endpoint accessed
- `RATE_LIMIT_EXCEEDED` - Rate limit triggered
- `404_ERROR` - Endpoint not found
- `500_ERROR` - Internal server error

### 7. Additional Security Measures

#### Error Handling
- Stack traces never exposed to clients
- Generic error messages for security-sensitive errors
- Detailed logging for debugging

#### Password Security
- Demo uses simple authentication (username: `admin`, password: `admin123`)
- **PRODUCTION RECOMMENDATION**: Implement proper password hashing (bcrypt/argon2)
- **PRODUCTION RECOMMENDATION**: Use database for user storage
- **PRODUCTION RECOMMENDATION**: Implement password complexity requirements

## Environment Variables

### Required for Production:
```bash
# JWT Secret Key (generate strong random key)
export JWT_SECRET_KEY="your-super-secret-key-here"

# Enable production mode
export FLASK_ENV=production
```

### Generating Secure JWT Secret:
```bash
python -c "import secrets; print(secrets.token_hex(32))"
```

### Demo Credentials Configuration (Development):
```bash
# Optional: Override demo credentials (defaults: admin/admin123)
export DEMO_USERNAME="your_username"
export DEMO_PASSWORD="your_password"
```

## Production Deployment Checklist

- [ ] Change `JWT_SECRET_KEY` from default value
- [ ] Set `FLASK_ENV=production` to enable HTTPS enforcement
- [ ] Configure reverse proxy (nginx/apache) for HTTPS
- [ ] Set up proper SSL/TLS certificates
- [ ] Implement database-backed user authentication
- [ ] Use password hashing (bcrypt/argon2)
- [ ] Configure centralized logging (e.g., ELK stack)
- [ ] Set up monitoring and alerting
- [ ] Review and adjust rate limits based on usage patterns
- [ ] Implement CORS restrictions for production domains
- [ ] Regular security updates for dependencies
- [ ] Enable firewall rules
- [ ] Implement database connection pooling
- [ ] Set up automated backups
- [ ] Configure session management
- [ ] Implement account lockout after failed login attempts
- [ ] Add 2FA support for admin accounts
- [ ] Regular security audits

## Testing Security Features

Run the test suite to verify all security features:
```bash
python -m pytest tests/test_api.py -v
```

### Security-Specific Tests:
- JWT authentication
- Rate limiting (login endpoint)
- Input sanitization (XSS prevention)
- Input validation (category filtering)
- Protected endpoint access control
- Error handling

## API Documentation

### Authentication Endpoints

#### POST `/api/auth/login`
Login and obtain JWT token.

**Request:**
```json
{
  "username": "admin",
  "password": "admin123"
}
```

**Response (Success):**
```json
{
  "success": true,
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "token_type": "Bearer"
}
```

**Response (Error):**
```json
{
  "success": false,
  "error": "Invalid credentials"
}
```

### Protected Endpoints

#### GET `/api/admin/products`
Get all products (admin only, requires JWT token).

**Headers:**
```
Authorization: Bearer YOUR_TOKEN_HERE
```

**Response:**
```json
{
  "success": true,
  "data": [...],
  "count": 10,
  "user": "admin"
}
```

## Monitoring and Alerts

### Recommended Monitoring:
1. Monitor `audit.log` for suspicious activity
2. Track rate limit violations
3. Monitor failed login attempts
4. Alert on unusual API usage patterns
5. Monitor error rates (4xx, 5xx)

### Log Analysis:
```bash
# Count failed login attempts
grep "LOGIN_FAILED" audit.log | wc -l

# Show rate limit violations
grep "RATE_LIMIT_EXCEEDED" audit.log

# Show recent admin access
grep "ADMIN_GET_PRODUCTS" audit.log | tail -10
```

## References

- [Flask-JWT-Extended Documentation](https://flask-jwt-extended.readthedocs.io/)
- [Flask-Limiter Documentation](https://flask-limiter.readthedocs.io/)
- [Flask-Talisman Documentation](https://github.com/GoogleCloudPlatform/flask-talisman)
- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [OWASP API Security Top 10](https://owasp.org/www-project-api-security/)

## Support

For security issues, please review the [SECURITY.md](SECURITY.md) file for reporting procedures.
