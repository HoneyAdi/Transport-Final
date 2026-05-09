#!/usr/bin/env python3
"""Check database schema for missing tables/columns"""

import pymysql

# Database config
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
    print("DATABASE SCHEMA CHECK")
    print("=" * 60)
    
    with conn.cursor() as cursor:
        # Check vendor_addresses table
        print("\n[1] Checking vendor_addresses table...")
        cursor.execute("""
            SELECT COUNT(*) as cnt FROM information_schema.tables 
            WHERE table_name = 'vendor_addresses' AND table_schema = DATABASE()
        """)
        exists = cursor.fetchone()['cnt'] > 0
        print(f"   Table exists: {'YES ✓' if exists else 'NO ✗'}")
        
        if exists:
            cursor.execute("SHOW COLUMNS FROM vendor_addresses")
            cols = cursor.fetchall()
            print(f"   Columns ({len(cols)}):")
            for col in cols:
                print(f"      - {col['Field']}: {col['Type']}")
        
        # Check expenses table for vendor fields
        print("\n[2] Checking expenses table...")
        cursor.execute("SHOW COLUMNS FROM expenses")
        cols = cursor.fetchall()
        col_names = [c['Field'] for c in cols]
        
        has_vendor_id = 'vendor_id' in col_names
        has_vendor_address_id = 'vendor_address_id' in col_names
        
        print(f"   vendor_id: {'YES ✓' if has_vendor_id else 'NO ✗'}")
        print(f"   vendor_address_id: {'YES ✓' if has_vendor_address_id else 'NO ✗'}")
        
        # Check transport_bills table for vendor_address_id
        print("\n[3] Checking transport_bills table...")
        cursor.execute("""
            SELECT COUNT(*) as cnt FROM information_schema.columns 
            WHERE table_name = 'transport_bills' AND column_name = 'vendor_address_id'
            AND table_schema = DATABASE()
        """)
        has_tba = cursor.fetchone()['cnt'] > 0
        print(f"   vendor_address_id: {'YES ✓' if has_tba else 'NO ✗'}")
        
        # List all tables
        print("\n[4] All tables in database:")
        cursor.execute("SHOW TABLES")
        tables = cursor.fetchall()
        for table in tables:
            table_name = list(table.values())[0]
            print(f"   - {table_name}")
        
        # Check for any vendor addresses
        if exists:
            print("\n[5] Vendor addresses count:")
            cursor.execute("SELECT COUNT(*) as cnt FROM vendor_addresses")
            count = cursor.fetchone()['cnt']
            print(f"   Total addresses: {count}")
    
    conn.close()
    
    print("\n" + "=" * 60)
    print("SCHEMA CHECK COMPLETE")
    print("=" * 60)
    
except ImportError:
    print("[ERROR] pymysql not installed. Run: pip install pymysql")
except Exception as e:
    print(f"[ERROR] {e}")
    import traceback
    traceback.print_exc()
