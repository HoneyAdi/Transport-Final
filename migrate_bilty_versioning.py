"""
Add versioning fields to transport_bills table
"""
from webapp import app, db
from sqlalchemy import text

def migrate_bilty_versioning():
    with app.app_context():
        with db.engine.begin() as connection:
            # Add new columns for versioning
            print("Adding versioning columns to transport_bills table...")
            
            # Remove unique constraint from name and gr_number to allow versions
            try:
                connection.execute(text("ALTER TABLE transport_bills DROP INDEX ix_transport_bills_name"))
                connection.execute(text("ALTER TABLE transport_bills DROP INDEX ix_transport_bills_gr_number"))
            except Exception as e:
                print(f"Note: Indexes may not exist or already removed: {e}")
            
            # Add versioning columns
            connection.execute(text("ALTER TABLE transport_bills ADD COLUMN parent_id INT NULL"))
            connection.execute(text("ALTER TABLE transport_bills ADD INDEX ix_transport_bills_parent_id (parent_id)"))
            connection.execute(text("ALTER TABLE transport_bills ADD FOREIGN KEY (parent_id) REFERENCES transport_bills(id)"))
            
            connection.execute(text("ALTER TABLE transport_bills ADD COLUMN version_number INT DEFAULT 1"))
            connection.execute(text("ALTER TABLE transport_bills ADD COLUMN is_original BOOLEAN DEFAULT TRUE"))
            connection.execute(text("ALTER TABLE transport_bills ADD COLUMN modification_reason TEXT NULL"))
            
            print("Migration completed successfully!")

if __name__ == "__main__":
    migrate_bilty_versioning()
