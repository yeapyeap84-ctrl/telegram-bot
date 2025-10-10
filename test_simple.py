#!/usr/bin/env python3
"""
Простой тест бота без эмодзи
"""

import asyncio
import sys
from telegram_bot import TelegramPublisher
from config import BOT_TOKEN, CHANNELS

async def test_bot():
    """Тестирование бота"""
    print("Тестирование Telegram бота...")
    
    # Проверяем токен
    if BOT_TOKEN == 'YOUR_BOT_TOKEN_HERE':
        print("ОШИБКА: Необходимо указать BOT_TOKEN в config.py")
        return False
    
    # Создаем экземпляр бота
    publisher = TelegramPublisher(BOT_TOKEN)
    
    try:
        # Тестируем подключение
        bot_info = await publisher.bot.get_me()
        print(f"Бот подключен: @{bot_info.username}")
        
        # Тестовое сообщение
        test_message = "Тестовое сообщение от бота"
        
        print(f"Отправляем тестовое сообщение в {len(CHANNELS)} каналов...")
        
        # Отправляем во все каналы
        results = await publisher.publish_to_all_channels(test_message)
        
        # Выводим результаты
        print("\nРезультаты тестирования:")
        successful = 0
        failed = 0
        
        for channel, success in results.items():
            status = "OK" if success else "ERROR"
            print(f"{status} {channel}")
            if success:
                successful += 1
            else:
                failed += 1
        
        print(f"\nИтого: {successful} успешно, {failed} с ошибками")
        
        if successful > 0:
            print("Тест прошел успешно! Бот готов к работе.")
            return True
        else:
            print("Все отправки завершились ошибкой. Проверьте настройки.")
            return False
            
    except Exception as e:
        print(f"Ошибка при тестировании: {e}")
        return False

async def main():
    """Основная функция"""
    print("=" * 50)
    print("ТЕСТИРОВАНИЕ TELEGRAM БОТА")
    print("=" * 50)
    
    success = await test_bot()
    
    print("\n" + "=" * 50)
    if success:
        print("Тестирование завершено успешно!")
        print("Теперь можно запустить основной бот: python telegram_bot.py")
    else:
        print("Тестирование завершилось с ошибками.")
        print("Проверьте настройки в config.py и права бота в каналах.")
    print("=" * 50)

if __name__ == "__main__":
    asyncio.run(main())
