@echo off
cd /d c:\Users\Admins\Documents\记账
git add .
git commit -m "Initial commit"
echo.
echo ====== Commit status ======
git log --oneline
echo.
echo Done!
pause
