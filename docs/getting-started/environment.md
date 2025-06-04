# Environment Configuration

Configure your environment variables for optimal system performance and security.

## 📋 Required Configuration

### OpenAI API Configuration

The AI agents require OpenAI API access:

```env
# Required for AI Agents
OPENAI_API_KEY=your-openai-api-key-here
OPENAI_MODEL=gpt-4o-mini
OPENAI_MAX_TOKENS=1000
```

!!! tip "Getting OpenAI API Key"

    1. Visit [OpenAI Platform](https://platform.openai.com/)
    2. Create an account or sign in
    3. Navigate to API Keys section
    4. Create a new API key
    5. Copy and paste into your `.env` file

### Database Configuration

Local SQLite database is used by default:

```env
DATABASE_URL=sqlite:///./disaster_response.db
```

### Authentication & Security

```env
# JWT Configuration
JWT_SECRET=your-super-secret-jwt-key-here-must-be-long-and-random
JWT_ALGORITHM=HS256
JWT_EXPIRE_MINUTES=1440

# Session configuration
SESSION_SECRET=your-session-secret-key
```

!!! warning "Security Best Practices"

    - Use strong, random secrets (minimum 32 characters)
    - Never commit `.env` files to version control
    - Rotate secrets regularly in production
    - Use different secrets for each environment

## 🔧 Optional Configuration

### Redis Configuration

For caching and session storage:

```env
# Redis configuration
REDIS_URL=redis://localhost:6379/0
REDIS_PASSWORD=
REDIS_DB=0
```

### Email & SMS Services

For notifications (optional):

```env
# Email configuration (SendGrid example)
SENDGRID_API_KEY=your-sendgrid-api-key
FROM_EMAIL=noreply@disaster-response.com

# SMS configuration (Twilio example)
TWILIO_ACCOUNT_SID=your-twilio-account-sid
TWILIO_AUTH_TOKEN=your-twilio-auth-token
TWILIO_PHONE_NUMBER=+1234567890
```

### External APIs

Integration with external services:

```env
# Weather API
WEATHER_API_KEY=your-weather-api-key

# Maps & Geocoding
GOOGLE_MAPS_API_KEY=your-google-maps-api-key

# Emergency Services API
EMERGENCY_API_ENDPOINT=https://api.emergency-services.gov
EMERGENCY_API_KEY=your-emergency-api-key
```

## 🌍 Environment-Specific Settings

### Development Environment

```env
# Development settings
ENVIRONMENT=development
DEBUG=true
LOG_LEVEL=DEBUG

# CORS settings for development
CORS_ORIGINS=["http://localhost:3000", "http://localhost:5173"]

# Database debug
DATABASE_ECHO=true
```

### Production Environment

```env
# Production settings
ENVIRONMENT=production
DEBUG=false
LOG_LEVEL=INFO

# Security settings
CORS_ORIGINS=["https://your-domain.com"]
SECURE_COOKIES=true
HTTPS_ONLY=true

# Performance settings
DATABASE_POOL_SIZE=20
DATABASE_MAX_OVERFLOW=30
REDIS_MAX_CONNECTIONS=100
```

### Testing Environment

```env
# Testing settings
ENVIRONMENT=testing
DATABASE_URL=postgresql://postgres:password@localhost:5432/disaster_response_test
REDIS_URL=redis://localhost:6379/1

# Disable external services in tests
DISABLE_NOTIFICATIONS=true
MOCK_EXTERNAL_APIS=true
```

## 📁 Configuration Files

### Main Environment File

Create `ai_services/.env`:

```bash
cp ai_services/.env.example ai_services/.env
```

Edit with your configuration:

```env
# Core Configuration
ENVIRONMENT=development
DEBUG=true

# OpenAI Configuration
OPENAI_API_KEY=sk-your-openai-api-key-here
OPENAI_MODEL=gpt-4o-mini

# Database
DATABASE_URL=postgresql://postgres:password@postgres:5432/disaster_response

# Security
JWT_SECRET=your-very-long-random-secret-key-here
SESSION_SECRET=another-random-secret-key

# Redis
REDIS_URL=redis://redis:6379/0

# API Configuration
API_HOST=0.0.0.0
API_PORT=8000
API_WORKERS=4

# CORS
CORS_ORIGINS=["http://localhost:3000", "http://localhost:5173"]

# Logging
LOG_LEVEL=INFO
LOG_FORMAT=json
```

### Docker Environment

For Docker Compose, also create `docker.env`:

```env
# Docker-specific overrides
POSTGRES_DB=disaster_response
POSTGRES_USER=postgres
POSTGRES_PASSWORD=password

REDIS_PASSWORD=
```

## 🔍 Environment Validation

The system validates environment configuration on startup:

```bash
# Check configuration
make validate-env

# Or manually
cd ai_services
uv run python -c "from core.config import settings; print('✅ Configuration valid')"
```

### Common Validation Errors

!!! error "Missing OpenAI API Key"

    ```
    Error: OPENAI_API_KEY is required
    ```

    **Solution**: Add your OpenAI API key to `.env` file

!!! error "Invalid Database URL"

    ```
    Error: Cannot connect to database
    ```

    **Solution**: Verify database is running and URL is correct

!!! error "Weak JWT Secret"

    ```
    Warning: JWT_SECRET should be at least 32 characters
    ```

    **Solution**: Generate a longer random secret

## 🚀 Quick Setup Commands

```bash
# Generate random secrets
openssl rand -hex 32  # For JWT_SECRET
openssl rand -hex 24  # For SESSION_SECRET

# Test database connection
psql $DATABASE_URL -c "SELECT version();"

# Test Redis connection
redis-cli -u $REDIS_URL ping

# Validate OpenAI API
curl -H "Authorization: Bearer $OPENAI_API_KEY" \
     https://api.openai.com/v1/models | jq '.data[0].id'
```

## 📚 Next Steps

- [Docker Setup](docker.md) - Container configuration
- [Quick Setup](quick-setup.md) - Get running quickly
- [API Reference](../api/authentication.md) - API configuration options

---

Need help? Check the [Troubleshooting Guide](../troubleshooting.md) for common configuration issues.
