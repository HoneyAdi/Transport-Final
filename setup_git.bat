@echo off
cd /d "D:\HONEY\Projects\transport-master"
"C:\Program Files\Git\bin\git.exe" config user.name "Transport User"
"C:\Program Files\Git\bin\git.exe" config user.email "transport@example.com"
"C:\Program Files\Git\bin\git.exe" add .
"C:\Program Files\Git\bin\git.exe" commit -m "Initial commit - Transport Final"
echo Git repository ready. Now you need to create the GitHub repository and push.
echo.
echo To push to GitHub, run these commands:
echo   git remote add origin https://github.com/YOUR_USERNAME/Transport-Final.git
echo   git push -u origin main
pause
