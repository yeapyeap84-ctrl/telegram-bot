#!/usr/bin/env python3
"""
Тест отправки в 30 каналов
"""

import asyncio
from render_bot import TelegramPublisher
from config import BOT_TOKEN, CHANNELS

async def test_30_channels():
    """Тестирование отправки в 30 каналов"""
    print("=" * 60)
    print("ТЕСТ ОТПРАВКИ В 30 КАНАЛОВ")
    print("=" * 60)
    
    # Создаем экземпляр бота
    publisher = TelegramPublisher(BOT_TOKEN)
    
    # Тестовое сообщение
    test_message = "🧪 ТЕСТ: Проверка работы с 30 каналами!"
    
    print(f"Отправляем тестовое сообщение в {len(CHANNELS)} каналов...")
    print(f"Каналы: {CHANNELS[:5]}... (показаны первые 5)")
    
    try:
        # Отправляем во все каналы
        results = await publisher.publish_to_all_channels(test_message)
        
        # Подсчитываем результаты
        successful = sum(1 for success in results.values() if success)
        failed = len(results) - successful
        
        print(f"\nРЕЗУЛЬТАТЫ ТЕСТА:")
        print(f"Всего каналов: {len(results)}")
        print(f"Успешно: {successful}")
        print(f"Ошибок: {failed}")
        
        if successful > 0:
            print(f"\n✅ ТЕСТ ПРОШЕЛ! Отправлено в {successful} каналов")
        else:
            print(f"\n❌ ТЕСТ НЕ ПРОШЕЛ! Все отправки завершились ошибкой")
            
        return successful > 0
        
    except Exception as e:
        print(f"❌ Ошибка при тестировании: {e}")
        return False

async def main():
    """Основная функция"""
    success = await test_30_channels()
    
    print("\n" + "=" * 60)
    if success:
        print("🎉 БОТ РАБОТАЕТ С 30 КАНАЛАМИ!")
        print("Теперь он будет автоматически публиковать в 30 каналов")
    else:
        print("❌ ПРОБЛЕМА! Проверьте настройки и права бота")
    print("=" * 60)

if __name__ == "__main__":
    asyncio.run(main())
