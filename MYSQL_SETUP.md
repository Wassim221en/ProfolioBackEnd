# MySQL Database Setup Guide

## 🗄️ Database Configuration

This project is configured to use **MySQL** as the primary database with **SQLite** as a fallback for development.

### Production Database (PythonAnywhere)

- **Host**: `Wassim221e.mysql.pythonanywhere-services.com`
- **Database Name**: `Wassim221e$PortfolioDb`
- **Username**: `Wassim221e`
- **Port**: `3306`

## 🔧 Setup Instructions

### 1. Environment Configuration

Create or update your `.env` file with the MySQL credentials:

```bash
# Database Configuration - MySQL
DB_NAME=Wassim221e$PortfolioDb
DB_USER=Wassim221e
DB_PASSWORD=your_mysql_password_here
DB_HOST=Wassim221e.mysql.pythonanywhere-services.com
DB_PORT=3306
```

### 2. Install MySQL Client

The project uses `PyMySQL` as the MySQL client:

```bash
pip install PyMySQL==1.1.1
```

### 3. Database Connection Test

The application will automatically:
1. Try to connect to MySQL using the provided credentials
2. Fall back to SQLite if MySQL is unavailable
3. Display connection status in the console

### 4. Run Migrations

Once connected to MySQL:

```bash
python manage.py makemigrations
python manage.py migrate
```

### 5. Create Sample Data

```bash
python manage.py create_sample_recommendations --count 5
```

## 🔍 Connection Status

When you run the server, you'll see one of these messages:

- ✅ **"Using MySQL database"** - Successfully connected to MySQL
- ⚠️ **"MySQL not available, using SQLite for development"** - Fallback to SQLite

## 🛠️ Troubleshooting

### Common Issues

1. **Connection Timeout**
   - Check your internet connection
   - Verify the host address is correct
   - Ensure the database server is running

2. **Authentication Failed**
   - Double-check your username and password
   - Verify the database name format: `Wassim221e$PortfolioDb`

3. **Database Not Found**
   - Ensure the database `Wassim221e$PortfolioDb` exists on the server
   - Check if you have the correct permissions

### Testing Connection

You can test the MySQL connection manually:

```python
import pymysql

try:
    connection = pymysql.connect(
        host='Wassim221e.mysql.pythonanywhere-services.com',
        user='Wassim221e',
        password='your_password',
        database='Wassim221e$PortfolioDb',
        port=3306
    )
    print("✅ MySQL connection successful!")
    connection.close()
except Exception as e:
    print(f"❌ MySQL connection failed: {e}")
```

## 📝 Notes

- The project uses **PyMySQL** instead of **mysqlclient** for better compatibility
- **SQLite** is used automatically for testing to ensure fast test execution
- All database operations are compatible with both MySQL and SQLite
- The application gracefully handles database connection failures

## 🔐 Security

- Never commit your actual database password to version control
- Use environment variables for all sensitive configuration
- The `.env` file is already in `.gitignore`
- Consider using different credentials for development and production
