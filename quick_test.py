#!/usr/bin/env python3
"""
Быстрый тест автопостов
Простой скрипт для тестирования в любое время
"""

import asyncio
import sys
from datetime import datetime
from telegram_bot import TelegramPublisher
from config import BOT_TOKEN, CHANNELS

async def quick_test():
    """Быстрый тест автопостов"""
    print("🚀 БЫСТРЫЙ ТЕСТ АВТОПОСТОВ")
    print("=" * 40)
    
    # Проверяем токен
    if BOT_TOKEN == 'YOUR_BOT_TOKEN_HERE':
        print("❌ Ошибка: Необходимо указать BOT_TOKEN в config.py")
        return False
    
    # Создаем экземпляр бота
    publisher = TelegramPublisher(BOT_TOKEN)
    
    try:
        # Тестируем подключение
        bot_info = await publisher.bot.get_me()
        print(f"✅ Бот подключен: @{bot_info.username}")
        
        # Тестовое сообщение с временной меткой
        current_time = datetime.now().strftime('%H:%M:%S')
        test_message = f"🧪 Тест автопоста - {current_time}"
        
        print(f"📤 Отправляем: {test_message}")
        print(f"📢 В {len(CHANNELS)} каналов...")
        
        # Отправляем во все каналы
        results = await publisher.publish_to_all_channels(test_message)
        
        # Подсчитываем результаты
        successful = sum(1 for success in results.values() if success)
        failed = len(results) - successful
        
        print(f"\n📊 Результаты:")
        print(f"✅ Успешно: {successful}")
        print(f"❌ Ошибок: {failed}")
        
        if successful > 0:
            print(f"\n🎉 Тест прошел успешно!")
            print(f"📈 Отправлено в {successful} из {len(results)} каналов")
            return True
        else:
            print(f"\n❌ Все отправки завершились ошибкой")
            return False
            
    except Exception as e:
        print(f"❌ Ошибка: {e}")
        return False

async def main():
    """Основная функция"""
    success = await quick_test()
    
    print("\n" + "=" * 40)
    if success:
        print("✅ Автопосты работают корректно!")
        print("🌐 Для полного управления используйте: python web_interface.py")
    else:
        print("❌ Проверьте настройки в config.py")
    print("=" * 40)

if __name__ == "__main__":
    asyncio.run(main())


