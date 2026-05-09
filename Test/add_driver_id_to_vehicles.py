"""
Script to add driver_id column to vehicles table
"""
import pymysql

# Database configuration
DB_HOST = "localhost"
DB_USER = "root"
DB_PASSWORD = "admin"
DB_NAME = "transport_db"

def add_driver_id_column():
    """Add driver_id column to vehicles table"""
    try:
        # Connect to MySQL
        connection = pymysql.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME
        )
        
        cursor = connection.cursor()
        
        # Check if column already exists
        cursor.execute("""
            SELECT COUNT(*) 
            FROM information_schema.columns 
            WHERE table_name = 'vehicles' 
            AND column_name = 'driver_id' 
            AND table_schema = DATABASE()
        """)
        
        column_exists = cursor.fetchone()[0]
        
        if column_exists:
            print("[OK] driver_id column already exists in vehicles table")
        else:
            print("Adding driver_id column to vehicles table...")
            cursor.execute("""
                ALTER TABLE vehicles 
                ADD COLUMN driver_id INT,
                ADD INDEX idx_vehicles_driver (driver_id),
                ADD FOREIGN KEY (driver_id) REFERENCES drivers(id) ON DELETE SET NULL
            """)
            print("[OK] driver_id column added successfully")
        
        connection.commit()
        connection.close()
        print("\nMigration completed successfully!")
        
    except Exception as e:
        print(f"Error: {str(e)}")
        if 'connection' in locals():
            connection.rollback()
            connection.close()

if __name__ == "__main__":
    # Add driver_id column
    add_driver_id_column()
