#!/usr/bin/env python3
"""Fix any issues in webapp.py and check for syntax errors"""

import ast
import sys

# Read the file
with open('webapp.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Check for @login_required decorator
if '@login_required' in content:
    print("Found @login_required decorator, removing...")
    content = content.replace('@login_required\n', '')
    content = content.replace('@login_required\r\n', '')
    with open('webapp.py', 'w', encoding='utf-8') as f:
        f.write(content)
    print("Removed @login_required decorators")

# Check syntax
try:
    ast.parse(content)
    print("Syntax check: OK")
except SyntaxError as e:
    print(f"Syntax error at line {e.lineno}: {e.msg}")
    print(f"Line content: {e.text}")
    sys.exit(1)

print("webapp.py is valid")
