"""
Script to create sample ratelist data
"""
from app import app, db
from models import RateList
from datetime import date

with app.app_context():
    # Check if ratelists exist
    if RateList.query.count() > 0:
        print(f"[OK] {RateList.query.count()} ratelists already exist")
    else:
        print("Creating sample ratelists...")
        
        # Sample ratelists
        ratelists = [
            RateList(
                tenant_id=1,
                name="Mumbai-Delhi Truck Rates",
                description="Standard rates for Mumbai to Delhi route",
                origin="Mumbai",
                destination="Delhi",
                vehicle_type="Truck",
                basic_freight=25000,
                loading_charge=500,
                unloading_charge=500,
                door_pickup_charge=1000,
                door_delivery_charge=1000,
                hamali_charge=800,
                detention_charge=500,
                waiting_charge=300,
                halting_charge=400,
                toll_charge=2000,
                border_charge=500,
                fuel_surcharge=1500,
                packing_charge=1000,
                weighment_charge=200,
                permit_charge=300,
                driver_allowance=1000,
                insurance_charge=500,
                other_charges=0,
                igst_rate=18,
                cgst_rate=9,
                sgst_rate=9,
                is_active=True,
                effective_from=date.today()
            ),
            RateList(
                tenant_id=1,
                name="Mumbai-Pune Tempo Rates",
                description="Standard rates for Mumbai to Pune route",
                origin="Mumbai",
                destination="Pune",
                vehicle_type="Tempo",
                basic_freight=8000,
                loading_charge=300,
                unloading_charge=300,
                door_pickup_charge=500,
                door_delivery_charge=500,
                hamali_charge=400,
                detention_charge=200,
                waiting_charge=100,
                halting_charge=150,
                toll_charge=500,
                border_charge=0,
                fuel_surcharge=400,
                packing_charge=300,
                weighment_charge=100,
                permit_charge=100,
                driver_allowance=500,
                insurance_charge=200,
                other_charges=0,
                igst_rate=18,
                cgst_rate=9,
                sgst_rate=9,
                is_active=True,
                effective_from=date.today()
            ),
            RateList(
                tenant_id=1,
                name="Delhi-Chennai Trailer Rates",
                description="Standard rates for Delhi to Chennai route",
                origin="Delhi",
                destination="Chennai",
                vehicle_type="Trailer",
                basic_freight=45000,
                loading_charge=1000,
                unloading_charge=1000,
                door_pickup_charge=2000,
                door_delivery_charge=2000,
                hamali_charge=1500,
                detention_charge=1000,
                waiting_charge=500,
                halting_charge=800,
                toll_charge=3500,
                border_charge=1000,
                fuel_surcharge=3000,
                packing_charge=2000,
                weighment_charge=500,
                permit_charge=500,
                driver_allowance=2000,
                insurance_charge=1000,
                other_charges=0,
                igst_rate=18,
                cgst_rate=9,
                sgst_rate=9,
                is_active=True,
                effective_from=date.today()
            )
        ]
        
        for ratelist in ratelists:
            db.session.add(ratelist)
        
        db.session.commit()
        print(f"[OK] Created {len(ratelists)} sample ratelists")
