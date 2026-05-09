"""
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, Response, session, g
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, date
from sqlalchemy import or_
from models import app, db, Tenant, User, DeliveryType, Location, Vehicle, TransportBill, Expense, Loan, generate_bill_name, generate_expense_name, generate_loan_name
import csv
import io

def get_current_user():
    user_id = session.get('user_id')
    if not user_id:
        return None
    return db.session.get(User, user_id)


@app.before_request
def require_login():
    g.current_user = get_current_user()
    g.current_tenant = g.current_user.tenant if g.current_user else None

    if request.endpoint is None:
        return None

    allowed_endpoints = {'login', 'static'}
    if request.endpoint in allowed_endpoints or request.endpoint.startswith('static'):
        return None

    if g.current_user is None:
        return redirect(url_for('login'))

    if not g.current_user.is_active:
        session.clear()
        flash('Your account is inactive. Please contact an administrator.', 'error')
        return redirect(url_for('login'))

    return None


@app.context_processor
def inject_auth_context():
    return {
        'current_user': getattr(g, 'current_user', None),
        'current_tenant': getattr(g, 'current_tenant', None)
    }


@app.route('/login', methods=['GET', 'POST'])
def login():
    if get_current_user():
        return redirect(url_for('dashboard'))

    if request.method == 'POST':
        identifier = request.form.get('identifier', '').strip()
        password = request.form.get('password', '')

        user = User.query.filter(
            or_(User.username == identifier, User.email == identifier)
        ).first()

        if not user or not user.check_password(password):
            flash('Invalid username/email or password.', 'error')
            return render_template('login.html')

        if not user.is_active:
            flash('Your account is inactive. Please contact an administrator.', 'error')
            return render_template('login.html')

        session['user_id'] = user.id
        flash(f'Welcome back, {user.full_name}!', 'success')
        return redirect(url_for('dashboard'))

    return render_template('login.html')


@app.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out successfully.', 'success')
    return redirect(url_for('login'))


# Dashboard
@app.route('/')
def dashboard():
    stats = {
        'total_bills': TransportBill.query.count(),
        'total_vehicles': Vehicle.query.count(),
        'total_locations': Location.query.count(),
        'total_delivery_types': DeliveryType.query.count(),
        'total_tenants': Tenant.query.count(),
    }
    recent_bills = TransportBill.query.order_by(TransportBill.created_at.desc()).limit(5).all()
    return render_template('dashboard.html', stats=stats, recent_bills=recent_bills)

# ============== DELIVERY TYPES ==============
@app.route('/delivery-types')
def delivery_types():
    types = DeliveryType.query.order_by(DeliveryType.delivery_type).all()
    return render_template('delivery_types/list.html', types=types)

@app.route('/delivery-types/create', methods=['GET', 'POST'])
def create_delivery_type():
    if request.method == 'POST':
        name = request.form.get('delivery_type', '').strip()
        if name:
            if DeliveryType.query.filter_by(delivery_type=name).first():
                flash('Delivery type already exists!', 'error')
            else:
                dt = DeliveryType(delivery_type=name)
                db.session.add(dt)
                db.session.commit()
                flash('Delivery type created successfully!', 'success')
                return redirect(url_for('delivery_types'))
        else:
            flash('Delivery type name is required!', 'error')
    return render_template('delivery_types/form.html')

@app.route('/delivery-types/edit/<int:id>', methods=['GET', 'POST'])
def edit_delivery_type(id):
    dt = DeliveryType.query.get_or_404(id)
    if request.method == 'POST':
        name = request.form.get('delivery_type', '').strip()
        if name:
            existing = DeliveryType.query.filter_by(delivery_type=name).first()
            if existing and existing.id != id:
                flash('Delivery type already exists!', 'error')
            else:
                dt.delivery_type = name
                db.session.commit()
                flash('Delivery type updated successfully!', 'success')
                return redirect(url_for('delivery_types'))
        else:
            flash('Delivery type name is required!', 'error')
    return render_template('delivery_types/form.html', dt=dt, edit=True)

@app.route('/delivery-types/delete/<int:id>', methods=['POST'])
def delete_delivery_type(id):
    dt = DeliveryType.query.get_or_404(id)
    try:
        db.session.delete(dt)
        db.session.commit()
        flash('Delivery type deleted successfully!', 'success')
    except:
        db.session.rollback()
        flash('Cannot delete: Delivery type is in use!', 'error')
    return redirect(url_for('delivery_types'))

# ============== LOCATIONS ==============
@app.route('/locations')
def locations():
    locs = Location.query.order_by(Location.location).all()
    return render_template('locations/list.html', locations=locs)

@app.route('/locations/create', methods=['GET', 'POST'])
def create_location():
    if request.method == 'POST':
        name = request.form.get('location', '').strip()
        rate = request.form.get('rate', 0)
        try:
            rate = int(rate) if rate else 0
        except:
            rate = 0
        
        if name:
            if Location.query.filter_by(location=name).first():
                flash('Location already exists!', 'error')
            else:
                loc = Location(location=name, rate=rate)
                db.session.add(loc)
                db.session.commit()
                flash('Location created successfully!', 'success')
                return redirect(url_for('locations'))
        else:
            flash('Location name is required!', 'error')
    return render_template('locations/form.html')

@app.route('/locations/edit/<int:id>', methods=['GET', 'POST'])
def edit_location(id):
    loc = Location.query.get_or_404(id)
    if request.method == 'POST':
        name = request.form.get('location', '').strip()
        rate = request.form.get('rate', 0)
        try:
            rate = int(rate) if rate else 0
        except:
            rate = 0
        
        if name:
            existing = Location.query.filter_by(location=name).first()
            if existing and existing.id != id:
                flash('Location already exists!', 'error')
            else:
                loc.location = name
                loc.rate = rate
                db.session.commit()
                flash('Location updated successfully!', 'success')
                return redirect(url_for('locations'))
        else:
            flash('Location name is required!', 'error')
    return render_template('locations/form.html', location=loc, edit=True)

@app.route('/locations/delete/<int:id>', methods=['POST'])
def delete_location(id):
    loc = Location.query.get_or_404(id)
    try:
        db.session.delete(loc)
        db.session.commit()
        flash('Location deleted successfully!', 'success')
    except:
        db.session.rollback()
        flash('Cannot delete: Location is in use!', 'error')
    return redirect(url_for('locations'))

@app.route('/api/location-rate/<int:id>')
def get_location_rate(id):
    loc = Location.query.get(id)
    if loc:
        return jsonify({'rate': loc.rate, 'location': loc.location})
    return jsonify({'rate': 0}), 404

# ============== VEHICLES ==============
@app.route('/vehicles')
def vehicles():
    vehs = Vehicle.query.order_by(Vehicle.registration_number).all()
    return render_template('vehicles/list.html', vehicles=vehs)

@app.route('/vehicles/create', methods=['GET', 'POST'])
def create_vehicle():
    if request.method == 'POST':
        reg_num = request.form.get('registration_number', '').strip()
        
        if not reg_num:
            flash('Registration number is required!', 'error')
            return render_template('vehicles/form.html')
        
        if Vehicle.query.filter_by(registration_number=reg_num).first():
            flash('Vehicle with this registration number already exists!', 'error')
            return render_template('vehicles/form.html')
        
        def get_int(val):
            try:
                return int(val) if val else None
            except:
                return None
        
        def get_date(val):
            try:
                return datetime.strptime(val, '%Y-%m-%d').date() if val else None
            except:
                return None
        
        veh = Vehicle(
            registration_number=reg_num,
            vehicle_type=request.form.get('vehicle_type', '').strip() or None,
            make=request.form.get('make', '').strip() or None,
            model=request.form.get('model', '').strip() or None,
            year=get_int(request.form.get('year')),
            color=request.form.get('color', '').strip() or None,
            fuel_type=request.form.get('fuel_type', '').strip() or None,
            engine_number=request.form.get('engine_number', '').strip() or None,
            chassis_number=request.form.get('chassis_number', '').strip() or None,
            seating_capacity=get_int(request.form.get('seating_capacity')),
            load_capacity_kg=get_int(request.form.get('load_capacity_kg')),
            owner_name=request.form.get('owner_name', '').strip() or None,
            owner_contact=request.form.get('owner_contact', '').strip() or None,
            purchase_date=get_date(request.form.get('purchase_date')),
            insurance_expiry=get_date(request.form.get('insurance_expiry')),
            fitness_expiry=get_date(request.form.get('fitness_expiry')),
            permit_expiry=get_date(request.form.get('permit_expiry')),
            notes=request.form.get('notes', '').strip() or None,
            status=request.form.get('status', 'Active')
        )
        db.session.add(veh)
        db.session.commit()
        flash('Vehicle created successfully!', 'success')
        return redirect(url_for('vehicles'))
    
    return render_template('vehicles/form.html')

@app.route('/vehicles/edit/<int:id>', methods=['GET', 'POST'])
def edit_vehicle(id):
    veh = Vehicle.query.get_or_404(id)
    if request.method == 'POST':
        reg_num = request.form.get('registration_number', '').strip()
        
        if not reg_num:
            flash('Registration number is required!', 'error')
            return render_template('vehicles/form.html', vehicle=veh, edit=True)
        
        existing = Vehicle.query.filter_by(registration_number=reg_num).first()
        if existing and existing.id != id:
            flash('Vehicle with this registration number already exists!', 'error')
            return render_template('vehicles/form.html', vehicle=veh, edit=True)
        
        def get_int(val):
            try:
                return int(val) if val else None
            except:
                return None
        
        def get_date(val):
            try:
                return datetime.strptime(val, '%Y-%m-%d').date() if val else None
            except:
                return None
        
        veh.registration_number = reg_num
        veh.vehicle_type = request.form.get('vehicle_type', '').strip() or None
        veh.make = request.form.get('make', '').strip() or None
        veh.model = request.form.get('model', '').strip() or None
        veh.year = get_int(request.form.get('year'))
        veh.color = request.form.get('color', '').strip() or None
        veh.fuel_type = request.form.get('fuel_type', '').strip() or None
        veh.engine_number = request.form.get('engine_number', '').strip() or None
        veh.chassis_number = request.form.get('chassis_number', '').strip() or None
        veh.seating_capacity = get_int(request.form.get('seating_capacity'))
        veh.load_capacity_kg = get_int(request.form.get('load_capacity_kg'))
        veh.owner_name = request.form.get('owner_name', '').strip() or None
        veh.owner_contact = request.form.get('owner_contact', '').strip() or None
        veh.purchase_date = get_date(request.form.get('purchase_date'))
        veh.insurance_expiry = get_date(request.form.get('insurance_expiry'))
        veh.fitness_expiry = get_date(request.form.get('fitness_expiry'))
        veh.permit_expiry = get_date(request.form.get('permit_expiry'))
        veh.notes = request.form.get('notes', '').strip() or None
        veh.status = request.form.get('status', 'Active')
        db.session.commit()
        flash('Vehicle updated successfully!', 'success')
        return redirect(url_for('vehicles'))
    
    return render_template('vehicles/form.html', vehicle=veh, edit=True)

@app.route('/vehicles/delete/<int:id>', methods=['POST'])
def delete_vehicle(id):
    veh = Vehicle.query.get_or_404(id)
    try:
        db.session.delete(veh)
        db.session.commit()
        flash('Vehicle deleted successfully!', 'success')
    except:
        db.session.rollback()
        flash('Cannot delete: Vehicle has associated bills!', 'error')
    return redirect(url_for('vehicles'))

# ============== TRANSPORT BILLS ==============
@app.route('/transport-bills')
def transport_bills():
    bills = TransportBill.query.order_by(TransportBill.created_at.desc()).all()
    return render_template('transport_bills/list.html', bills=bills)

@app.route('/transport-bills/create', methods=['GET', 'POST'])
def create_transport_bill():
    vehicles = Vehicle.query.order_by(Vehicle.registration_number).all()
    locations = Location.query.order_by(Location.location).all()
    delivery_types = DeliveryType.query.order_by(DeliveryType.delivery_type).all()
    
    if request.method == 'POST':
        vehicle_id = request.form.get('vehicle_id')
        bill_date = request.form.get('date')
        challan = request.form.get('challan_number', '').strip()
        party = request.form.get('party_information', '').strip()
        location_id = request.form.get('location_id') or None
        delivery_type_id = request.form.get('delivery_type_id') or None
        rate = request.form.get('rate', 0)
        
        try:
            rate = int(rate) if rate else 0
        except:
            rate = 0
        
        try:
            bill_date = datetime.strptime(bill_date, '%Y-%m-%d').date() if bill_date else date.today()
        except:
            bill_date = date.today()
        
        if vehicle_id:
            bill = TransportBill(
                name=generate_bill_name(),
                vehicle_id=vehicle_id,
                date=bill_date,
                challan_number=challan,
                party_information=party,
                location_id=location_id,
                delivery_type_id=delivery_type_id,
                rate=rate
            )
            db.session.add(bill)
            db.session.commit()
            flash(f'Transport bill {bill.name} created successfully!', 'success')
            return redirect(url_for('transport_bills'))
        else:
            flash('Vehicle is required!', 'error')
    
    return render_template('transport_bills/form.html', 
                         vehicles=vehicles, 
                         locations=locations, 
                         delivery_types=delivery_types,
                         today=date.today().isoformat())

@app.route('/transport-bills/edit/<int:id>', methods=['GET', 'POST'])
def edit_transport_bill(id):
    bill = TransportBill.query.get_or_404(id)
    vehicles = Vehicle.query.order_by(Vehicle.registration_number).all()
    locations = Location.query.order_by(Location.location).all()
    delivery_types = DeliveryType.query.order_by(DeliveryType.delivery_type).all()
    
    if request.method == 'POST':
        vehicle_id = request.form.get('vehicle_id')
        bill_date = request.form.get('date')
        challan = request.form.get('challan_number', '').strip()
        party = request.form.get('party_information', '').strip()
        location_id = request.form.get('location_id') or None
        delivery_type_id = request.form.get('delivery_type_id') or None
        rate = request.form.get('rate', 0)
        
        try:
            rate = int(rate) if rate else 0
        except:
            rate = 0
        
        try:
            bill_date = datetime.strptime(bill_date, '%Y-%m-%d').date() if bill_date else date.today()
        except:
            bill_date = date.today()
        
        if vehicle_id:
            bill.vehicle_id = vehicle_id
            bill.date = bill_date
            bill.challan_number = challan
            bill.party_information = party
            bill.location_id = location_id
            bill.delivery_type_id = delivery_type_id
            bill.rate = rate
            db.session.commit()
            flash(f'Transport bill {bill.name} updated successfully!', 'success')
            return redirect(url_for('transport_bills'))
        else:
            flash('Vehicle is required!', 'error')
    
    return render_template('transport_bills/form.html', 
                         bill=bill,
                         vehicles=vehicles, 
                         locations=locations, 
                         delivery_types=delivery_types,
                         edit=True)

@app.route('/transport-bills/delete/<int:id>', methods=['POST'])
def delete_transport_bill(id):
    bill = TransportBill.query.get_or_404(id)
    db.session.delete(bill)
    db.session.commit()
    flash('Transport bill deleted successfully!', 'success')
    return redirect(url_for('transport_bills'))

# ============== REPORTS ==============
@app.route('/reports')
def reports():
    vehicles = Vehicle.query.order_by(Vehicle.registration_number).all()
    return render_template('reports/index.html', vehicles=vehicles)

@app.route('/reports/generate', methods=['POST'])
def generate_report():
    vehicle_id = request.form.get('vehicle_id')
    from_date = request.form.get('from_date')
    to_date = request.form.get('to_date')
    export = request.form.get('export') == 'csv'
    
    query = TransportBill.query
    
    if vehicle_id:
        query = query.filter_by(vehicle_id=vehicle_id)
    
    if from_date:
        try:
            from_date = datetime.strptime(from_date, '%Y-%m-%d').date()
            query = query.filter(TransportBill.date >= from_date)
        except:
            pass
    
    if to_date:
        try:
            to_date = datetime.strptime(to_date, '%Y-%m-%d').date()
            query = query.filter(TransportBill.date <= to_date)
        except:
            pass
    
    bills = query.order_by(TransportBill.date.desc()).all()
    
    if export:
        output = io.StringIO()
        writer = csv.writer(output)
        writer.writerow(['Bill No', 'Date', 'Vehicle', 'Challan No', 'Party', 'Location', 'Delivery Type', 'Rate'])
        
        for bill in bills:
            writer.writerow([
                bill.name,
                bill.date.strftime('%Y-%m-%d') if bill.date else '',
                bill.vehicle.registration_number if bill.vehicle else '',
                bill.challan_number or '',
                bill.party_information or '',
                bill.location.location if bill.location else '',
                bill.delivery_type.delivery_type if bill.delivery_type else '',
                bill.rate
            ])
        
        output.seek(0)
        return Response(
            output.getvalue(),
            mimetype='text/csv',
            headers={'Content-Disposition': 'attachment; filename=transport_report.csv'}
        )
    
    vehicles = Vehicle.query.order_by(Vehicle.registration_number).all()
    return render_template('reports/index.html', bills=bills, vehicles=vehicles, 
                         filter_vehicle=vehicle_id, filter_from=from_date, filter_to=to_date)

# ============== EXPENSES ==============
@app.route('/expenses')
def expenses():
    expenses_list = Expense.query.order_by(Expense.expense_date.desc()).all()
    total_expenses = db.session.query(db.func.sum(Expense.amount)).scalar() or 0
    return render_template('expenses/list.html', expenses=expenses_list, total_expenses=total_expenses)

@app.route('/expenses/create', methods=['GET', 'POST'])
def create_expense():
    vehicles = Vehicle.query.order_by(Vehicle.registration_number).all()
    locations = Location.query.order_by(Location.location).all()
    categories = ['Fuel', 'Maintenance', 'Insurance', 'Tolls', 'Driver Salary', 'Spare Parts', 'Tyres', 'Lubricants', 'Car Wash', 'Parking', 'Fine/Penalty', 'Other']
    vendors = Vendor.query.filter_by(status='active').order_by(Vendor.vendor_name).all()
    
    if request.method == 'POST':
        def get_float(val):
            try:
                return float(val) if val else 0
            except:
                return 0
        
        def get_date(val):
            try:
                return datetime.strptime(val, '%Y-%m-%d').date() if val else date.today()
            except:
                return date.today()
        
        category = request.form.get('category', '').strip()
        amount = get_float(request.form.get('amount'))
        
        if not category or amount <= 0:
            flash('Category and valid amount are required!', 'error')
            return render_template('expenses/form.html', vehicles=vehicles, locations=locations, categories=categories, vendors=vendors, today=date.today().isoformat())
        
        expense = Expense(
            name=generate_expense_name(),
            expense_date=get_date(request.form.get('expense_date')),
            category=category,
            description=request.form.get('description', '').strip() or None,
            amount=amount,
            vehicle_id=request.form.get('vehicle_id') or None,
            location_id=request.form.get('location_id') or None,
            payment_method=request.form.get('payment_method', 'Cash'),
            vendor_id=request.form.get('vendor_id') or None,
            vendor_address_id=request.form.get('vendor_address_id') or None,
            vendor_name=request.form.get('vendor_name', '').strip() or None,
            vendor_contact=request.form.get('vendor_contact', '').strip() or None,
            bill_number=request.form.get('bill_number', '').strip() or None,
            notes=request.form.get('notes', '').strip() or None,
            status=request.form.get('status', 'Pending')
        )
        db.session.add(expense)
        db.session.commit()
        flash(f'Expense {expense.name} added successfully!', 'success')
        return redirect(url_for('expenses'))
    
    return render_template('expenses/form.html', 
                         vehicles=vehicles,
                         locations=locations,
                         categories=categories,
                         vendors=vendors,
                         today=date.today().isoformat())

@app.route('/expenses/edit/<int:id>', methods=['GET', 'POST'])
def edit_expense(id):
    expense = Expense.query.get_or_404(id)
    vehicles = Vehicle.query.order_by(Vehicle.registration_number).all()
    locations = Location.query.order_by(Location.location).all()
    categories = ['Fuel', 'Maintenance', 'Insurance', 'Tolls', 'Driver Salary', 'Spare Parts', 'Tyres', 'Lubricants', 'Car Wash', 'Parking', 'Fine/Penalty', 'Other']
    vendors = Vendor.query.filter_by(status='active').order_by(Vendor.vendor_name).all()
    
    if request.method == 'POST':
        def get_float(val):
            try:
                return float(val) if val else 0
            except:
                return 0
        
        def get_date(val):
            try:
                return datetime.strptime(val, '%Y-%m-%d').date() if val else date.today()
            except:
                return date.today()
        
        category = request.form.get('category', '').strip()
        amount = get_float(request.form.get('amount'))
        
        if not category or amount <= 0:
            flash('Category and valid amount are required!', 'error')
            return render_template('expenses/form.html', expense=expense, vehicles=vehicles, locations=locations, categories=categories, vendors=vendors, edit=True)
        
        expense.expense_date = get_date(request.form.get('expense_date'))
        expense.category = category
        expense.description = request.form.get('description', '').strip() or None
        expense.amount = amount
        expense.vehicle_id = request.form.get('vehicle_id') or None
        expense.location_id = request.form.get('location_id') or None
        expense.payment_method = request.form.get('payment_method', 'Cash')
        expense.vendor_id = request.form.get('vendor_id') or None
        expense.vendor_address_id = request.form.get('vendor_address_id') or None
        expense.vendor_name = request.form.get('vendor_name', '').strip() or None
        expense.vendor_contact = request.form.get('vendor_contact', '').strip() or None
        expense.bill_number = request.form.get('bill_number', '').strip() or None
        expense.notes = request.form.get('notes', '').strip() or None
        expense.status = request.form.get('status', 'Pending')
        db.session.commit()
        flash(f'Expense {expense.name} updated successfully!', 'success')
        return redirect(url_for('expenses'))
    
    return render_template('expenses/form.html', 
                         expense=expense,
                         vehicles=vehicles,
                         locations=locations,
                         categories=categories,
                         vendors=vendors,
                         edit=True)

@app.route('/expenses/delete/<int:id>', methods=['POST'])
def delete_expense(id):
    expense = Expense.query.get_or_404(id)
    name = expense.name
    db.session.delete(expense)
    db.session.commit()
    flash(f'Expense {name} deleted successfully!', 'success')
    return redirect(url_for('expenses'))

# ============== LOANS ==============
@app.route('/loans')
def loans():
    loans_list = Loan.query.order_by(Loan.created_at.desc()).all()
    total_principal = db.session.query(db.func.sum(Loan.principal_amount)).scalar() or 0
    total_balance = db.session.query(db.func.sum(Loan.balance_amount)).scalar() or 0
    return render_template('loans/list.html', loans=loans_list, total_principal=total_principal, total_balance=total_balance)

@app.route('/loans/create', methods=['GET', 'POST'])
def create_loan():
    vehicles = Vehicle.query.order_by(Vehicle.registration_number).all()
    loan_types = ['Truck Loan', 'Body Loan']
    lender_types = ['Bank', 'NBFC', 'Private', 'Individual']
    
    if request.method == 'POST':
        def get_float(val):
            try:
                return float(val) if val else 0
            except:
                return 0
        
        def get_int(val):
            try:
                return int(val) if val else 0
            except:
                return 0
        
        def get_date(val):
            try:
                return datetime.strptime(val, '%Y-%m-%d').date() if val else None
            except:
                return None
        
        vehicle_id = request.form.get('vehicle_id')
        loan_type = request.form.get('loan_type', '').strip()
        
        if not vehicle_id or not loan_type:
            flash('Vehicle and Loan Type are required!', 'error')
            return render_template('loans/form.html', vehicles=vehicles, loan_types=loan_types, lender_types=lender_types, today=date.today().isoformat())
        
        # Calculate loan details
        principal = get_float(request.form.get('principal_amount'))
        interest_rate = get_float(request.form.get('interest_rate'))
        tenure = get_int(request.form.get('tenure_months'))
        down_payment = get_float(request.form.get('down_payment'))
        
        # Calculate EMI using standard formula: P * r * (1+r)^n / ((1+r)^n - 1)
        monthly_rate = interest_rate / 12 / 100
        if monthly_rate > 0 and tenure > 0:
            emi = principal * monthly_rate * ((1 + monthly_rate) ** tenure) / (((1 + monthly_rate) ** tenure) - 1)
            total_payable = emi * tenure
            total_interest = total_payable - principal
        else:
            emi = principal / tenure if tenure > 0 else 0
            total_payable = principal
            total_interest = 0
        
        balance = total_payable - down_payment
        
        loan = Loan(
            name=generate_loan_name(),
            loan_type=loan_type,
            vehicle_id=vehicle_id,
            principal_amount=principal,
            interest_rate=interest_rate,
            tenure_months=tenure,
            emi_amount=emi,
            total_payable=total_payable,
            total_interest=total_interest,
            lender_name=request.form.get('lender_name', '').strip() or None,
            lender_type=request.form.get('lender_type', '').strip() or None,
            lender_contact=request.form.get('lender_contact', '').strip() or None,
            lender_address=request.form.get('lender_address', '').strip() or None,
            agent_name=request.form.get('agent_name', '').strip() or None,
            agent_contact=request.form.get('agent_contact', '').strip() or None,
            loan_date=get_date(request.form.get('loan_date')) or date.today(),
            disbursement_date=get_date(request.form.get('disbursement_date')),
            first_emi_date=get_date(request.form.get('first_emi_date')),
            down_payment=down_payment,
            amount_paid=down_payment,
            balance_amount=balance,
            next_emi_due_date=get_date(request.form.get('first_emi_date')),
            loan_account_number=request.form.get('loan_account_number', '').strip() or None,
            purpose=request.form.get('purpose', '').strip() or None,
            collateral=request.form.get('collateral', '').strip() or None,
            insurance_details=request.form.get('insurance_details', '').strip() or None,
            remarks=request.form.get('remarks', '').strip() or None,
            status=request.form.get('status', 'Active')
        )
        db.session.add(loan)
        db.session.commit()
        flash(f'Loan {loan.name} created successfully! EMI: Rs. {emi:.2f}', 'success')
        return redirect(url_for('loans'))
    
    return render_template('loans/form.html', vehicles=vehicles, loan_types=loan_types, lender_types=lender_types, today=date.today().isoformat())

@app.route('/loans/edit/<int:id>', methods=['GET', 'POST'])
def edit_loan(id):
    loan = Loan.query.get_or_404(id)
    vehicles = Vehicle.query.order_by(Vehicle.registration_number).all()
    loan_types = ['Truck Loan', 'Body Loan']
    lender_types = ['Bank', 'NBFC', 'Private', 'Individual']
    
    if request.method == 'POST':
        def get_float(val):
            try:
                return float(val) if val else 0
            except:
                return 0
        
        def get_int(val):
            try:
                return int(val) if val else 0
            except:
                return 0
        
        def get_date(val):
            try:
                return datetime.strptime(val, '%Y-%m-%d').date() if val else None
            except:
                return None
        
        loan.loan_type = request.form.get('loan_type', '').strip()
        loan.vehicle_id = request.form.get('vehicle_id')
        
        # Recalculate if principal/interest/tenure changed
        principal = get_float(request.form.get('principal_amount'))
        interest_rate = get_float(request.form.get('interest_rate'))
        tenure = get_int(request.form.get('tenure_months'))
        
        monthly_rate = interest_rate / 12 / 100
        if monthly_rate > 0 and tenure > 0:
            emi = principal * monthly_rate * ((1 + monthly_rate) ** tenure) / (((1 + monthly_rate) ** tenure) - 1)
            total_payable = emi * tenure
            total_interest = total_payable - principal
        else:
            emi = principal / tenure if tenure > 0 else 0
            total_payable = principal
            total_interest = 0
        
        loan.principal_amount = principal
        loan.interest_rate = interest_rate
        loan.tenure_months = tenure
        loan.emi_amount = emi
        loan.total_payable = total_payable
        loan.total_interest = total_interest
        loan.lender_name = request.form.get('lender_name', '').strip() or None
        loan.lender_type = request.form.get('lender_type', '').strip() or None
        loan.lender_contact = request.form.get('lender_contact', '').strip() or None
        loan.lender_address = request.form.get('lender_address', '').strip() or None
        loan.agent_name = request.form.get('agent_name', '').strip() or None
        loan.agent_contact = request.form.get('agent_contact', '').strip() or None
        loan.loan_date = get_date(request.form.get('loan_date')) or loan.loan_date
        loan.disbursement_date = get_date(request.form.get('disbursement_date'))
        loan.first_emi_date = get_date(request.form.get('first_emi_date'))
        loan.loan_account_number = request.form.get('loan_account_number', '').strip() or None
        loan.purpose = request.form.get('purpose', '').strip() or None
        loan.collateral = request.form.get('collateral', '').strip() or None
        loan.insurance_details = request.form.get('insurance_details', '').strip() or None
        loan.remarks = request.form.get('remarks', '').strip() or None
        loan.status = request.form.get('status', 'Active')
        
        db.session.commit()
        flash(f'Loan {loan.name} updated successfully!', 'success')
        return redirect(url_for('loans'))
    
    return render_template('loans/form.html', loan=loan, vehicles=vehicles, loan_types=loan_types, lender_types=lender_types, edit=True)

@app.route('/loans/delete/<int:id>', methods=['POST'])
def delete_loan(id):
    loan = Loan.query.get_or_404(id)
    name = loan.name
    db.session.delete(loan)
    db.session.commit()
    flash(f'Loan {name} deleted successfully!', 'success')
    return redirect(url_for('loans'))

if __name__ == '__main__':
    app.run(debug=True, port=5000)
"""

from webapp import app, db


if __name__ == "__main__":
    app.run(debug=True, port=5000)
