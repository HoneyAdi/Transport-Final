"""
Script to create ratelists table
"""
import pymysql

# Database configuration
DB_HOST = "localhost"
DB_USER = "root"
DB_PASSWORD = "admin"
DB_NAME = "transport_db"

def create_ratelist_table():
    """Create ratelists table"""
    try:
        # Connect to MySQL
        connection = pymysql.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME
        )
        
        cursor = connection.cursor()
        
        # Check if table already exists
        cursor.execute("""
            SELECT COUNT(*) 
            FROM information_schema.tables 
            WHERE table_name = 'ratelists' 
            AND table_schema = DATABASE()
        """)
        
        table_exists = cursor.fetchone()[0]
        
        if table_exists:
            print("[OK] ratelists table already exists")
        else:
            print("Creating ratelists table...")
            cursor.execute("""
                CREATE TABLE ratelists (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    tenant_id INT NOT NULL,
                    name VARCHAR(200) NOT NULL,
                    description TEXT,
                    origin VARCHAR(100),
                    destination VARCHAR(100),
                    vehicle_type VARCHAR(50),
                    basic_freight DECIMAL(10, 2),
                    loading_charge DECIMAL(10, 2),
                    unloading_charge DECIMAL(10, 2),
                    door_pickup_charge DECIMAL(10, 2),
                    door_delivery_charge DECIMAL(10, 2),
                    hamali_charge DECIMAL(10, 2),
                    detention_charge DECIMAL(10, 2),
                    waiting_charge DECIMAL(10, 2),
                    halting_charge DECIMAL(10, 2),
                    toll_charge DECIMAL(10, 2),
                    border_charge DECIMAL(10, 2),
                    fuel_surcharge DECIMAL(10, 2),
                    packing_charge DECIMAL(10, 2),
                    weighment_charge DECIMAL(10, 2),
                    permit_charge DECIMAL(10, 2),
                    driver_allowance DECIMAL(10, 2),
                    insurance_charge DECIMAL(10, 2),
                    other_charges DECIMAL(10, 2),
                    igst_rate DECIMAL(5, 2),
                    cgst_rate DECIMAL(5, 2),
                    sgst_rate DECIMAL(5, 2),
                    is_active BOOLEAN DEFAULT TRUE,
                    effective_from DATE,
                    effective_to DATE,
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                    INDEX idx_ratelists_tenant (tenant_id),
                    INDEX idx_ratelists_active (is_active),
                    CONSTRAINT fk_ratelists_tenant FOREIGN KEY (tenant_id) REFERENCES tenants(id) ON DELETE CASCADE,
                    CONSTRAINT uq_ratelist_name_tenant UNIQUE (tenant_id, name)
                ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
            """)
            print("[OK] ratelists table created successfully")
        
        connection.commit()
        connection.close()
        print("\nMigration completed successfully!")
        
    except Exception as e:
        print(f"Error: {str(e)}")
        if 'connection' in locals():
            connection.rollback()
            connection.close()

if __name__ == "__main__":
    create_ratelist_table()
