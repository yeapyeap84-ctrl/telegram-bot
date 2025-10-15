#!/usr/bin/env python3
"""
Скрипт для тестирования автопостов
Позволяет запустить публикацию в любое время для тестирования
"""

import asyncio
import sys
from datetime import datetime
from telegram_bot import TelegramPublisher
from config import BOT_TOKEN, CHANNELS, POST_TEMPLATES

async def test_autopost():
    """Тестирование автопостов"""
    print("🧪 Тестирование автопостов...")
    print("=" * 50)
    
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
        
        # Показываем доступные шаблоны
        print("\n📝 Доступные шаблоны постов:")
        for time_key, template in POST_TEMPLATES.items():
            print(f"  {time_key}: {template['text']}")
        
        print(f"\n📤 Отправляем тестовое сообщение в {len(CHANNELS)} каналов...")
        
        # Выбираем шаблон для тестирования (например, утренний)
        test_template = POST_TEMPLATES.get('08:00', {
            'text': '🧪 Тестовое сообщение от бота',
            'parse_mode': 'HTML'
        })
        
        message = test_template['text']
        parse_mode = test_template.get('parse_mode', 'HTML')
        
        # Отправляем во все каналы
        results = await publisher.publish_to_all_channels(message, parse_mode)
        
        # Выводим результаты
        print("\n📊 Результаты тестирования:")
        successful = 0
        failed = 0
        
        for channel, success in results.items():
            status = "✅" if success else "❌"
            print(f"{status} {channel}")
            if success:
                successful += 1
            else:
                failed += 1
        
        print(f"\n📈 Итого: {successful} успешно, {failed} с ошибками")
        
        if successful > 0:
            print("🎉 Тест автопостов прошел успешно!")
            print("✅ Бот готов к автоматической публикации по расписанию")
            return True
        else:
            print("❌ Все отправки завершились ошибкой. Проверьте настройки.")
            return False
            
    except Exception as e:
        print(f"❌ Ошибка при тестировании: {e}")
        return False

async def test_custom_message():
    """Тестирование с пользовательским сообщением"""
    print("\n" + "=" * 50)
    print("📝 Тестирование с пользовательским сообщением")
    print("=" * 50)
    
    # Пользовательское сообщение
    custom_message = "🚀 Тестовый автопост - " + datetime.now().strftime('%H:%M:%S')
    
    publisher = TelegramPublisher(BOT_TOKEN)
    
    try:
        print(f"📤 Отправляем: {custom_message}")
        results = await publisher.publish_to_all_channels(custom_message)
        
        successful = sum(1 for success in results.values() if success)
        print(f"✅ Отправлено успешно: {successful} из {len(results)} каналов")
        
        return successful > 0
        
    except Exception as e:
        print(f"❌ Ошибка: {e}")
        return False

async def main():
    """Основная функция"""
    print("🤖 ТЕСТИРОВАНИЕ АВТОПОСТОВ")
    print("=" * 50)
    
    # Тест 1: Стандартный тест
    success1 = await test_autopost()
    
    # Тест 2: Пользовательское сообщение
    success2 = await test_custom_message()
    
    print("\n" + "=" * 50)
    print("📋 ИТОГИ ТЕСТИРОВАНИЯ")
    print("=" * 50)
    
    if success1 and success2:
        print("✅ Все тесты прошли успешно!")
        print("🚀 Автопосты работают корректно")
        print("⏰ Бот будет публиковать по расписанию:")
        from config import PUBLISH_SCHEDULE
        for time in PUBLISH_SCHEDULE:
            print(f"   - {time} МСК")
    else:
        print("❌ Некоторые тесты завершились с ошибками")
        print("🔧 Проверьте настройки в config.py и права бота в каналах")
    
    print("=" * 50)

if __name__ == "__main__":
    asyncio.run(main())


