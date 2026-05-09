from app import app, db
from models import Vendor, VendorAddress

with app.app_context():
    v = Vendor.query.first()
    print('First vendor:', v.vendor_name if v else 'None')
    print('Addresses:', v.addresses.count() if v else 0)
    if v and v.addresses.count() > 0:
        a = v.addresses.first()
        print('First address:', a.address_line1, a.city)
