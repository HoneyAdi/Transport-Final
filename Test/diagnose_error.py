#!/usr/bin/env python3
"""Diagnostic script to check for import errors"""
import sys
import os
import traceback

os.chdir(r'E:\PROJECTS\Transport')
os.environ['AUTO_MIGRATE'] = 'false'

log = []

def log_msg(msg):
    print(msg)
    log.append(msg)

try:
    log_msg("Step 1: Importing models...")
    from models import Vendor, VendorAddress, app, db
    log_msg("  OK - models imported")
    
    log_msg("Step 2: Importing webapp...")
    import webapp
    log_msg("  OK - webapp imported")
    
    log_msg("\nAll imports successful!")
    
except Exception as e:
    log_msg(f"\nERROR: {type(e).__name__}: {e}")
    log_msg("\nTraceback:")
    log_msg(traceback.format_exc())

# Write to file
with open('diagnose_result.txt', 'w', encoding='utf-8') as f:
    f.write('\n'.join(log))
