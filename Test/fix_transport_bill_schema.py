#!/usr/bin/env python3
"""Add vendor fields to transport_bills table"""

import pymysql

db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'admin',
    'database': 'transport_db'
}

try:
    conn = pymysql.connect(
        host=db_config['host'],
        user=db_config['user'],
        password=db_config['password'],
        database=db_config['database'],
        cursorclass=pymysql.cursors.DictCursor
    )
    
    print("=" * 60)
    print("FIXING TRANSPORT_BILLS SCHEMA")
    print("=" * 60)
    
    with conn.cursor() as cursor:
        # Check and add vendor_id
        print("\n[1] Checking vendor_id column...")
        cursor.execute("""
            SELECT COUNT(*) as cnt FROM information_schema.columns 
            WHERE table_name = 'transport_bills' AND column_name = 'vendor_id'
            AND table_schema = DATABASE()
        """)
        if cursor.fetchone()['cnt'] == 0:
            cursor.execute("""
                ALTER TABLE transport_bills 
                ADD COLUMN vendor_id INT,
                ADD INDEX idx_transport_bills_vendor (vendor_id)
            """)
            print("  [OK] vendor_id added")
        else:
            print("  [OK] vendor_id already exists")
        
        # Check and add vendor_address_id
        print("\n[2] Checking vendor_address_id column...")
        cursor.execute("""
            SELECT COUNT(*) as cnt FROM information_schema.columns 
            WHERE table_name = 'transport_bills' AND column_name = 'vendor_address_id'
            AND table_schema = DATABASE()
        """)
        if cursor.fetchone()['cnt'] == 0:
            cursor.execute("""
                ALTER TABLE transport_bills 
                ADD COLUMN vendor_address_id INT,
                ADD INDEX idx_transport_bills_vendor_address (vendor_address_id)
            """)
            print("  [OK] vendor_address_id added")
        else:
            print("  [OK] vendor_address_id already exists")
        
        conn.commit()
    
    conn.close()
    
    print("\n" + "=" * 60)
    print("SCHEMA FIX COMPLETE!")
    print("=" * 60)
    
except Exception as e:
    print(f"[ERROR] {e}")
    import traceback
    traceback.print_exc()
