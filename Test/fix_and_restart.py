#!/usr/bin/env python3
"""Fix issues and restart the server"""

import os
import sys
import subprocess
import time

os.chdir(r'E:\PROJECTS\Transport')

print("=" * 60)
print("FIX AND RESTART SERVER")
print("=" * 60)

# Step 1: Clear Python cache
print("\n[1] Clearing Python cache...")
import shutil
for root, dirs, files in os.walk('.'):
    for d in dirs:
        if d == '__pycache__':
            path = os.path.join(root, d)
            try:
                shutil.rmtree(path)
                print(f"  Removed: {path}")
            except:
                pass
    for f in files:
        if f.endswith('.pyc') or f.endswith('.pyo'):
            path = os.path.join(root, f)
            try:
                os.remove(path)
            except:
                pass
print("  Cache cleared")

# Step 2: Check and fix webapp.py
print("\n[2] Checking webapp.py...")
with open('webapp.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Remove @login_required if present
if '@login_required' in content:
    print("  Found @login_required, removing...")
    content = content.replace('@login_required\n@app.route("/api/vendors/<int:vendor_id>/addresses")', 
                              '@app.route("/api/vendors/<int:vendor_id>/addresses")')
    content = content.replace('@login_required\r\n@app.route("/api/vendors/<int:vendor_id>/addresses")', 
                              '@app.route("/api/vendors/<int:vendor_id>/addresses")')
    with open('webapp.py', 'w', encoding='utf-8') as f:
        f.write(content)
    print("  Fixed @login_required")
else:
    print("  No @login_required found")

# Step 3: Check syntax
print("\n[3] Checking Python syntax...")
import ast
try:
    ast.parse(content)
    print("  webapp.py syntax: OK")
except SyntaxError as e:
    print(f"  ERROR in webapp.py at line {e.lineno}: {e.msg}")
    sys.exit(1)

# Check models.py
with open('models.py', 'r', encoding='utf-8') as f:
    models_content = f.read()
try:
    ast.parse(models_content)
    print("  models.py syntax: OK")
except SyntaxError as e:
    print(f"  ERROR in models.py at line {e.lineno}: {e.msg}")
    sys.exit(1)

# Step 4: Test imports
print("\n[4] Testing imports...")
os.environ['AUTO_MIGRATE'] = 'false'
try:
    from models import Vendor, VendorAddress, app, db
    print("  models import: OK")
except Exception as e:
    print(f"  ERROR importing models: {e}")
    sys.exit(1)

try:
    import webapp
    print("  webapp import: OK")
except Exception as e:
    print(f"  ERROR importing webapp: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

print("\n" + "=" * 60)
print("ALL CHECKS PASSED!")
print("=" * 60)
print("\nYou can now start the server with:")
print("  $env:AUTO_MIGRATE=\"false\"")
print("  $env:FLASK_APP=\"webapp.py\"")
print("  flask run --host=0.0.0.0 --port=5000")
