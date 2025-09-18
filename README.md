# Portfolio Backend - Professional Recommendations System

A sophisticated Django REST API backend for managing professional recommendations with enterprise-level architecture patterns.

## 🏗️ Architecture Overview

This project implements a **Senior Backend Developer** level architecture with:

- **Repository Pattern**: Separates data access logic from business logic
- **Service Layer Pattern**: Encapsulates business logic and complex operations
- **Common Layer**: Reusable components and utilities across applications
- **Clean Architecture**: Well-organized, maintainable, and testable code structure

## 🚀 Features

### Core Functionality
- ✅ **Professional Recommendations Management**
- ✅ **Rating System (1-5 stars)**
- ✅ **Skills Tracking**
- ✅ **Image Upload for Recommenders**
- ✅ **Featured Recommendations**
- ✅ **Public/Private Visibility Control**
- ✅ **Advanced Search & Filtering**
- ✅ **Statistics & Analytics**

### Technical Features
- ✅ **PostgreSQL Database**
- ✅ **Django REST Framework**
- ✅ **Comprehensive API Documentation**
- ✅ **Caching System**
- ✅ **Soft Delete Functionality**
- ✅ **UUID Primary Keys**
- ✅ **Timestamp Tracking**
- ✅ **Custom Exception Handling**
- ✅ **Logging System**
- ✅ **Comprehensive Test Suite**

## 📁 Project Structure

```
portfolio_backend/
├── common/                     # Shared utilities and base classes
│   ├── models.py              # Base models (TimestampedModel, UUIDModel, etc.)
│   ├── managers.py            # Custom model managers
│   ├── repositories.py        # Base repository pattern implementation
│   ├── services.py            # Base service layer implementation
│   ├── serializers.py         # Base serializers
│   ├── exceptions.py          # Custom exception classes
│   └── utils.py               # Utility functions
├── recommendations/           # Recommendations app
│   ├── models.py             # Recommendation model
│   ├── repositories.py       # Recommendation repository
│   ├── services.py           # Recommendation service
│   ├── serializers.py        # API serializers
│   ├── views.py              # API viewsets
│   ├── admin.py              # Django admin configuration
│   ├── tests.py              # Comprehensive test suite
│   └── management/           # Management commands
│       └── commands/
│           └── create_sample_recommendations.py
└── portfolio_backend/        # Main project settings
    ├── settings.py           # Django settings
    ├── urls.py               # URL configuration
    └── wsgi.py               # WSGI configuration
```

## 🛠️ Installation & Setup

### Prerequisites
- Python 3.8+
- PostgreSQL 12+
- pip or pipenv

### 1. Clone the Repository
```bash
git clone <repository-url>
cd portfolio_backend
```

### 2. Create Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Database Setup (MySQL)
```bash
# Copy environment file
cp .env.example .env

# Edit .env file with your MySQL credentials
# DB_NAME=Wassim221e$PortfolioDb
# DB_USER=Wassim221e
# DB_PASSWORD=your_mysql_password
# DB_HOST=Wassim221e.mysql.pythonanywhere-services.com
# DB_PORT=3306
```

**Note**: The project uses MySQL as primary database with SQLite fallback for development.

### 5. Run Migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### 6. Create Superuser
```bash
python manage.py createsuperuser
```

### 7. Load Sample Data (Optional)
```bash
python manage.py create_sample_recommendations --count 5
```

### 8. Run Development Server
```bash
python manage.py runserver
```

## 📚 API Documentation

### Interactive Documentation
- **Swagger UI**: `http://localhost:8000/swagger/` - Interactive API documentation with testing capabilities
- **ReDoc**: `http://localhost:8000/redoc/` - Clean, responsive API documentation
- **API Docs**: `http://localhost:8000/docs/` - Alternative Swagger interface

### OpenAPI Schema
- **JSON Schema**: `http://localhost:8000/swagger.json` - Raw OpenAPI 3.0 schema
- **YAML Schema**: `http://localhost:8000/swagger.yaml` - YAML format schema

The documentation includes:
- Complete API endpoint descriptions
- Request/response schemas
- Authentication requirements
- Example requests and responses
- Interactive testing interface

### Base URL
```
http://localhost:8000/api/
```

### Authentication
The API uses Django REST Framework's session authentication. For write operations, authentication is required.

### Available Endpoints (4 Basic CRUD Operations Only)

#### Recommendations
- `GET /api/recommendations/` - List all recommendations (no pagination, filtering, or search)
- `POST /api/recommendations/` - Create new recommendation (authenticated)
- `GET /api/recommendations/{id}/` - Get specific recommendation details
- `PUT /api/recommendations/{id}/` - Update recommendation (authenticated)

### Ultra-Simple Data Format

Each recommendation displays in clean format:
```json
{
  "id": "uuid",
  "recommender_name": "Ahmed Hassan",
  "recommender_title": "Project Manager",
  "recommender_company": "Tech Solutions Ltd",
  "recommender_location": "Dubai, UAE",
  "recommendation_date": "2024-06-20",
  "rating": 5,
  "rating_stars": "★★★★★",
  "recommendation_text": "Working with Wassim was a pleasure...",
  "linkedin_url": "https://linkedin.com/in/ahmed-hassan"
}
```

### Required Fields for Create/Update
- **recommender_name**: Full name (e.g., "Ahmed Hassan")
- **recommender_title**: Job title (e.g., "Project Manager")
- **recommender_company**: Company name (e.g., "Tech Solutions Ltd")
- **recommendation_date**: Date in YYYY-MM-DD format
- **rating**: Integer from 1 to 5 stars
- **recommendation_text**: The recommendation content (minimum 10 characters)

### Optional Fields
- **recommender_location**: Location (e.g., "Dubai, UAE")
- **linkedin_url**: LinkedIn profile URL (e.g., "https://linkedin.com/in/username")

### Removed Features
- ❌ Image upload (removed as requested)
- ❌ Pagination (removed for simplicity)
- ❌ Search functionality (removed for simplicity)
- ❌ Filtering and sorting (removed for simplicity)
- ❌ Delete operation (only GET, POST, PUT allowed)

### Example API Responses

#### Get Recommendations
```json
{
  "success": true,
  "message": "Success",
  "data": [
    {
      "id": "uuid-here",
      "recommender_name": "Adel Abobacker",
      "recommender_title": "Senior WordPress Developer",
      "recommender_company": "Freelancer",
      "recommendation_text": "Wassim Alshami is an exceptional back-end developer...",
      "rating": 5,
      "rating_display": "★★★★★",
      "recommendation_date": "2024-07-15",
      "is_featured": true,
      "skills_mentioned": ["ASP.NET", "Problem Solving"],
      "recommender_image_url": "http://localhost:8000/media/recommendations/images/image.jpg"
    }
  ]
}
```

#### Get Statistics
```json
{
  "success": true,
  "data": {
    "total_recommendations": 5,
    "featured_recommendations": 3,
    "average_rating": 4.8,
    "rating_distribution": {
      "5_stars": 4,
      "4_stars": 1,
      "3_stars": 0,
      "2_stars": 0,
      "1_star": 0
    },
    "companies_count": 5,
    "latest_recommendation_date": "2024-07-15"
  }
}
```

## 🧪 Testing

### Run All Tests
```bash
python manage.py test
```

### Run Specific Test Categories
```bash
# Model tests
python manage.py test recommendations.tests.RecommendationModelTest

# Repository tests
python manage.py test recommendations.tests.RecommendationRepositoryTest

# Service tests
python manage.py test recommendations.tests.RecommendationServiceTest

# API tests
python manage.py test recommendations.tests.RecommendationAPITest
```

### Test Coverage
The project includes comprehensive tests covering:
- Model functionality and validation
- Repository pattern implementation
- Service layer business logic
- API endpoints and responses
- Authentication and permissions
- File upload functionality

## 🔧 Configuration

### Environment Variables
```bash
# Django Settings
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Database Configuration
DB_NAME=portfolio_db
DB_USER=postgres
DB_PASSWORD=your-password-here
DB_HOST=localhost
DB_PORT=5432

# Static and Media Files
STATIC_URL=/static/
MEDIA_URL=/media/
```

### Caching
The project uses Django's built-in caching framework. Configure Redis for production:

```python
CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': 'redis://127.0.0.1:6379/1',
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
        }
    }
}
```

## 🚀 Deployment

### Production Checklist
- [ ] Set `DEBUG=False`
- [ ] Configure proper `ALLOWED_HOSTS`
- [ ] Set up PostgreSQL database
- [ ] Configure Redis for caching
- [ ] Set up static file serving (nginx/Apache)
- [ ] Configure media file storage (AWS S3/similar)
- [ ] Set up logging
- [ ] Configure SSL/HTTPS
- [ ] Set up monitoring

### Docker Deployment (Optional)
```dockerfile
# Dockerfile example
FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
EXPOSE 8000

CMD ["gunicorn", "portfolio_backend.wsgi:application", "--bind", "0.0.0.0:8000"]
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 👨‍💻 Author

**Wassim Alshami**
- Senior Backend Developer
- Expertise in Django, ASP.NET, and scalable architecture
- Focus on clean code, performance optimization, and best practices

---

*This project demonstrates senior-level backend development skills with enterprise architecture patterns, comprehensive testing, and production-ready code quality.*
