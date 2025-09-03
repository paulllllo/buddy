# Onboarding-as-a-Service (OaaS) Backend

A FastAPI-based backend for the Onboarding-as-a-Service application, providing a robust API for managing onboarding flows, content types, and new hire progress tracking.

## 🚀 Features

- **FastAPI** with automatic OpenAPI documentation
- **SQLAlchemy** ORM with PostgreSQL/SQLite support
- **JWT Authentication** with access and refresh tokens
- **Abstracted File Storage** (Local/S3)
- **Dynamic Content Types** with JSONB storage
- **Multi-tenant Architecture** (company-based isolation)
- **Progress Tracking** at content block level
- **CORS Support** for frontend integration

## 🏗️ Architecture

### Database Models
- **Company**: Multi-tenant isolation
- **User**: Admin authentication
- **OnboardingFlow**: Flow management
- **Stage**: Flow stages with ordering
- **ContentBlock**: Dynamic content with JSONB
- **ContentType**: Content type definitions
- **NewHire**: New hire management
- **Progress**: Granular progress tracking
- **StageTemplate**: Reusable stage templates

### Key Components
- **Authentication**: JWT with refresh tokens
- **Storage**: Abstracted file storage interface
- **Validation**: Pydantic schemas
- **Database**: SQLAlchemy with migrations

## 📋 Prerequisites

- Python 3.8+
- pip
- (Optional) Redis for caching
- (Optional) PostgreSQL for production

## 🛠️ Installation

1. **Clone and navigate to backend directory**
   ```bash
   cd backend
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   ```bash
   cp env.example .env
   # Edit .env with your configuration
   ```

5. **Generate secret key**
   ```bash
   python -c "import secrets; print(secrets.token_urlsafe(32))"
   # Add the output to SECRET_KEY in .env
   ```

## 🚀 Running the Application

### Development
```bash
python run.py
```

### Production
```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

The API will be available at:
- **API**: http://localhost:8000
- **Documentation**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## 📚 API Endpoints

### Authentication
- `POST /api/auth/register` - Register new company and admin
- `POST /api/auth/login` - Login user
- `POST /api/auth/refresh` - Refresh access token

### Companies
- `GET /api/companies/me` - Get current company info
- `PUT /api/companies/me` - Update company settings

### Onboarding Flows
- `GET /api/flows` - List flows
- `POST /api/flows` - Create flow
- `GET /api/flows/{id}` - Get flow details
- `PUT /api/flows/{id}` - Update flow
- `DELETE /api/flows/{id}` - Delete flow

### Stages
- `GET /api/flows/{flow_id}/stages` - List stages
- `POST /api/flows/{flow_id}/stages` - Create stage
- `GET /api/stages/{id}` - Get stage details
- `PUT /api/stages/{id}` - Update stage
- `DELETE /api/stages/{id}` - Delete stage

### Content Types
- `GET /api/content-types` - List content types
- `GET /api/content-types/{name}` - Get content type
- `GET /api/content-types/{name}/config` - Get content type config
- `POST /api/content-types/validate` - Validate content

### New Hires
- `GET /api/new-hires` - List new hires
- `POST /api/new-hires` - Create new hire
- `GET /api/new-hires/{id}` - Get new hire details
- `PUT /api/new-hires/{id}` - Update new hire

## 🔧 Configuration

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `DATABASE_URL` | Database connection string | `sqlite:///./onboarding.db` |
| `SECRET_KEY` | JWT secret key | Required |
| `FILE_STORAGE_TYPE` | Storage backend (local/s3) | `local` |
| `LOCAL_STORAGE_PATH` | Local storage directory | `./uploads` |
| `CORS_ORIGINS` | Allowed CORS origins | `["http://localhost:3000"]` |

### Database Migration

For PostgreSQL production deployment:
```bash
# Update DATABASE_URL in .env
DATABASE_URL=postgresql://user:password@localhost/onboarding

# Run migrations (when implemented)
alembic upgrade head
```

## 🧪 Testing

```bash
# Run tests
pytest

# Run with coverage
pytest --cov=app
```

## 📁 Project Structure

```
backend/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI application
│   ├── config.py            # Configuration settings
│   ├── database.py          # Database setup
│   ├── auth/                # Authentication
│   │   ├── jwt.py
│   │   └── dependencies.py
│   ├── models/              # SQLAlchemy models
│   │   ├── __init__.py
│   │   ├── company.py
│   │   ├── user.py
│   │   ├── onboarding_flow.py
│   │   ├── stage.py
│   │   ├── content_block.py
│   │   ├── content_type.py
│   │   ├── new_hire.py
│   │   ├── progress.py
│   │   └── stage_template.py
│   ├── routers/             # API routes
│   │   ├── __init__.py
│   │   ├── auth.py
│   │   ├── companies.py
│   │   ├── flows.py
│   │   ├── stages.py
│   │   ├── content_types.py
│   │   └── new_hires.py
│   ├── schemas/             # Pydantic schemas
│   │   ├── __init__.py
│   │   └── auth.py
│   └── storage/             # File storage
│       ├── __init__.py
│       ├── base.py
│       ├── local.py
│       └── factory.py
├── requirements.txt
├── run.py
├── env.example
└── README.md
```

## 🔒 Security

- **JWT Authentication**: Secure token-based auth
- **Password Hashing**: bcrypt for password security
- **CORS Protection**: Configurable origin restrictions
- **Input Validation**: Pydantic schema validation
- **SQL Injection Protection**: SQLAlchemy ORM

## 🚀 Deployment

### Docker (Recommended)
```dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Environment Setup
1. Set production environment variables
2. Use PostgreSQL for production database
3. Configure S3 for file storage
4. Set up Redis for caching
5. Configure proper CORS origins

## 🤝 Contributing

1. Follow the existing code structure
2. Add tests for new features
3. Update documentation
4. Use type hints
5. Follow PEP 8 style guide

## 📄 License

This project is part of the Onboarding-as-a-Service application. 