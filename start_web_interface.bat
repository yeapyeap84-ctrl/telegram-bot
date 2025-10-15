@echo off
echo ========================================
echo    TELEGRAM BOT WEB INTERFACE
echo ========================================
echo.
echo Запуск веб-интерфейса для управления ботом...
echo.
echo После запуска откройте браузер и перейдите по адресу:
echo http://localhost:5000
echo.
echo Нажмите любую клавишу для запуска...
pause >nul
echo.
echo Запуск веб-интерфейса...
python web_interface.py
echo.
echo Веб-интерфейс остановлен.
pause


