"""
Migration script to add new columns to RateList table
Run this script to update the database schema
"""
import sys
from datetime import date
from sqlalchemy import text
from webapp import app, db

def migrate():
    with app.app_context():
        # Check if columns already exist
        inspector = db.inspect(db.engine)
        columns = [col['name'] for col in inspector.get_columns('ratelists')]
        
        migrations = []
        
        # Add party_id column if not exists
        if 'party_id' not in columns:
            migrations.append("ALTER TABLE ratelists ADD COLUMN party_id INT")
            migrations.append("ALTER TABLE ratelists ADD INDEX ix_ratelists_party_id (party_id)")
            migrations.append("ALTER TABLE ratelists ADD FOREIGN KEY (party_id) REFERENCES vendors(id)")
        
        # Add vehicle-specific rate columns if not exist
        vehicle_columns = ['rate_14ft', 'rate_17ft', 'rate_t5_1109', 'rate_19ft', 'rate_22ft', 'rate_32ft']
        for col in vehicle_columns:
            if col not in columns:
                migrations.append(f"ALTER TABLE ratelists ADD COLUMN {col} DECIMAL(10, 2)")
        
        # Add effective_date column if not exists
        if 'effective_date' not in columns:
            migrations.append("ALTER TABLE ratelists ADD COLUMN effective_date DATE")
        
        if migrations:
            print("Running migrations...")
            for migration in migrations:
                print(f"  Executing: {migration}")
                db.session.execute(text(migration))
            db.session.commit()
            print("Migration completed successfully!")
        else:
            print("All columns already exist. No migration needed.")
        
        # Update existing records with default effective_date
        if 'effective_date' in columns:
            result = db.session.execute(text("UPDATE ratelists SET effective_date = :today WHERE effective_date IS NULL"), 
                                      {"today": date.today()})
            db.session.commit()
            print(f"Updated {result.rowcount} records with effective_date")

if __name__ == "__main__":
    migrate()
