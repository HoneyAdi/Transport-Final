# PowerShell script to run migration
$ErrorActionPreference = "Stop"

Set-Location -Path "E:\PROJECTS\Transport"

Write-Host "Clearing Python cache..." -ForegroundColor Cyan
Remove-Item -Path "__pycache__" -Recurse -Force -ErrorAction SilentlyContinue
Get-ChildItem -Path "." -Recurse -Filter "*.pyc" | Remove-Item -Force -ErrorAction SilentlyContinue
Get-ChildItem -Path "." -Recurse -Filter "__pycache__" -Directory | Remove-Item -Recurse -Force -ErrorAction SilentlyContinue

Write-Host "Running migration..." -ForegroundColor Green
python migrate_vendor_addresses.py

Write-Host "Done!" -ForegroundColor Green
