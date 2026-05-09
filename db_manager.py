"""Database Migration Manager with Auto-Migration Support"""
import os
import sys
import subprocess
from models import app, db, migrate

def init_migrations():
    """Initialize the migration environment if it doesn't exist"""
    if not os.path.exists("migrations"):
        print("Initializing migration environment...")
        with app.app_context():
            from flask_migrate import init
            init(directory="migrations")
        print("Migration environment initialized.")
    else:
        print("Migration environment already exists.")

def create_migration(message="Auto migration"):
    """Create a new migration based on model changes"""
    print(f"Creating migration: {message}")
    with app.app_context():
        from flask_migrate import migrate as migrate_cmd
        migrate_cmd(directory="migrations", message=message)
    print("Migration created.")

def upgrade_db():
    """Apply all pending migrations"""
    print("Applying migrations...")
    with app.app_context():
        from flask_migrate import upgrade
        upgrade(directory="migrations")
    print("Database upgraded successfully.")

def auto_migrate():
    """Automatically detect changes and migrate (for CI/CD or startup)"""
    init_migrations()
    
    # Check if we need an initial migration
    migration_files = []
    if os.path.exists("migrations/versions"):
        migration_files = [f for f in os.listdir("migrations/versions") if f.endswith(".py") and not f.startswith("__")]
    
    if not migration_files:
        print("Creating initial migration...")
        create_migration("Initial migration")
    else:
        print("Creating migration for any new changes...")
        create_migration("Auto migration on module change")
    
    upgrade_db()

def downgrade_db(revision="-1"):
    """Downgrade database to previous revision"""
    print(f"Downgrading database to {revision}...")
    with app.app_context():
        from flask_migrate import downgrade
        downgrade(directory="migrations", revision=revision)
    print("Database downgraded.")

def show_history():
    """Show migration history"""
    with app.app_context():
        from flask_migrate import history
        history(directory="migrations")

def show_current():
    """Show current migration version"""
    with app.app_context():
        from flask_migrate import current
        current(directory="migrations")

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Database Migration Manager")
    parser.add_argument("command", choices=[
        "init", "migrate", "upgrade", "auto", "downgrade", "history", "current"
    ], help="Command to run")
    parser.add_argument("-m", "--message", default="Auto migration", help="Migration message")
    parser.add_argument("-r", "--revision", default="-1", help="Revision for downgrade")
    
    args = parser.parse_args()
    
    if args.command == "init":
        init_migrations()
    elif args.command == "migrate":
        create_migration(args.message)
    elif args.command == "upgrade":
        upgrade_db()
    elif args.command == "auto":
        auto_migrate()
    elif args.command == "downgrade":
        downgrade_db(args.revision)
    elif args.command == "history":
        show_history()
    elif args.command == "current":
        show_current()
