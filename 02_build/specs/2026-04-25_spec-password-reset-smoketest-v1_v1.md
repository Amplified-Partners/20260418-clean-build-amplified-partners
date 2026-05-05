---
title: "Technical Specification: Password Reset Feature"
id: "spec-password-reset-smoketest-v1"
version: 1
created: "2026-04-25"
type: "document"
topic_type: "spec"
audience: "internal"
layer: "build"
status: "filed"
signed_by: "Devon, 2026-04-25, devin-992682c244cf444f91e0a516498afbfd"
---

# Technical Specification: Password Reset Feature

## 1. Overview

This specification outlines the implementation of a password reset feature that allows users to securely reset their passwords via email verification, with a strict requirement to deliver reset emails within 1 minute of request.

## 2. Functional Requirements

### 2.1 Core Functionality
- Users can request password reset using their registered email address
- System generates secure, time-limited reset tokens
- Reset email must be delivered within 1 minute of request
- Users can reset password using valid token within expiry window
- Old password becomes invalid after successful reset

### 2.2 User Flows

#### 2.2.1 Password Reset Request Flow
1. User navigates to "Forgot Password" page
2. User enters registered email address
3. System validates email format and existence
4. System generates reset token and queues email
5. User receives confirmation message (regardless of email validity)
6. Reset email delivered within 1 minute

#### 2.2.2 Password Reset Completion Flow
1. User clicks reset link in email
2. System validates token (existence, expiry, usage status)
3. User enters and confirms new password
4. System validates password requirements
5. System updates password and invalidates token
6. User receives confirmation and is redirected to login

## 3. Technical Architecture

### 3.1 System Components

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   Frontend      │    │   Backend API    │    │   Email Queue   │
│   - Request UI  │◄──►│   - Validation   │◄──►│   - Redis/SQS   │
│   - Reset UI    │    │   - Token Mgmt   │    │   - Workers     │
└─────────────────┘    └──────────────────┘    └─────────────────┘
                                │                        │
                       ┌────────▼────────┐      ┌────────▼────────┐
                       │    Database     │      │  Email Service  │
                       │  - Users        │      │  - SMTP/SES     │
                       │  - Reset Tokens │      │  - Templates    │
                       └─────────────────┘      └─────────────────┘
```

### 3.2 Database Schema

#### 3.2.1 Users Table
```sql
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_password_reset TIMESTAMP
);

CREATE INDEX idx_users_email ON users(email);
```

#### 3.2.2 Password Reset Tokens Table
```sql
CREATE TABLE password_reset_tokens (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    token_hash VARCHAR(255) UNIQUE NOT NULL,
    expires_at TIMESTAMP NOT NULL,
    used_at TIMESTAMP NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    ip_address INET,
    user_agent TEXT
);

CREATE INDEX idx_reset_tokens_hash ON password_reset_tokens(token_hash);
CREATE INDEX idx_reset_tokens_user_id ON password_reset_tokens(user_id);
CREATE INDEX idx_reset_tokens_expires ON password_reset_tokens(expires_at);
```

## 4. API Specifications

### 4.1 Request Password Reset

**Endpoint:** `POST /api/auth/password-reset/request`

**Request:**
```json
{
    "email": "user@example.com"
}
```

**Response (Success - 200):**
```json
{
    "message": "If this email is registered, you will receive reset instructions within 1 minute.",
    "request_id": "req_abc123def456"
}
```

**Response (Rate Limited - 429):**
```json
{
    "error": "Too many reset requests. Please wait before trying again.",
    "retry_after": 300
}
```

### 4.2 Validate Reset Token

**Endpoint:** `GET /api/auth/password-reset/validate/{token}`

**Response (Valid Token - 200):**
```json
{
    "valid": true,
    "expires_in": 3600
}
```

**Response (Invalid Token - 400):**
```json
{
    "valid": false,
    "error": "Token is invalid or expired"
}
```

### 4.3 Complete Password Reset

**Endpoint:** `POST /api/auth/password-reset/complete`

**Request:**
```json
{
    "token": "abc123def456...",
    "new_password": "NewSecurePassword123!",
    "confirm_password": "NewSecurePassword123!"
}
```

**Response (Success - 200):**
```json
{
    "message": "Password successfully reset",
    "login_url": "/login"
}
```

## 5. Implementation Details

### 5.1 Token Generation and Management

#### 5.1.1 Token Generation
```python
import secrets
import hashlib
from datetime import datetime, timedelta

def generate_reset_token():
    """Generate cryptographically secure reset token"""
    token = secrets.token_urlsafe(32)  # 256-bit entropy
    token_hash = hashlib.sha256(token.encode()).hexdigest()
    expires_at = datetime.utcnow() + timedelta(hours=24)
    
    return token, token_hash, expires_at
```

#### 5.1.2 Token Validation
```python
def validate_reset_token(token):
    """Validate reset token and return user info if valid"""
    token_hash = hashlib.sha256(token.encode()).hexdigest()
    
    token_record = db.query("""
        SELECT rt.*, u.email 
        FROM password_reset_tokens rt
        JOIN users u ON rt.user_id = u.id
        WHERE rt.token_hash = %s 
        AND rt.expires_at > NOW() 
        AND rt.used_at IS NULL
    """, [token_hash])
    
    return token_record
```

### 5.2 Email Queue Implementation

#### 5.2.1 Queue Configuration (Redis)
```python
import redis
import json
from datetime import datetime

redis_client = redis.Redis(host='localhost', port=6379, db=0)

def queue_password_reset_email(user_email, reset_token, priority='high'):
    """Queue password reset email with high priority for 1-minute SLA"""
    message = {
        'type': 'password_reset',
        'email': user_email,
        'token': reset_token,
        'queued_at': datetime.utcnow().isoformat(),
        'priority': priority
    }
    
    # Use high-priority queue for password resets
    redis_client.lpush('email_queue:high', json.dumps(message))
    redis_client.expire('email_queue:high', 3600)  # 1 hour TTL
```

#### 5.2.2 Email Worker
```python
async def email_worker():
    """Process email queue with priority handling"""
    while True:
        try:
            # Process high priority queue first
            message = redis_client.brpop('email_queue:high', timeout=1)
            if not message:
                message = redis_client.brpop('email_queue:normal', timeout=5)
            
            if message:
                await process_email(json.loads(message[1]))
                
        except Exception as e:
            logger.error(f"Email worker error: {e}")
            await asyncio.sleep(5)
```

### 5.3 Email Service Integration

#### 5.3.1 Email Template
```html
<!DOCTYPE html>
<html>
<head>
    <title>Password Reset Request</title>
</head>
<body>
    <h2>Reset Your Password</h2>
    <p>Hello,</p>
    <p>You requested to reset your password. Click the link below to set a new password:</p>
    <p><a href="{{reset_url}}" style="background-color: #007bff; color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px;">Reset Password</a></p>
    <p>This link will expire in 24 hours.</p>
    <p>If you didn't request this reset, please ignore this email.</p>
    <p>Best regards,<br>Your App Team</p>
</body>
</html>
```

#### 5.3.2 Email Service Implementation
```python
import boto3
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

class EmailService:
    def __init__(self):
        self.ses_client = boto3.client('ses', region_name='us-east-1')
    
    async def send_password_reset_email(self, email, token):
        """Send password reset email via AWS SES"""
        reset_url = f"{config.FRONTEND_URL}/reset-password?token={token}"
        
        html_body = render_template('password_reset.html', {
            'reset_url': reset_url,
            'app_name': config.APP_NAME
        })
        
        try:
            response = self.ses_client.send_email(
                Source=config.FROM_EMAIL,
                Destination={'ToAddresses': [email]},
                Message={
                    'Subject': {'Data': 'Reset Your Password'},
                    'Body': {'Html': {'Data': html_body}}
                }
            )
            
            logger.info(f"Password reset email sent to {email}, MessageId: {response['MessageId']}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to send password reset email to {email}: {e}")
            return False
```

## 6. Security Considerations

### 6.1 Token Security
- Tokens generated with cryptographically secure random generator
- Tokens hashed before database storage
- 24-hour expiration window
- Single-use tokens (invalidated after use)
- IP address and User-Agent logging for audit trail

### 6.2 Rate Limiting
```python
class PasswordResetRateLimiter:
    def __init__(self, redis_client):
        self.redis = redis_client
    
    def check_rate_limit(self, email, ip_address):
        """Check rate limits for password reset requests"""
        email_key = f"reset_rate:email:{email}"
        ip_key = f"reset_rate:ip:{ip_address}"
        
        email_count = self.redis.get(email_key) or 0
        ip_count = self.redis.get(ip_key) or 0
        
        if int(email_count) >= 3:  # Max 3 per email per hour
            return False, "Too many requests for this email"
        
        if int(ip_count) >= 10:  # Max 10 per IP per hour
            return False, "Too many requests from this IP"
        
        # Increment counters
        pipe = self.redis.pipeline()
        pipe.incr(email_key)
        pipe.expire(email_key, 3600)
        pipe.incr(ip_key)
        pipe.expire(ip_key, 3600)
        pipe.execute()
        
        return True, None
```

### 6.3 Password Validation
```python
def validate_password(password):
    """Validate password meets security requirements"""
    errors = []
    
    if len(password) < 8:
        errors.append("Password must be at least 8 characters long")
    
    if not re.search(r'[A-Z]', password):
        errors.append("Password must contain at least one uppercase letter")
    
    if not re.search(r'[a-z]', password):
        errors.append("Password must contain at least one lowercase letter")
    
    if not re.search(r'\d', password):
        errors.append("Password must contain at least one number")
    
    if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
        errors.append("Password must contain at least one special character")
    
    return len(errors) == 0, errors
```

## 7. Performance Requirements

### 7.1 Email Delivery SLA
- **Target:** 95% of emails delivered within 60 seconds
- **Maximum:** 99% of emails delivered within 90 seconds
- **Monitoring:** Queue depth and processing time metrics

### 7.2 Queue Configuration
```python
# Email queue worker configuration
EMAIL_WORKERS = {
    'high_priority': {
        'workers': 5,
        'queue': 'email_queue:high',
        'timeout': 30,
        'retry_limit': 3
    },
    'normal_priority': {
        'workers': 2,
        'queue': 'email_queue:normal',
        'timeout': 60,
        'retry_limit': 2
    }
}
```

## 8. Monitoring and Logging

### 8.1 Key Metrics
- Email delivery time percentiles (p50, p95, p99)
- Queue depth and processing rate
- Failed email delivery rate
- Token usage patterns
- Rate limiting triggers

### 8.2 Logging Structure
```python
import structlog

logger = structlog.get_logger()

# Password reset request
logger.info(
    "password_reset_requested",
    email=masked_email,
    request_id=request_id,
    ip_address=request.remote_addr,
    user_agent=request.user_agent.string
)

# Email queued
logger.info(
    "password_reset_email_queued",
    request_id=request_id,
    queue_time=datetime.utcnow().isoformat(),
    priority="high"
)

# Email sent
logger.info(
    "password_reset_email_sent",
    request_id=request_id,
    delivery_time_ms=delivery_time,
    message_id=ses_message_id
)
```

## 9. Testing Strategy

### 9.1 Unit Tests
- Token generation and validation
- Password validation logic
- Rate limiting functionality
- Email template rendering

### 9.2 Integration Tests
- End-to-end password reset flow
- Email queue processing
- Database transaction handling
- Rate limiting with Redis

### 9.3 Performance Tests
- Email delivery time under load
- Queue processing capacity
- Database performance with concurrent requests
- Rate limiting accuracy

## 10. Deployment Considerations

### 10.1 Infrastructure Requirements
- Redis cluster for email queue (high availability)
- AWS SES or equivalent email service
- Database with proper indexing
- Load balancer with sticky sessions
- Monitoring and alerting system

### 10.2 Configuration Management
```yaml
# Environment variables
EMAIL_SERVICE_TYPE: "ses"  # ses, smtp, sendgrid
REDIS_URL: "redis://localhost:6379/0"
EMAIL_QUEUE_WORKERS: 5
PASSWORD_RESET_TOKEN_TTL: 86400  # 24 hours
RATE_LIMIT_EMAIL_PER_HOUR: 3
RATE_LIMIT_IP_PER_HOUR: 10
EMAIL_DELIVERY_SLA_SECONDS: 60
```

This technical specification provides a comprehensive foundation for implementing a secure, scalable password reset feature that meets the 1-minute email delivery requirement through proper queue management and monitoring.