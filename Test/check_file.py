#!/usr/bin/env python3
"""Check webapp.py for syntax errors"""

with open('webapp.py', 'r', encoding='utf-8') as f:
    content = f.read()
    lines = content.split('\n')
    
print(f'Total lines: {len(lines)}')
print(f'File size: {len(content)} bytes')

# Check for syntax errors
try:
    compile(content, 'webapp.py', 'exec')
    print('Syntax: OK')
except SyntaxError as e:
    print(f'Syntax Error at line {e.lineno}: {e.text}')
    print(f'Error: {e.msg}')
