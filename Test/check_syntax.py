#!/usr/bin/env python
import py_compile
import sys

try:
    py_compile.compile('webapp.py', doraise=True)
    print("Syntax OK")
    sys.exit(0)
except Exception as e:
    print(f"Syntax Error: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
