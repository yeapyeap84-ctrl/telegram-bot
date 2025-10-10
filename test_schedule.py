#!/usr/bin/env python3
"""
Тест нового расписания публикации
"""

import asyncio
from telegram_bot import TelegramPublisher
from config import BOT_TOKEN, POST_TEMPLATES, PUBLISH_SCHEDULE

async def test_schedule():
    """Тестирование нового расписания"""
    print("=" * 60)
    print("ТЕСТ НОВОГО РАСПИСАНИЯ ПУБЛИКАЦИИ")
    print("=" * 60)
    
    print(f"Новое расписание: {', '.join(PUBLISH_SCHEDULE)} МСК")
    print(f"Количество публикаций в день: {len(PUBLISH_SCHEDULE)}")
    print()
    
    # Показываем все шаблоны сообщений
    print("Шаблоны сообщений:")
    for time_str in PUBLISH_SCHEDULE:
        template = POST_TEMPLATES.get(time_str, {})
        text = template.get('text', 'Нет шаблона')
        # Убираем эмодзи для совместимости с Windows
        clean_text = text.replace('🌅', '').replace('☀️', '').replace('☕', '').replace('🌆', '').strip()
        print(f"  {time_str} МСК: {clean_text}")
    
    print()
    print("=" * 60)
    print("БОТ ГОТОВ К РАБОТЕ С НОВЫМ РАСПИСАНИЕМ!")
    print("=" * 60)
    print("Публикации будут происходить:")
    print("• 08:00 МСК - Утренний пост")
    print("• 12:00 МСК - Полуденный пост") 
    print("• 16:00 МСК - Послеобеденный пост")
    print("• 19:00 МСК - Вечерний пост")
    print()
    print("Для запуска бота используйте: py telegram_bot.py")

if __name__ == "__main__":
    asyncio.run(test_schedule())
