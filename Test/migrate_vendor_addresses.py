#!/usr/bin/env python3
"""
Database Migration Script: Vendor Multiple Addresses

This script:
1. Creates the vendor_addresses table
2. Migrates existing vendor addresses to the new table
3. Adds vendor_id and vendor_address_id to expenses table
4. Merges duplicate GSTIN vendors into single vendor with multiple addresses
5. Restores GSTIN unique constraint

Run: python migrate_vendor_addresses.py
"""
import os
import sys

# Set environment variables before importing models
os.environ['AUTO_MIGRATE'] = 'false'

from app import app, db
from sqlalchemy import text

def create_vendor_addresses_table():
    """Create the vendor_addresses table if not exists"""
    print("=" * 60)
    print("STEP 1: Creating vendor_addresses table")
    print("=" * 60)
    
    with app.app_context():
        # Check if table exists
        result = db.session.execute(text("""
            SELECT COUNT(*) FROM information_schema.tables 
            WHERE table_name = 'vendor_addresses' AND table_schema = DATABASE()
        """))
        
        if result.scalar() > 0:
            print("[OK] vendor_addresses table already exists")
            return True
        
        print("Creating vendor_addresses table...")
        db.session.execute(text("""
            CREATE TABLE vendor_addresses (
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
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
        """))
        db.session.commit()
        print("[OK] vendor_addresses table created successfully")
        return True

def add_expense_vendor_fields():
    """Add vendor_id and vendor_address_id to expenses table"""
    print("\n" + "=" * 60)
    print("STEP 2: Adding vendor fields to expenses table")
    print("=" * 60)
    
    with app.app_context():
        # Check if vendor_id column exists
        result = db.session.execute(text("""
            SELECT COUNT(*) FROM information_schema.columns 
            WHERE table_name = 'expenses' AND column_name = 'vendor_id' AND table_schema = DATABASE()
        """))
        
        if result.scalar() == 0:
            print("Adding vendor_id column to expenses table...")
            db.session.execute(text("""
                ALTER TABLE expenses 
                ADD COLUMN vendor_id INT,
                ADD INDEX idx_expenses_vendor (vendor_id),
                ADD FOREIGN KEY (vendor_id) REFERENCES vendors(id) ON DELETE SET NULL
            """))
            db.session.commit()
            print("[OK] vendor_id column added")
        else:
            print("[OK] vendor_id column already exists")
        
        # Check if vendor_address_id column exists
        result = db.session.execute(text("""
            SELECT COUNT(*) FROM information_schema.columns 
            WHERE table_name = 'expenses' AND column_name = 'vendor_address_id' AND table_schema = DATABASE()
        """))
        
        if result.scalar() == 0:
            print("Adding vendor_address_id column to expenses table...")
            db.session.execute(text("""
                ALTER TABLE expenses 
                ADD COLUMN vendor_address_id INT,
                ADD INDEX idx_expenses_vendor_address (vendor_address_id),
                ADD FOREIGN KEY (vendor_address_id) REFERENCES vendor_addresses(id) ON DELETE SET NULL
            """))
            db.session.commit()
            print("[OK] vendor_address_id column added")
        else:
            print("[OK] vendor_address_id column already exists")
        
        return True

def migrate_existing_addresses():
    """Migrate existing vendor addresses to the new table"""
    print("\n" + "=" * 60)
    print("STEP 3: Migrating existing vendor addresses")
    print("=" * 60)
    
    with app.app_context():
        from models import Vendor, VendorAddress
        
        vendors = Vendor.query.all()
        migrated_count = 0
        skipped_count = 0
        
        for vendor in vendors:
            # Check if vendor already has addresses
            existing = VendorAddress.query.filter_by(vendor_id=vendor.id).first()
            if existing:
                skipped_count += 1
                continue
            
            # Create address from vendor's registered address
            if vendor.reg_address_line1:
                try:
                    address = VendorAddress(
                        tenant_id=vendor.tenant_id,
                        vendor_id=vendor.id,
                        address_type='Registered Office',
                        address_line1=vendor.reg_address_line1 or '',
                        address_line2=vendor.reg_address_line2,
                        city=vendor.reg_city or '',
                        state=vendor.reg_state or '',
                        pincode=vendor.reg_pincode or '',
                        country=vendor.reg_country or 'India',
                        contact_person=vendor.contact_person,
                        phone=vendor.phone_primary or vendor.mobile,
                        email=vendor.email,
                        is_primary=True,
                        is_active=True
                    )
                    db.session.add(address)
                    migrated_count += 1
                except Exception as e:
                    print(f"  [WARN] Error migrating vendor {vendor.vendor_code}: {e}")
                    db.session.rollback()
                    continue
            
            # If vendor has different office address, add it too
            if (vendor.office_address_line1 and 
                vendor.office_address_line1 != vendor.reg_address_line1):
                try:
                    address = VendorAddress(
                        tenant_id=vendor.tenant_id,
                        vendor_id=vendor.id,
                        address_type='Office',
                        address_line1=vendor.office_address_line1 or '',
                        address_line2=vendor.office_address_line2,
                        city=vendor.office_city or '',
                        state=vendor.office_state or '',
                        pincode=vendor.office_pincode or '',
                        country=vendor.office_country or 'India',
                        is_primary=False,
                        is_active=True
                    )
                    db.session.add(address)
                except Exception as e:
                    print(f"  [WARN] Error adding office address for {vendor.vendor_code}: {e}")
                    db.session.rollback()
                    continue
        
        db.session.commit()
        print(f"[OK] Migrated {migrated_count} vendor addresses")
        print(f"[INFO] Skipped {skipped_count} vendors (already migrated)")
        return True

def merge_duplicate_gstin_vendors():
    """Merge vendors with duplicate GSTIN into single vendor with multiple addresses"""
    print("\n" + "=" * 60)
    print("STEP 4: Merging duplicate GSTIN vendors")
    print("=" * 60)
    
    with app.app_context():
        from models import Vendor, VendorAddress, Expense
        
        # Find duplicate GSTINs per tenant
        result = db.session.execute(text("""
            SELECT tenant_id, gstin, GROUP_CONCAT(id ORDER BY id) as vendor_ids, COUNT(*) as count
            FROM vendors 
            WHERE gstin IS NOT NULL AND gstin != ''
            GROUP BY tenant_id, gstin 
            HAVING COUNT(*) > 1
        """))
        
        duplicates = result.fetchall()
        
        if not duplicates:
            print("[OK] No duplicate GSTIN vendors found")
            return True
        
        print(f"Found {len(duplicates)} duplicate GSTIN groups")
        
        merged_count = 0
        for dup in duplicates:
            tenant_id, gstin, vendor_ids_str, count = dup
            vendor_ids = [int(id) for id in vendor_ids_str.split(',')]
            
            print(f"\n  Processing GSTIN: {gstin} (Tenant: {tenant_id})")
            print(f"    Found {count} vendors: {vendor_ids}")
            
            # Keep the first vendor as master
            master_vendor_id = vendor_ids[0]
            duplicate_vendor_ids = vendor_ids[1:]
            
            master_vendor = Vendor.query.get(master_vendor_id)
            if not master_vendor:
                print(f"    [ERROR] Master vendor {master_vendor_id} not found")
                continue
            
            print(f"    Master vendor: {master_vendor.vendor_code} ({master_vendor.vendor_name})")
            
            # Migrate addresses from duplicate vendors to master
            for dup_id in duplicate_vendor_ids:
                dup_vendor = Vendor.query.get(dup_id)
                if not dup_vendor:
                    print(f"    [WARN] Duplicate vendor {dup_id} not found")
                    continue
                
                # Get or create address for duplicate vendor
                address_type = 'Office'
                if dup_vendor.reg_address_line1:
                    # Check if this address already exists for master
                    existing = VendorAddress.query.filter_by(
                        vendor_id=master_vendor_id,
                        address_line1=dup_vendor.reg_address_line1
                    ).first()
                    
                    if not existing:
                        try:
                            new_address = VendorAddress(
                                tenant_id=tenant_id,
                                vendor_id=master_vendor_id,
                                address_type=address_type,
                                address_line1=dup_vendor.reg_address_line1 or '',
                                address_line2=dup_vendor.reg_address_line2,
                                city=dup_vendor.reg_city or '',
                                state=dup_vendor.reg_state or '',
                                pincode=dup_vendor.reg_pincode or '',
                                country=dup_vendor.reg_country or 'India',
                                contact_person=dup_vendor.contact_person,
                                phone=dup_vendor.phone_primary or dup_vendor.mobile,
                                email=dup_vendor.email,
                                is_primary=False,
                                is_active=True
                            )
                            db.session.add(new_address)
                            print(f"    [OK] Migrated address from {dup_vendor.vendor_code}")
                        except Exception as e:
                            print(f"    [ERROR] Failed to migrate address: {e}")
                            db.session.rollback()
                            continue
                    else:
                        print(f"    [INFO] Address already exists for master, skipping")
                
                # Update related records to point to master vendor
                try:
                    Expense.query.filter_by(vendor_id=dup_id).update({"vendor_id": master_vendor_id})
                    print(f"    [OK] Updated expenses to point to master vendor")
                except Exception as e:
                    print(f"    [WARN] Could not update expenses: {e}")
                
                # Delete the duplicate vendor
                try:
                    db.session.delete(dup_vendor)
                    print(f"    [OK] Deleted duplicate vendor {dup_vendor.vendor_code}")
                except Exception as e:
                    print(f"    [ERROR] Failed to delete duplicate: {e}")
                    db.session.rollback()
                    continue
            
            db.session.commit()
            merged_count += 1
        
        print(f"\n[OK] Merged {merged_count} duplicate GSTIN groups")
        return True

def restore_gstin_constraint():
    """Restore GSTIN unique constraint"""
    print("\n" + "=" * 60)
    print("STEP 5: Restoring GSTIN unique constraint")
    print("=" * 60)
    
    with app.app_context():
        # Check if constraint exists
        result = db.session.execute(text("""
            SELECT COUNT(*) FROM information_schema.table_constraints 
            WHERE table_name = 'vendors' 
            AND constraint_name = 'uq_vendor_gstin_tenant'
            AND table_schema = DATABASE()
        """))
        
        if result.scalar() > 0:
            print("[OK] GSTIN unique constraint already exists")
            return True
        
        try:
            print("Restoring GSTIN unique constraint...")
            db.session.execute(text("""
                ALTER TABLE vendors 
                ADD CONSTRAINT uq_vendor_gstin_tenant 
                UNIQUE KEY (tenant_id, gstin)
            """))
            db.session.commit()
            print("[OK] GSTIN unique constraint restored")
            return True
        except Exception as e:
            print(f"[ERROR] Failed to restore constraint: {e}")
            db.session.rollback()
            return False

def verify_migration():
    """Verify the migration results"""
    print("\n" + "=" * 60)
    print("STEP 6: Verification")
    print("=" * 60)
    
    with app.app_context():
        # Count addresses
        result = db.session.execute(text("SELECT COUNT(*) FROM vendor_addresses"))
        address_count = result.scalar()
        print(f"Total vendor addresses: {address_count}")
        
        # Count vendors with addresses
        result = db.session.execute(text("""
            SELECT COUNT(DISTINCT vendor_id) FROM vendor_addresses
        """))
        vendors_with_addresses = result.scalar()
        print(f"Vendors with addresses: {vendors_with_addresses}")
        
        # Check for duplicate GSTINs
        result = db.session.execute(text("""
            SELECT COUNT(*) FROM (
                SELECT tenant_id, gstin, COUNT(*) as cnt
                FROM vendors 
                WHERE gstin IS NOT NULL AND gstin != ''
                GROUP BY tenant_id, gstin 
                HAVING COUNT(*) > 1
            ) as dups
        """))
        duplicate_count = result.scalar()
        
        if duplicate_count == 0:
            print("[OK] No duplicate GSTINs found - constraint is effective")
        else:
            print(f"[WARNING] Found {duplicate_count} duplicate GSTINs")
        
        # Show sample data
        print("\nSample vendor addresses:")
        result = db.session.execute(text("""
            SELECT v.vendor_code, v.vendor_name, v.gstin, 
                   va.address_type, va.city, va.state, va.is_primary
            FROM vendors v
            JOIN vendor_addresses va ON v.id = va.vendor_id
            LIMIT 5
        """))
        
        for row in result.fetchall():
            print(f"  {row.vendor_code} | {row.vendor_name[:20]:<20} | {row.gstin or 'N/A':<15} | {row.address_type:<15} | {row.city}, {row.state} {'[PRIMARY]' if row.is_primary else ''}")
        
        return True

def main():
    """Main migration function"""
    print("\n" + "=" * 60)
    print("VENDOR MULTIPLE ADDRESSES MIGRATION")
    print("=" * 60)
    print("\nThis script will:")
    print("1. Create vendor_addresses table")
    print("2. Add vendor fields to expenses table")
    print("3. Migrate existing vendor addresses")
    print("4. Merge duplicate GSTIN vendors")
    print("5. Restore GSTIN unique constraint")
    print("6. Verify the migration")
    print("\n" + "=" * 60)
    
    try:
        # Run all migration steps
        steps = [
            create_vendor_addresses_table,
            add_expense_vendor_fields,
            migrate_existing_addresses,
            merge_duplicate_gstin_vendors,
            restore_gstin_constraint,
            verify_migration
        ]
        
        for step in steps:
            if not step():
                print(f"\n[ERROR] Migration failed at step: {step.__name__}")
                return 1
        
        print("\n" + "=" * 60)
        print("MIGRATION COMPLETED SUCCESSFULLY!")
        print("=" * 60)
        print("\nSummary:")
        print("- vendor_addresses table created")
        print("- Expense table updated with vendor fields")
        print("- Existing addresses migrated")
        print("- Duplicate vendors merged")
        print("- GSTIN unique constraint restored")
        print("- One vendor can now have multiple addresses")
        print("\nNext steps:")
        print("1. Restart the Flask server")
        print("2. Test vendor address management in UI")
        print("3. Use vendor address selection in Transport Bills and Expenses")
        
        return 0
        
    except Exception as e:
        print(f"\n[ERROR] Migration failed: {e}")
        import traceback
        traceback.print_exc()
        return 1

if __name__ == "__main__":
    sys.exit(main())
