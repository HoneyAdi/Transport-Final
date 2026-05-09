#!/usr/bin/env python3
"""Migration with direct file logging"""

import sys
import os

# Redirect stdout and stderr to a log file
log_file = open('migration_run.log', 'w', encoding='utf-8')
sys.stdout = log_file
sys.stderr = log_file

os.chdir(r'E:\PROJECTS\Transport')

db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'admin',
    'database': 'transport_db'
}

try:
    import pymysql
    import re
    
    print("=" * 60)
    print("VENDOR MULTIPLE ADDRESSES MIGRATION")
    print("=" * 60)
    
    conn = pymysql.connect(
        host=db_config['host'],
        user=db_config['user'],
        password=db_config['password'],
        database=db_config['database'],
        charset='utf8mb4',
        cursorclass=pymysql.cursors.DictCursor
    )
    
    with conn.cursor() as cursor:
        # Step 1: Create vendor_addresses table
        print("\n[STEP 1] Creating vendor_addresses table...")
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS vendor_addresses (
                id INT AUTO_INCREMENT PRIMARY KEY,
                tenant_id INT NOT NULL,
                vendor_id INT NOT NULL,
                address_type VARCHAR(50) NOT NULL,
                address_line1 VARCHAR(255) NOT NULL,
                address_line2 VARCHAR(255),
                city VARCHAR(100) NOT NULL,
                state VARCHAR(100) NOT NULL,
                pincode VARCHAR(20) NOT NULL,
                country VARCHAR(100) DEFAULT 'India',
                contact_person VARCHAR(200),
                phone VARCHAR(20),
                email VARCHAR(150),
                is_primary BOOLEAN DEFAULT FALSE,
                is_active BOOLEAN DEFAULT TRUE,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                INDEX idx_vendor_addresses_tenant (tenant_id),
                INDEX idx_vendor_addresses_vendor (vendor_id),
                FOREIGN KEY (tenant_id) REFERENCES tenants(id) ON DELETE CASCADE,
                FOREIGN KEY (vendor_id) REFERENCES vendors(id) ON DELETE CASCADE,
                UNIQUE KEY uq_vendor_address_type (vendor_id, address_type)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
        """)
        print("[OK] Table created or already exists")
        
        # Step 2: Add vendor fields to expenses
        print("\n[STEP 2] Adding vendor fields to expenses table...")
        
        cursor.execute("""
            SELECT COUNT(*) as cnt FROM information_schema.columns 
            WHERE table_name = 'expenses' AND column_name = 'vendor_id'
            AND table_schema = DATABASE()
        """)
        if cursor.fetchone()['cnt'] == 0:
            cursor.execute("ALTER TABLE expenses ADD COLUMN vendor_id INT, ADD INDEX idx_expenses_vendor (vendor_id)")
            print("[OK] vendor_id column added")
        else:
            print("[OK] vendor_id already exists")
        
        cursor.execute("""
            SELECT COUNT(*) as cnt FROM information_schema.columns 
            WHERE table_name = 'expenses' AND column_name = 'vendor_address_id'
            AND table_schema = DATABASE()
        """)
        if cursor.fetchone()['cnt'] == 0:
            cursor.execute("ALTER TABLE expenses ADD COLUMN vendor_address_id INT, ADD INDEX idx_expenses_vendor_address (vendor_address_id)")
            print("[OK] vendor_address_id column added")
        else:
            print("[OK] vendor_address_id already exists")
        
        # Step 3: Migrate existing addresses
        print("\n[STEP 3] Migrating existing vendor addresses...")
        cursor.execute("""
            SELECT v.id, v.tenant_id, v.reg_address_line1, v.reg_address_line2, 
                   v.reg_city, v.reg_state, v.reg_pincode, v.reg_country,
                   v.contact_person, v.phone_primary, v.mobile, v.email
            FROM vendors v
            LEFT JOIN vendor_addresses va ON v.id = va.vendor_id
            WHERE va.id IS NULL AND v.reg_address_line1 IS NOT NULL
        """)
        vendors = cursor.fetchall()
        
        migrated = 0
        for vendor in vendors:
            try:
                cursor.execute("""
                    INSERT INTO vendor_addresses 
                    (tenant_id, vendor_id, address_type, address_line1, address_line2,
                     city, state, pincode, country, contact_person, phone, email, is_primary, is_active)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """, (
                    vendor['tenant_id'], vendor['id'], 'Registered Office',
                    vendor['reg_address_line1'], vendor['reg_address_line2'],
                    vendor['reg_city'], vendor['reg_state'], vendor['reg_pincode'], vendor['reg_country'] or 'India',
                    vendor['contact_person'], vendor['phone_primary'] or vendor['mobile'], vendor['email'],
                    True, True
                ))
                migrated += 1
            except Exception as e:
                print(f"  [WARN] Error migrating vendor {vendor['id']}: {e}")
        
        print(f"[OK] Migrated {migrated} vendor addresses")
        
        conn.commit()
        
        print("\n" + "=" * 60)
        print("MIGRATION COMPLETED SUCCESSFULLY!")
        print("=" * 60)
        print(f"\nSummary:")
        print(f"- vendor_addresses table: OK")
        print(f"- Expense table updated: OK")
        print(f"- Migrated {migrated} addresses: OK")
        
    conn.close()
    
except ImportError as e:
    print(f"[ERROR] Import error: {e}")
    print("Install with: pip install pymysql")
except Exception as e:
    print(f"[ERROR] Migration failed: {e}")
    import traceback
    traceback.print_exc()

log_file.close()
