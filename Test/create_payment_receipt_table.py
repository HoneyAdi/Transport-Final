"""
Script to create payment_receipts table
"""
import pymysql

# Database configuration
DB_HOST = "localhost"
DB_USER = "root"
DB_PASSWORD = "admin"
DB_NAME = "transport_db"

def create_payment_receipt_table():
    """Create payment_receipts table"""
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
            WHERE table_name = 'payment_receipts' 
            AND table_schema = DATABASE()
        """)
        
        table_exists = cursor.fetchone()[0]
        
        if table_exists:
            print("[OK] payment_receipts table already exists")
        else:
            print("Creating payment_receipts table...")
            cursor.execute("""
                CREATE TABLE payment_receipts (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    tenant_id INT NOT NULL,
                    bilty_id INT NOT NULL,
                    receipt_number VARCHAR(50) NOT NULL,
                    receipt_date DATE NOT NULL DEFAULT (CURRENT_DATE),
                    amount_received DECIMAL(12, 2) NOT NULL,
                    tds_amount DECIMAL(12, 2) DEFAULT 0,
                    optional_amount DECIMAL(12, 2) DEFAULT 0,
                    optional_amount_reason TEXT,
                    balance_before DECIMAL(12, 2) NOT NULL,
                    balance_after DECIMAL(12, 2) NOT NULL,
                    is_complete BOOLEAN DEFAULT FALSE,
                    remarks TEXT,
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                    created_by INT,
                    INDEX idx_payment_receipts_tenant (tenant_id),
                    INDEX idx_payment_receipts_bilty (bilty_id),
                    INDEX idx_payment_receipts_date (receipt_date),
                    CONSTRAINT fk_payment_receipts_tenant FOREIGN KEY (tenant_id) REFERENCES tenants(id) ON DELETE CASCADE,
                    CONSTRAINT fk_payment_receipts_bilty FOREIGN KEY (bilty_id) REFERENCES transport_bills(id) ON DELETE CASCADE,
                    CONSTRAINT fk_payment_receipts_creator FOREIGN KEY (created_by) REFERENCES users(id) ON DELETE SET NULL,
                    CONSTRAINT uq_payment_receipt_number_tenant UNIQUE (tenant_id, receipt_number)
                ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
            """)
            print("[OK] payment_receipts table created successfully")
        
        connection.commit()
        connection.close()
        print("\nMigration completed successfully!")
        
    except Exception as e:
        print(f"Error: {str(e)}")
        if 'connection' in locals():
            connection.rollback()
            connection.close()

if __name__ == "__main__":
    create_payment_receipt_table()
