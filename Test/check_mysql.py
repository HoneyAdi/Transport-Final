"""
MySQL Setup Verification Script
Checks if MySQL connection works and creates database if needed
"""
import sys
import pymysql
import os

def load_env():
    """Load environment variables from .env file"""
    if os.path.exists('.env'):
        with open('.env', 'r') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    key, value = line.split('=', 1)
                    os.environ[key] = value

def check_mysql_setup():
    load_env()
    
    # Read from environment variables
    DB_USER = os.getenv('DB_USER', 'root')
    DB_PASSWORD = os.getenv('DB_PASSWORD', 'admin')
    DB_HOST = os.getenv('DB_HOST', 'localhost')
    DB_NAME = os.getenv('DB_NAME', 'transport_db')
    
    print("=" * 50)
    print("MySQL Setup Verification")
    print("=" * 50)
    print(f"\nUsing credentials:")
    print(f"  Host: {DB_HOST}")
    print(f"  User: {DB_USER}")
    print(f"  Database: {DB_NAME}")
    
    # Check 1: Can connect to MySQL server
    print("\n[1] Checking MySQL server connection...")
    try:
        conn = pymysql.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD,
            charset='utf8mb4'
        )
        print("    [OK] Connected to MySQL server successfully")
    except pymysql.Error as e:
        print(f"    [FAIL] Failed to connect: {e}")
        print("\n    Possible issues:")
        print("    - MySQL server not running")
        print("    - Wrong username/password")
        print("    - MySQL not installed")
        print("\n    To fix: Update .env file with correct credentials")
        return False
    
    # Check 2: Check if database exists
    print(f"\n[2] Checking database '{DB_NAME}'...")
    try:
        with conn.cursor() as cursor:
            cursor.execute(f"SHOW DATABASES LIKE '{DB_NAME}'")
            result = cursor.fetchone()
            if result:
                print(f"    [OK] Database '{DB_NAME}' exists")
            else:
                print(f"    [INFO] Database '{DB_NAME}' not found")
                print(f"\n[3] Creating database '{DB_NAME}'...")
                cursor.execute(f"CREATE DATABASE {DB_NAME} CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci")
                conn.commit()
                print(f"    [OK] Database '{DB_NAME}' created successfully")
    except pymysql.Error as e:
        print(f"    [FAIL] Database error: {e}")
        return False
    finally:
        conn.close()
    
    print("\n" + "=" * 50)
    print("MySQL setup is ready!")
    print("=" * 50)
    print("\nNext steps:")
    print("  1. pip install PyMySQL==1.1.0")
    print("  2. python init_db.py")
    print("  3. python app.py")
    return True

if __name__ == '__main__':
    success = check_mysql_setup()
    sys.exit(0 if success else 1)
