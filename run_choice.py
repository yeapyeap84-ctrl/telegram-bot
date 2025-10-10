#!/usr/bin/env python3
"""
Выбор между локальной и хостинг-версией бота
"""

import asyncio
import sys
import os
from pathlib import Path

def check_requirements():
    """Проверка требований"""
    print("Проверка требований...")
    
    # Проверяем основные файлы
    required_files = ['config.py', 'telegram_bot.py', 'bot_hosting.py']
    missing_files = []
    
    for file in required_files:
        if not Path(file).exists():
            missing_files.append(file)
    
    if missing_files:
        print(f"ОШИБКА: Отсутствуют файлы: {', '.join(missing_files)}")
        return False
    
    # Проверяем зависимости
    try:
        import telegram
        import schedule
        import pytz
        print("Основные зависимости установлены")
    except ImportError as e:
        print(f"ОШИБКА: Отсутствует зависимость: {e}")
        return False
    
    # Проверяем Flask для хостинга
    try:
        import flask
        print("Flask доступен для хостинга")
    except ImportError:
        print("ВНИМАНИЕ: Flask не установлен. Хостинг-версия недоступна")
        return False
    
    return True

async def main():
    """Главное меню"""
    print("=" * 60)
    print("TELEGRAM BOT - ВЫБОР ВЕРСИИ")
    print("=" * 60)
    
    if not check_requirements():
        print("\nОШИБКА: Не выполнены требования")
        return
    
    print("\nВыберите версию бота:")
    print("1. 🖥️  Локальная версия (только на вашем компьютере)")
    print("2. ☁️  Хостинг-версия (с веб-интерфейсом)")
    print("3. 🚀 Деплой на хостинг")
    print("4. 🧪 Тестирование")
    print("5. ❌ Выход")
    
    while True:
        try:
            choice = input("\nВведите номер (1-5): ").strip()
            
            if choice == '1':
                print("\nЗапуск локальной версии...")
                print("Для остановки нажмите Ctrl+C")
                from telegram_bot import main as run_local
                await run_local()
                break
                
            elif choice == '2':
                print("\nЗапуск хостинг-версии...")
                print("Веб-интерфейс: http://localhost:5000")
                print("Для остановки нажмите Ctrl+C")
                from bot_hosting import main as run_hosting
                await run_hosting()
                break
                
            elif choice == '3':
                print("\nЗапуск деплоя...")
                from deploy import main as deploy_main
                deploy_main()
                break
                
            elif choice == '4':
                print("\nВыберите тест:")
                print("1. Тест локальной версии")
                print("2. Тест хостинг-версии")
                print("3. Тест расписания")
                
                test_choice = input("Введите номер (1-3): ").strip()
                
                if test_choice == '1':
                    from test_simple import main as test_local
                    await test_local()
                elif test_choice == '2':
                    from test_hosting import main as test_hosting
                    await test_hosting()
                elif test_choice == '3':
                    from test_schedule import main as test_schedule
                    await test_schedule()
                else:
                    print("Неверный выбор")
                break
                
            elif choice == '5':
                print("До свидания!")
                break
                
            else:
                print("Неверный выбор. Введите 1-5")
                
        except KeyboardInterrupt:
            print("\nВыход...")
            break
        except Exception as e:
            print(f"ОШИБКА: {e}")
            break

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nПрограмма завершена")
    except Exception as e:
        print(f"КРИТИЧЕСКАЯ ОШИБКА: {e}")
        sys.exit(1)
