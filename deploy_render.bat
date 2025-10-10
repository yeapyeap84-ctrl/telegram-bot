@echo off
chcp 65001 >nul
title Telegram Bot - Деплой на Render

echo ============================================================
echo TELEGRAM BOT - ДЕПЛОЙ НА RENDER.COM
echo ============================================================
echo.
echo Этот скрипт поможет вам развернуть бота на бесплатном хостинге Render
echo.

py deploy_render.py

pause
