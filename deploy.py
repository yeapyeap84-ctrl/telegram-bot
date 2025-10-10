#!/usr/bin/env python3
"""
Скрипт для деплоя Telegram бота на различные хостинги
"""

import os
import subprocess
import sys

def check_requirements():
    """Проверка требований для деплоя"""
    print("🔍 Проверка требований для деплоя...")
    
    # Проверяем Docker
    try:
        result = subprocess.run(['docker', '--version'], capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ Docker установлен")
        else:
            print("❌ Docker не найден")
            return False
    except FileNotFoundError:
        print("❌ Docker не установлен")
        return False
    
    # Проверяем docker-compose
    try:
        result = subprocess.run(['docker-compose', '--version'], capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ Docker Compose установлен")
        else:
            print("❌ Docker Compose не найден")
            return False
    except FileNotFoundError:
        print("❌ Docker Compose не установлен")
        return False
    
    return True

def deploy_local():
    """Деплой на локальную машину"""
    print("\n🚀 Деплой на локальную машину...")
    
    if not check_requirements():
        print("❌ Не выполнены требования для деплоя")
        return False
    
    try:
        # Собираем Docker образ
        print("📦 Сборка Docker образа...")
        subprocess.run(['docker-compose', 'build'], check=True)
        
        # Запускаем контейнер
        print("🚀 Запуск контейнера...")
        subprocess.run(['docker-compose', 'up', '-d'], check=True)
        
        print("✅ Бот успешно развернут!")
        print("🌐 Веб-интерфейс: http://localhost:5000")
        print("📊 Мониторинг: http://localhost:5000/api/status")
        
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Ошибка при деплое: {e}")
        return False

def deploy_heroku():
    """Деплой на Heroku"""
    print("\n🚀 Деплой на Heroku...")
    
    # Создаем Procfile для Heroku
    procfile_content = """web: python bot_hosting.py"""
    
    with open('Procfile', 'w') as f:
        f.write(procfile_content)
    
    print("📝 Создан Procfile для Heroku")
    
    # Создаем runtime.txt
    runtime_content = """python-3.11.0"""
    
    with open('runtime.txt', 'w') as f:
        f.write(runtime_content)
    
    print("📝 Создан runtime.txt")
    
    print("\n📋 Инструкции для деплоя на Heroku:")
    print("1. Установите Heroku CLI")
    print("2. Войдите в аккаунт: heroku login")
    print("3. Создайте приложение: heroku create your-bot-name")
    print("4. Установите переменные окружения:")
    print("   heroku config:set BOT_TOKEN=your_bot_token")
    print("5. Деплой: git push heroku main")
    print("6. Запуск: heroku ps:scale web=1")
    
    return True

def deploy_railway():
    """Деплой на Railway"""
    print("\n🚀 Деплой на Railway...")
    
    # Создаем railway.json
    railway_config = {
        "build": {
            "builder": "NIXPACKS"
        },
        "deploy": {
            "startCommand": "python bot_hosting.py",
            "restartPolicyType": "ON_FAILURE",
            "restartPolicyMaxRetries": 10
        }
    }
    
    import json
    with open('railway.json', 'w') as f:
        json.dump(railway_config, f, indent=2)
    
    print("📝 Создан railway.json")
    
    print("\n📋 Инструкции для деплоя на Railway:")
    print("1. Установите Railway CLI")
    print("2. Войдите в аккаунт: railway login")
    print("3. Создайте проект: railway init")
    print("4. Установите переменные окружения:")
    print("   railway variables set BOT_TOKEN=your_bot_token")
    print("5. Деплой: railway up")
    
    return True

def deploy_render():
    """Деплой на Render"""
    print("\n🚀 Деплой на Render...")
    
    # Создаем render.yaml
    render_config = """services:
  - type: web
    name: telegram-bot
    env: python
    buildCommand: pip install -r requirements.txt && pip install flask
    startCommand: python bot_hosting.py
    envVars:
      - key: BOT_TOKEN
        sync: false"""
    
    with open('render.yaml', 'w') as f:
        f.write(render_config)
    
    print("📝 Создан render.yaml")
    
    print("\n📋 Инструкции для деплоя на Render:")
    print("1. Зарегистрируйтесь на render.com")
    print("2. Подключите GitHub репозиторий")
    print("3. Создайте Web Service")
    print("4. Установите переменные окружения:")
    print("   BOT_TOKEN=your_bot_token")
    print("5. Деплой произойдет автоматически")
    
    return True

def main():
    """Главное меню"""
    print("=" * 60)
    print("🚀 ДЕПЛОЙ TELEGRAM БОТА НА ХОСТИНГ")
    print("=" * 60)
    
    print("\nВыберите платформу для деплоя:")
    print("1. 🖥️  Локальная машина (Docker)")
    print("2. ☁️  Heroku")
    print("3. 🚂 Railway")
    print("4. 🎨 Render")
    print("5. ❌ Выход")
    
    while True:
        try:
            choice = input("\nВведите номер (1-5): ").strip()
            
            if choice == '1':
                deploy_local()
                break
            elif choice == '2':
                deploy_heroku()
                break
            elif choice == '3':
                deploy_railway()
                break
            elif choice == '4':
                deploy_render()
                break
            elif choice == '5':
                print("👋 До свидания!")
                break
            else:
                print("❌ Неверный выбор. Введите 1-5")
                
        except KeyboardInterrupt:
            print("\n👋 Выход...")
            break
        except Exception as e:
            print(f"❌ Ошибка: {e}")
            break

if __name__ == "__main__":
    main()
