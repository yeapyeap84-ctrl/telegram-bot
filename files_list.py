#!/usr/bin/env python3
"""
Список файлов для GitHub
"""

import os

def main():
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
    
    print("\nОСНОВНЫЕ ФАЙЛЫ (ОБЯЗАТЕЛЬНО):")
    print("-" * 40)
    for file in deploy_files:
        if os.path.exists(file):
            size = os.path.getsize(file)
            print(f"OK {file} ({size} байт)")
        else:
            print(f"ERROR {file} - НЕ НАЙДЕН!")
    
    print("\n" + "=" * 60)
    print("ИНСТРУКЦИИ:")
    print("=" * 60)
    print("1. Создайте репозиторий на github.com")
    print("2. Клонируйте в GitHub Desktop")
    print("3. Скопируйте ВСЕ файлы в папку репозитория")
    print("4. Сделайте commit и push")
    print("5. Деплойте на Render!")
    print("=" * 60)

if __name__ == "__main__":
    main()
