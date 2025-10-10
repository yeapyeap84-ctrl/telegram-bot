#!/usr/bin/env python3
"""
Тест хостинг-версии бота
"""

import asyncio
import sys
from bot_hosting import TelegramPublisher, bot_status
from config import BOT_TOKEN, CHANNELS

async def test_hosting_bot():
    """Тестирование хостинг-версии бота"""
    print("=" * 60)
    print("ТЕСТ ХОСТИНГ-ВЕРСИИ TELEGRAM БОТА")
    print("=" * 60)
    
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
        test_message = "Тестовое сообщение с хостинга"
        
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
        
        # Проверяем статус
        print(f"\nСтатус бота: {bot_status}")
        
        if successful > 0:
            print("Тест прошел успешно! Хостинг-версия готова к работе.")
            return True
        else:
            print("Все отправки завершились ошибкой. Проверьте настройки.")
            return False
            
    except Exception as e:
        print(f"Ошибка при тестировании: {e}")
        return False

async def main():
    """Основная функция"""
    success = await test_hosting_bot()
    
    print("\n" + "=" * 60)
    if success:
        print("ХОСТИНГ-ВЕРСИЯ ГОТОВА К РАБОТЕ!")
        print("Для запуска используйте: python bot_hosting.py")
        print("Веб-интерфейс будет доступен на http://localhost:5000")
    else:
        print("Тестирование завершилось с ошибками.")
        print("Проверьте настройки в config.py и права бота в каналах.")
    print("=" * 60)

if __name__ == "__main__":
    asyncio.run(main())
