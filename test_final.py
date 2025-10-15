#!/usr/bin/env python3
"""
Финальное тестирование интерактивного бота
"""

import asyncio
import sys
import os

# Добавляем текущую директорию в путь для импорта
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from interactive_bot import InteractiveBot
from config import BOT_TOKEN, CHANNELS, POST_TEMPLATES

async def test_bot_connection():
    """Тестирование подключения к боту"""
    print("Тестирование подключения к боту...")
    
    try:
        bot = InteractiveBot(BOT_TOKEN)
        bot_info = await bot.publisher.bot.get_me()
        print(f"OK: Бот подключен: @{bot_info.username}")
        return True
    except Exception as e:
        print(f"ERROR: Ошибка подключения: {e}")
        return False

async def test_post_functionality():
    """Тестирование функциональности отправки постов"""
    print("\nТестирование отправки постов...")
    
    try:
        bot = InteractiveBot(BOT_TOKEN)
        
        # Тестовое сообщение без эмодзи
        test_message = "Тестовое сообщение от интерактивного бота"
        
        print(f"Отправляем тестовое сообщение в {len(CHANNELS)} каналов...")
        print(f"Текст: {test_message}")
        
        # Отправляем во все каналы
        results = await bot.publisher.publish_to_all_channels(test_message)
        
        # Подсчитываем результаты
        successful = sum(1 for success in results.values() if success)
        failed = len(results) - successful
        
        print(f"\nРезультаты:")
        print(f"Успешно: {successful}")
        print(f"Ошибки: {failed}")
        
        if successful > 0:
            print("Тест прошел успешно!")
            return True
        else:
            print("Все отправки завершились ошибкой")
            return False
            
    except Exception as e:
        print(f"ERROR: Ошибка при тестировании: {e}")
        return False

async def main():
    """Основная функция тестирования"""
    print("ТЕСТИРОВАНИЕ ИНТЕРАКТИВНОГО БОТА")
    print("=" * 50)
    
    # Тест 1: Подключение к боту
    connection_ok = await test_bot_connection()
    
    # Тест 2: Отправка постов (только если подключение успешно)
    posts_ok = False
    if connection_ok:
        posts_ok = await test_post_functionality()
    
    print("\n" + "=" * 50)
    print("ИТОГИ ТЕСТИРОВАНИЯ")
    print("=" * 50)
    
    if connection_ok:
        print("OK: Подключение к боту")
    else:
        print("ERROR: Подключение к боту")
    
    if posts_ok:
        print("OK: Отправка постов")
    else:
        print("ERROR: Отправка постов")
    
    print("\nКоманды для использования в боте:")
    print("/start - Начать работу с ботом")
    print("/post - Отправить пост во все каналы")
    print("/post [текст] - Отправить кастомный пост")
    print("/status - Проверить статус бота")
    print("/help - Показать справку")
    
    if connection_ok and posts_ok:
        print("\nИнтерактивный бот готов к работе!")
        print("Запустите: py start_interactive_bot.py")
    else:
        print("\nПроверьте настройки в config.py")
    
    print("=" * 50)

if __name__ == "__main__":
    asyncio.run(main())
