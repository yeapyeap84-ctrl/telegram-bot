#!/usr/bin/env python3
"""
Быстрый деплой на Render - БЕЗ ЭМОДЗИ
"""

import os
import subprocess
import sys

def check_git():
    """Проверка Git"""
    try:
        result = subprocess.run(['git', '--version'], capture_output=True, text=True)
        if result.returncode == 0:
            print("Git установлен")
            return True
        else:
            print("Git не найден")
            return False
    except FileNotFoundError:
        print("Git не установлен")
        return False

def init_git_repo():
    """Инициализация Git репозитория"""
    print("Инициализация Git репозитория...")
    
    try:
        # Проверяем, есть ли уже Git репозиторий
        if os.path.exists('.git'):
            print("Git репозиторий уже существует")
            return True
        
        # Инициализируем Git
        subprocess.run(['git', 'init'], check=True)
        print("Git репозиторий инициализирован")
        
        # Добавляем все файлы
        subprocess.run(['git', 'add', '.'], check=True)
        print("Файлы добавлены в Git")
        
        # Первый коммит
        subprocess.run(['git', 'commit', '-m', 'Initial commit - Telegram Bot'], check=True)
        print("Первый коммит создан")
        
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"Ошибка при инициализации Git: {e}")
        return False

def main():
    """Главная функция"""
    print("=" * 60)
    print("ДЕПЛОЙ TELEGRAM БОТА НА RENDER.COM")
    print("=" * 60)
    
    # Проверяем Git
    if not check_git():
        print("\nУстановите Git и попробуйте снова")
        print("Скачать Git: https://git-scm.com/downloads")
        return
    
    # Инициализируем Git репозиторий
    if not init_git_repo():
        print("\nНе удалось инициализировать Git репозиторий")
        return
    
    print("\nИНСТРУКЦИИ ДЛЯ СОЗДАНИЯ GITHUB РЕПОЗИТОРИЯ:")
    print("=" * 60)
    print("1. Перейдите на https://github.com")
    print("2. Нажмите 'New repository'")
    print("3. Назовите репозиторий: telegram-bot")
    print("4. Сделайте его ПУБЛИЧНЫМ")
    print("5. НЕ добавляйте README, .gitignore или лицензию")
    print("6. Нажмите 'Create repository'")
    print("7. Скопируйте URL репозитория")
    print()
    
    repo_url = input("Введите URL вашего GitHub репозитория: ").strip()
    
    if not repo_url:
        print("URL репозитория не указан")
        return
    
    try:
        # Добавляем remote origin
        subprocess.run(['git', 'remote', 'add', 'origin', repo_url], check=True)
        print("Remote origin добавлен")
        
        # Переименовываем ветку в main
        subprocess.run(['git', 'branch', '-M', 'main'], check=True)
        print("Ветка переименована в main")
        
        # Пушим в GitHub
        subprocess.run(['git', 'push', '-u', 'origin', 'main'], check=True)
        print("Код загружен в GitHub")
        
    except subprocess.CalledProcessError as e:
        print(f"Ошибка при загрузке в GitHub: {e}")
        return
    
    print("\nИНСТРУКЦИИ ДЛЯ ДЕПЛОЯ НА RENDER:")
    print("=" * 60)
    print("1. Перейдите на https://render.com")
    print("2. Нажмите 'Get Started for Free'")
    print("3. Войдите через GitHub")
    print("4. Нажмите 'New +' -> 'Web Service'")
    print("5. Подключите ваш GitHub репозиторий")
    print("6. Настройки:")
    print("   - Name: telegram-bot")
    print("   - Environment: Python 3")
    print("   - Build Command: pip install -r requirements.txt")
    print("   - Start Command: python render_bot.py")
    print("7. Добавьте переменную окружения:")
    print("   - Key: BOT_TOKEN")
    print("   - Value: 7647122248:AAG49utA8oAhwPgjUbH2qTcNiT1Akh6JdtI")
    print("8. Нажмите 'Create Web Service'")
    print("9. Дождитесь завершения сборки (5-10 минут)")
    print("10. Откройте URL вашего сервиса")
    print()
    print("После деплоя ваш бот будет доступен по URL:")
    print("https://your-app-name.onrender.com")
    
    print("\n" + "=" * 60)
    print("ПОДГОТОВКА ЗАВЕРШЕНА!")
    print("Теперь следуйте инструкциям выше для деплоя на Render")
    print("=" * 60)

if __name__ == "__main__":
    main()
