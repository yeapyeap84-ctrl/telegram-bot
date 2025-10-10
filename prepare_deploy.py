#!/usr/bin/env python3
"""
Подготовка файлов для деплоя на Render
"""

import os
import shutil

def create_deploy_files():
    """Создание всех необходимых файлов для деплоя"""
    print("Подготовка файлов для деплоя на Render...")
    
    # Список файлов для деплоя
    deploy_files = [
        'render_bot.py',
        'config.py', 
        'requirements.txt',
        'Procfile',
        'runtime.txt',
        '.gitignore'
    ]
    
    # Проверяем наличие файлов
    missing_files = []
    for file in deploy_files:
        if not os.path.exists(file):
            missing_files.append(file)
    
    if missing_files:
        print(f"Отсутствуют файлы: {', '.join(missing_files)}")
        return False
    
    print("Все необходимые файлы готовы!")
    return True

def show_deploy_instructions():
    """Показать инструкции по деплою"""
    print("\n" + "=" * 60)
    print("ИНСТРУКЦИИ ДЛЯ ДЕПЛОЯ НА RENDER")
    print("=" * 60)
    print()
    print("1. СОЗДАНИЕ GITHUB РЕПОЗИТОРИЯ:")
    print("   - Перейдите на https://github.com")
    print("   - Нажмите 'New repository'")
    print("   - Название: telegram-bot")
    print("   - Сделайте ПУБЛИЧНЫМ")
    print("   - НЕ добавляйте README, .gitignore, лицензию")
    print("   - Нажмите 'Create repository'")
    print()
    print("2. ЗАГРУЗКА КОДА:")
    print("   - Скачайте GitHub Desktop: https://desktop.github.com/")
    print("   - Или используйте веб-интерфейс GitHub")
    print("   - Загрузите все файлы из этой папки")
    print()
    print("3. ДЕПЛОЙ НА RENDER:")
    print("   - Перейдите на https://render.com")
    print("   - Нажмите 'Get Started for Free'")
    print("   - Войдите через GitHub")
    print("   - Нажмите 'New +' -> 'Web Service'")
    print("   - Подключите ваш репозиторий")
    print()
    print("4. НАСТРОЙКИ:")
    print("   - Name: telegram-bot")
    print("   - Environment: Python 3")
    print("   - Build Command: pip install -r requirements.txt")
    print("   - Start Command: python render_bot.py")
    print("   - Environment Variable: BOT_TOKEN = 7647122248:AAG49utA8oAhwPgjUbH2qTcNiT1Akh6JdtI")
    print()
    print("5. ЗАПУСК:")
    print("   - Нажмите 'Create Web Service'")
    print("   - Дождитесь завершения сборки (5-10 минут)")
    print("   - Откройте URL вашего сервиса")
    print()
    print("ГОТОВО! Ваш бот будет работать 24/7 на Render! 🚀")

def main():
    """Главная функция"""
    print("=" * 60)
    print("ПОДГОТОВКА ДЕПЛОЯ НА RENDER")
    print("=" * 60)
    
    if create_deploy_files():
        show_deploy_instructions()
    else:
        print("Ошибка при подготовке файлов")

if __name__ == "__main__":
    main()
