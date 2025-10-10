#!/usr/bin/env python3
"""
Скрипт для быстрого запуска Telegram бота
Включает проверку настроек и тестирование
"""

import asyncio
import sys
import os
from pathlib import Path

# Устанавливаем кодировку UTF-8 для Windows
if sys.platform == "win32":
    import codecs
    sys.stdout = codecs.getwriter("utf-8")(sys.stdout.detach())
    sys.stderr = codecs.getwriter("utf-8")(sys.stderr.detach())

def check_config():
    """Проверка конфигурации"""
    print("🔍 Проверка конфигурации...")
    
    # Проверяем наличие файлов
    required_files = ['config.py', 'telegram_bot.py', 'requirements.txt']
    missing_files = []
    
    for file in required_files:
        if not Path(file).exists():
            missing_files.append(file)
    
    if missing_files:
        print(f"❌ Отсутствуют файлы: {', '.join(missing_files)}")
        return False
    
    # Проверяем токен
    try:
        from config import BOT_TOKEN, CHANNELS
        
        if BOT_TOKEN == 'YOUR_BOT_TOKEN_HERE':
            print("❌ Необходимо указать BOT_TOKEN в config.py")
            return False
        
        if not CHANNELS or len(CHANNELS) == 0:
            print("❌ Необходимо указать каналы в config.py")
            return False
        
        # Проверяем, что используются ID каналов
        example_ids = [-1001234567890, -1001234567891, -1001234567892]
        if any(channel in example_ids for channel in CHANNELS):
            print("⚠️ В config.py указаны примеры ID каналов")
            print("💡 Замените их на реальные ID ваших каналов")
            print("🔍 Запустите: python get_channel_ids.py для получения ID")
            return False
        
        if len(CHANNELS) < 10:
            print(f"⚠️ Указано только {len(CHANNELS)} каналов (рекомендуется 10)")
        
        print("✅ Конфигурация проверена")
        return True
        
    except ImportError as e:
        print(f"❌ Ошибка импорта: {e}")
        return False

def install_requirements():
    """Установка зависимостей"""
    print("📦 Проверка зависимостей...")
    
    try:
        import telegram
        import schedule
        import pytz
        print("✅ Все зависимости установлены")
        return True
    except ImportError as e:
        print(f"❌ Отсутствует зависимость: {e}")
        print("💡 Установите зависимости: pip install -r requirements.txt")
        return False

async def main():
    """Основная функция"""
    print("=" * 60)
    print("🤖 TELEGRAM BOT - АВТОМАТИЧЕСКАЯ ПУБЛИКАЦИЯ ПОСТОВ")
    print("=" * 60)
    
    # Проверяем конфигурацию
    if not check_config():
        print("\n❌ Проверьте настройки и попробуйте снова")
        return
    
    # Проверяем зависимости
    if not install_requirements():
        print("\n❌ Установите зависимости и попробуйте снова")
        return
    
    print("\n🎯 Выберите действие:")
    print("1. 🧪 Тестирование бота (отправить тестовое сообщение)")
    print("2. 🚀 Запуск бота (автоматическая публикация по расписанию)")
    print("3. 🔍 Получить ID каналов")
    print("4. ❌ Выход")
    
    while True:
        try:
            choice = input("\nВведите номер (1-4): ").strip()
            
            if choice == '1':
                print("\n🧪 Запуск тестирования...")
                from test_bot import test_bot
                success = await test_bot()
                if success:
                    print("\n✅ Тестирование завершено успешно!")
                else:
                    print("\n❌ Тестирование завершилось с ошибками")
                break
                
            elif choice == '2':
                print("\n🚀 Запуск бота...")
                print("💡 Для остановки нажмите Ctrl+C")
                from telegram_bot import main as run_bot
                await run_bot()
                break
                
            elif choice == '3':
                print("\n🔍 Запуск получения ID каналов...")
                from get_channel_ids import main as get_ids
                await get_ids()
                break
                
            elif choice == '4':
                print("👋 До свидания!")
                break
                
            else:
                print("❌ Неверный выбор. Введите 1, 2, 3 или 4")
                
        except KeyboardInterrupt:
            print("\n👋 Выход...")
            break
        except Exception as e:
            print(f"❌ Ошибка: {e}")
            break

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n👋 Программа завершена")
    except Exception as e:
        print(f"❌ Критическая ошибка: {e}")
        sys.exit(1)

