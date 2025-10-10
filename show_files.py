#!/usr/bin/env python3
"""
Показать все файлы для загрузки в GitHub
"""

import os
from pathlib import Path

def show_deploy_files():
    """Показать файлы для деплоя"""
    print("=" * 60)
    print("ФАЙЛЫ ДЛЯ ЗАГРУЗКИ В GITHUB")
    print("=" * 60)
    
    # Основные файлы для деплоя
    deploy_files = [
        'render_bot.py',
        'config.py', 
        'requirements.txt',
        'Procfile',
        'runtime.txt',
        '.gitignore'
    ]
    
    # Дополнительные файлы
    extra_files = [
        'telegram_bot.py',
        'test_simple.py',
        'README.md',
        'HOSTING.md',
        'RENDER_DEPLOY.md'
    ]
    
    print("\nОСНОВНЫЕ ФАЙЛЫ (ОБЯЗАТЕЛЬНО):")
    print("-" * 40)
    for file in deploy_files:
        if os.path.exists(file):
            size = os.path.getsize(file)
            print(f"✅ {file} ({size} байт)")
        else:
            print(f"❌ {file} - НЕ НАЙДЕН!")
    
    print("\nДОПОЛНИТЕЛЬНЫЕ ФАЙЛЫ (ОПЦИОНАЛЬНО):")
    print("-" * 40)
    for file in extra_files:
        if os.path.exists(file):
            size = os.path.getsize(file)
            print(f"✅ {file} ({size} байт)")
        else:
            print(f"⚠️  {file} - не найден (не критично)")
    
    print("\n" + "=" * 60)
    print("ИНСТРУКЦИИ ДЛЯ GITHUB DESKTOP:")
    print("=" * 60)
    print("1. Создайте репозиторий на github.com")
    print("2. Клонируйте в GitHub Desktop")
    print("3. Скопируйте ВСЕ файлы в папку репозитория")
    print("4. Сделайте commit и push")
    print("5. Деплойте на Render!")
    print("=" * 60)

def main():
    """Главная функция"""
    show_deploy_files()

if __name__ == "__main__":
    main()
