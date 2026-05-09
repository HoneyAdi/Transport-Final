@echo off
cd /d "E:\PROJECTS\Transport"

echo Initializing git (if not already)...
git init

echo Adding remote repository...
git remote remove origin 2>nul
git remote add origin https://github.com/HoneyAdi/transport.git

echo Configuring git user...
git config user.email "admin@transport.com"
git config user.name "Transport Admin"

echo Adding all files to git...
git add .

echo Committing changes...
git commit -m "Add vendor multiple addresses feature - migration, models, forms, and UI"

echo Pushing to GitHub...
git push -u origin master

echo.
echo If prompted for credentials, enter your GitHub username and password/token.
echo.
pause
