@echo off
chcp 65001 >nul
title Telegram Bot - ФИНАЛЬНАЯ ИНСТРУКЦИЯ

echo ============================================================
echo TELEGRAM BOT - ФИНАЛЬНАЯ ИНСТРУКЦИЯ
echo ============================================================
echo.

echo ВСЕ ФАЙЛЫ ГОТОВЫ ДЛЯ ДЕПЛОЯ!
echo.

echo ОСНОВНЫЕ ФАЙЛЫ:
echo - render_bot.py (14684 байт) - основной бот
echo - config.py (2037 байт) - конфигурация с каналами
echo - requirements.txt (114 байт) - зависимости
echo - Procfile (27 байт) - команда запуска
echo - runtime.txt (15 байт) - версия Python
echo - .gitignore (440 байт) - исключения
echo.

echo СЕЙЧАС ДЕЛАЙТЕ ТАК:
echo.

echo ШАГ 1: СОЗДАНИЕ GITHUB РЕПОЗИТОРИЯ
echo ----------------------------------------
echo 1. Идите на https://github.com
echo 2. Нажмите "New repository"
echo 3. Название: telegram-bot
echo 4. Сделайте ПУБЛИЧНЫМ
echo 5. НЕ добавляйте README, .gitignore, лицензию
echo 6. Нажмите "Create repository"
echo 7. Скопируйте URL репозитория
echo.

echo ШАГ 2: КЛОНИРОВАНИЕ В GITHUB DESKTOP
echo ----------------------------------------
echo 1. Откройте GitHub Desktop
echo 2. Нажмите "Clone a repository from the Internet"
echo 3. Вставьте URL вашего репозитория
echo 4. Выберите папку: C:\Users\admin\Desktop\
echo 5. Нажмите "Clone"
echo.

echo ШАГ 3: КОПИРОВАНИЕ ФАЙЛОВ
echo ----------------------------------------
echo Скопируйте ВСЕ эти файлы в папку репозитория:
echo - render_bot.py
echo - config.py
echo - requirements.txt
echo - Procfile
echo - runtime.txt
echo - .gitignore
echo.

echo ШАГ 4: КОММИТ И ПУШ
echo ----------------------------------------
echo 1. В GitHub Desktop вы увидите все файлы
echo 2. Напишите commit message: "Initial commit - Telegram Bot"
echo 3. Нажмите "Commit to main"
echo 4. Нажмите "Push origin"
echo.

echo ШАГ 5: ДЕПЛОЙ НА RENDER
echo ----------------------------------------
echo 1. Идите на https://render.com
echo 2. Нажмите "Get Started for Free"
echo 3. Войдите через GitHub
echo 4. Нажмите "New +" -> "Web Service"
echo 5. Подключите ваш репозиторий
echo.

echo ШАГ 6: НАСТРОЙКИ RENDER
echo ----------------------------------------
echo - Name: telegram-bot
echo - Environment: Python 3
echo - Build Command: pip install -r requirements.txt
echo - Start Command: python render_bot.py
echo - Environment Variable: BOT_TOKEN = 7647122248:AAG49utA8oAhwPgjUbH2qTcNiT1Akh6JdtI
echo.

echo ШАГ 7: ЗАПУСК
echo ----------------------------------------
echo 1. Нажмите "Create Web Service"
echo 2. Дождитесь завершения сборки (5-10 минут)
echo 3. Откройте URL вашего сервиса
echo.

echo ГОТОВО! Ваш бот будет работать 24/7 на Render!
echo.

pause
