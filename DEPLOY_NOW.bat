@echo off
chcp 65001 >nul
title Telegram Bot - Деплой на Render СЕЙЧАС

echo ============================================================
echo TELEGRAM BOT - ДЕПЛОЙ НА RENDER ПРЯМО СЕЙЧАС!
echo ============================================================
echo.

echo ВСЕ ФАЙЛЫ ГОТОВЫ ДЛЯ ДЕПЛОЯ!
echo.

echo ШАГ 1: СОЗДАНИЕ GITHUB РЕПОЗИТОРИЯ
echo ----------------------------------------
echo 1. Перейдите на https://github.com
echo 2. Нажмите "New repository"
echo 3. Название: telegram-bot
echo 4. Сделайте ПУБЛИЧНЫМ
echo 5. НЕ добавляйте README, .gitignore, лицензию
echo 6. Нажмите "Create repository"
echo.

echo ШАГ 2: ЗАГРУЗКА КОДА
echo ----------------------------------------
echo 1. Скачайте GitHub Desktop: https://desktop.github.com/
echo 2. Или используйте веб-интерфейс GitHub
echo 3. Загрузите ВСЕ файлы из этой папки
echo.

echo ШАГ 3: ДЕПЛОЙ НА RENDER
echo ----------------------------------------
echo 1. Перейдите на https://render.com
echo 2. Нажмите "Get Started for Free"
echo 3. Войдите через GitHub
echo 4. Нажмите "New +" -> "Web Service
echo 5. Подключите ваш репозиторий
echo.

echo ШАГ 4: НАСТРОЙКИ
echo ----------------------------------------
echo - Name: telegram-bot
echo - Environment: Python 3
echo - Build Command: pip install -r requirements.txt
echo - Start Command: python render_bot.py
echo - Environment Variable: BOT_TOKEN = 7647122248:AAG49utA8oAhwPgjUbH2qTcNiT1Akh6JdtI
echo.

echo ШАГ 5: ЗАПУСК
echo ----------------------------------------
echo 1. Нажмите "Create Web Service"
echo 2. Дождитесь завершения сборки (5-10 минут)
echo 3. Откройте URL вашего сервиса
echo.

echo ГОТОВО! Ваш бот будет работать 24/7 на Render!
echo.

echo ФАЙЛЫ ДЛЯ ЗАГРУЗКИ В GITHUB:
echo - render_bot.py
echo - config.py
echo - requirements.txt
echo - Procfile
echo - runtime.txt
echo - .gitignore
echo.

pause
