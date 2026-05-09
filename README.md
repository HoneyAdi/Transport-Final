# Transport Management System - Flask Edition

A standalone Flask-based transport management system replicating all features from the original Frappe/ERPNext app and uses MySQL by default.

## Features

- **Delivery Types** - Master data management
- **Locations** - Route locations with rates
- **Vehicles** - Vehicle registration management
- **Transport Bills** - Core challan/bill generation with auto-rate fetch
- **Reports** - Filter by vehicle and date range, CSV export

## Quick Start

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Initialize database with sample data:**
   ```bash
   python init_db.py
   ```

3. **Run the application:**
   ```bash
   python webapp.py
   ```

4. **Open in browser:**
   http://localhost:5000

5. **Login with seeded accounts:**
   - `superadmin` / `SuperAdmin@123`
   - `tenant` / `Tenant@123`

## Original vs Flask Version

| Feature | Original (Frappe) | Flask Version |
|---------|-------------------|---------------|
| Framework | Frappe/ERPNext | Flask + SQLAlchemy |
| Database | MariaDB | MySQL |
| Vehicle | Linked to ERPNext Vehicle | Standalone Vehicle model |
| Lead extensions | Custom fields on Lead | Not included (pre-sales feature) |
| Auto-numbering | TBG-.##### | ✅ Same format |
| Auto-fetch rate | From location.rate | ✅ JavaScript + API |
| Report filters | Vehicle, Date Range | ✅ Same filters |
| CSV Export | Available | ✅ Implemented |

## Project Structure

```
Transport/
├── webapp.py               # Main Flask application
├── models.py               # SQLAlchemy models
├── init_db.py              # Sample data initialization
├── requirements.txt        # Python dependencies
├── templates/
│   ├── base.html           # Base layout with sidebar
│   ├── dashboard.html      # Dashboard with stats
│   ├── delivery_types/
│   │   ├── list.html
│   │   └── form.html
│   ├── locations/
│   │   ├── list.html
│   │   └── form.html
│   ├── vehicles/
│   │   ├── list.html
│   │   └── form.html
│   ├── transport_bills/
│   │   ├── list.html
│   │   └── form.html
│   └── reports/
│       └── index.html
└── .env                    # MySQL credentials used by the app
```

## Usage

1. **Setup Master Data:**
   - Add Delivery Types
   - Add Locations with rates
   - Add Vehicles

2. **Create Transport Bills:**
   - Select Vehicle
   - Enter Challan Number
   - Enter Party Information
   - Select Location (auto-fetches rate)
   - Select Delivery Type
   - Confirm/Adjust Rate
   - Save

3. **Generate Reports:**
   - Filter by Vehicle
   - Filter by Date Range
   - View results or Export to CSV
