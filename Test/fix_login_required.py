#!/usr/bin/env python
"""Script to remove @login_required decorator from webapp.py"""

with open('webapp.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Check for @login_required followed by the API route
if '@login_required\n@app.route("/api/vendors/<int:vendor_id>/addresses")' in content:
    print("Found @login_required decorator, removing it...")
    content = content.replace(
        '@login_required\n@app.route("/api/vendors/<int:vendor_id>/addresses")',
        '@app.route("/api/vendors/<int:vendor_id>/addresses")'
    )
    with open('webapp.py', 'w', encoding='utf-8') as f:
        f.write(content)
    print("Fixed!")
else:
    print("@login_required decorator not found (or already fixed)")

# Also check any other @login_required instances
lines = content.split('\n')
for i, line in enumerate(lines, 1):
    if '@login_required' in line:
        print(f"Found @login_required at line {i}: {line}")
