"""
Script to create sample vendor addresses
"""
from app import app, db
from models import Vendor, VendorAddress
from datetime import date

with app.app_context():
    # Get first vendor
    vendor = Vendor.query.first()
    
    if not vendor:
        print("No vendors found. Please create vendors first.")
    else:
        print(f"Adding addresses for vendor: {vendor.vendor_name}")
        
        # Check if vendor already has addresses
        if vendor.addresses.count() > 0:
            print(f"[OK] Vendor already has {vendor.addresses.count()} addresses")
        else:
            print("Creating sample addresses...")
            
            # Sample addresses
            addresses = [
                VendorAddress(
                    tenant_id=vendor.tenant_id,
                    vendor_id=vendor.id,
                    address_type="Office",
                    address_line1="123 Industrial Area",
                    address_line2="Sector 5",
                    city="Mumbai",
                    state="Maharashtra",
                    pincode="400001",
                    country="India",
                    is_primary=True,
                    is_active=True,
                    contact_person="Rajesh Kumar",
                    phone="9876543210",
                    email="office@alokindustries.com"
                ),
                VendorAddress(
                    tenant_id=vendor.tenant_id,
                    vendor_id=vendor.id,
                    address_type="Warehouse",
                    address_line1="456 Warehouse Zone",
                    address_line2="Andheri East",
                    city="Mumbai",
                    state="Maharashtra",
                    pincode="400069",
                    country="India",
                    is_primary=False,
                    is_active=True,
                    contact_person="Suresh Patel",
                    phone="9876543211",
                    email="warehouse@alokindustries.com"
                ),
                VendorAddress(
                    tenant_id=vendor.tenant_id,
                    vendor_id=vendor.id,
                    address_type="Branch",
                    address_line1="789 Branch Office",
                    address_line2="Connaught Place",
                    city="Delhi",
                    state="Delhi",
                    pincode="110001",
                    country="India",
                    is_primary=False,
                    is_active=True,
                    contact_person="Amit Sharma",
                    phone="9876543212",
                    email="delhi@alokindustries.com"
                )
            ]
            
            for addr in addresses:
                db.session.add(addr)
            
            db.session.commit()
            print(f"[OK] Created {len(addresses)} sample addresses for {vendor.vendor_name}")
