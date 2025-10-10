@echo off
chcp 65001 >nul
title Telegram Bot - Автоматическая публикация постов

echo ============================================================
echo 🤖 TELEGRAM BOT - АВТОМАТИЧЕСКАЯ ПУБЛИКАЦИЯ ПОСТОВ
echo ============================================================
echo.

REM Проверяем наличие Python
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python не найден! Установите Python 3.8+ с python.org
    pause
    exit /b 1
)

REM Проверяем наличие pip
pip --version >nul 2>&1
if errorlevel 1 (
    echo ❌ pip не найден! Установите pip
    pause
    exit /b 1
)

echo ✅ Python найден
echo.

REM Устанавливаем зависимости
echo 📦 Установка зависимостей...
pip install -r requirements.txt
if errorlevel 1 (
    echo ❌ Ошибка установки зависимостей
    pause
    exit /b 1
)

echo ✅ Зависимости установлены
echo.

REM Запускаем основной скрипт
echo 🚀 Запуск бота...
python start.py

pause

