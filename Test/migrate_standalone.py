#!/usr/bin/env python3
"""Standalone migration script using Flask app database config"""

import os
import sys
import re

# Change to project directory
os.chdir(r'E:\PROJECTS\Transport')

# Read database credentials from app.py
db_config = None
try:
    with open('app.py', 'r', encoding='utf-8') as f:
        content = f.read()
        # Look for SQLALCHEMY_DATABASE_URI
        match = re.search(r"SQLALCHEMY_DATABASE_URI\s*=\s*['\"]([^'\"]+)['\"]", content)
        if match:
            uri = match.group(1)
            # Parse mysql://user:password@host/database
            match2 = re.search(r"mysql://([^:]+):([^@]+)@([^/]+)/(\w+)", uri)
            if match2:
                db_config = {
                    'user': match2.group(1),
                    'password': match2.group(2),
                    'host': match2.group(3),
                    'database': match2.group(4)
                }
except Exception as e:
    print(f"Warning: Could not read app.py: {e}")

# Fallback defaults if not found
if not db_config:
    db_config = {
        'host': 'localhost',
        'user': 'root',
        'password': 'admin',  # Updated with provided password
        'database': 'transport_db'
    }

# If password is empty, use default
if not db_config.get('password'):
    db_config['password'] = 'admin'

try:
    import pymysql
    
    print(f"Connecting to database {db_config['database']} at {db_config['host']}...")
    conn = pymysql.connect(
        host=db_config['host'],
        user=db_config['user'],
        password=db_config['password'],
        database=db_config['database'],
        charset='utf8mb4',
        cursorclass=pymysql.cursors.DictCursor
    )
    
    print("=" * 60)
    print("VENDOR MULTIPLE ADDRESSES MIGRATION")
    print("=" * 60)
    
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
        
        # Check if vendor_id exists
        cursor.execute("""
            SELECT COUNT(*) as cnt FROM information_schema.columns 
            WHERE table_name = 'expenses' AND column_name = 'vendor_id'
        """)
        if cursor.fetchone()['cnt'] == 0:
            cursor.execute("ALTER TABLE expenses ADD COLUMN vendor_id INT, ADD INDEX idx_expenses_vendor (vendor_id)")
            print("[OK] vendor_id column added")
        else:
            print("[OK] vendor_id already exists")
        
        # Check if vendor_address_id exists
        cursor.execute("""
            SELECT COUNT(*) as cnt FROM information_schema.columns 
            WHERE table_name = 'expenses' AND column_name = 'vendor_address_id'
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
        print("\nSummary:")
        print(f"- vendor_addresses table: OK")
        print(f"- Expense table updated: OK")
        print(f"- Migrated {migrated} addresses: OK")
        
    conn.close()
    
except ImportError:
    print("[ERROR] pymysql not installed. Install with: pip install pymysql")
    sys.exit(1)
except Exception as e:
    print(f"[ERROR] Migration failed: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
