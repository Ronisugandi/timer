@echo off
echo Membuat file .exe dari timer_app.py ...
pyinstaller --onefile --windowed timer.py
echo.
echo Selesai! File .exe ada di folder "dist".
pause
