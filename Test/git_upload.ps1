# Git upload script
cd E:\PROJECTS\Transport

# Initialize git if not already
git init

# Add remote
git remote remove origin 2>$null
git remote add origin https://github.com/HoneyAdi/transport.git

# Configure user
git config user.email "admin@transport.com"
git config user.name "Transport Admin"

# Add all files
git add .

# Commit
git commit -m "Add vendor multiple addresses feature - migration, models, forms, and UI" 2>$null

# Push to master branch
git push -u origin master 2>&1 | Tee-Object git_push_output.txt

Write-Host "Git operations complete. Check git_push_output.txt for details."
