#!/usr/bin/env python3
"""
Скрипт для получения ID каналов
Помогает найти ID каналов для настройки бота
"""

import asyncio
import logging
from telegram import Bot
from config import BOT_TOKEN

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def get_channel_info(bot_token: str, channel_username: str):
    """Получение информации о канале по @username"""
    bot = Bot(token=bot_token)
    
    try:
        # Пробуем получить информацию о канале
        chat = await bot.get_chat(f"@{channel_username}")
        
        print(f"📢 Канал: @{channel_username}")
        print(f"🆔 ID: {chat.id}")
        print(f"📝 Название: {chat.title}")
        print(f"👥 Тип: {chat.type}")
        print("-" * 50)
        
        return chat.id
        
    except Exception as e:
        print(f"❌ Ошибка для @{channel_username}: {e}")
        return None

async def get_my_chats(bot_token: str):
    """Получение списка всех чатов, где есть бот"""
    bot = Bot(token=bot_token)
    
    try:
        # Получаем информацию о боте
        bot_info = await bot.get_me()
        print(f"🤖 Бот: @{bot_info.username}")
        print("=" * 60)
        
        # К сожалению, Telegram API не предоставляет прямой способ
        # получить список всех чатов бота, поэтому показываем инструкции
        print("📋 ИНСТРУКЦИЯ ПО ПОЛУЧЕНИЮ ID КАНАЛОВ:")
        print("=" * 60)
        print("1. Добавьте бота в канал как администратора")
        print("2. Отправьте любое сообщение в канал")
        print("3. Перешлите это сообщение боту @userinfobot")
        print("4. Бот покажет ID канала (начинается с -100)")
        print("5. Скопируйте ID и вставьте в config.py")
        print()
        print("🔗 Альтернативный способ:")
        print("1. Отправьте сообщение в канал")
        print("2. Перешлите его боту @RawDataBot")
        print("3. Найдите 'chat_id' в ответе")
        print()
        print("💡 ID канала выглядит так: -1001234567890")
        print("   (всегда начинается с -100 для каналов)")
        
    except Exception as e:
        print(f"❌ Ошибка: {e}")

async def test_channel_access(bot_token: str, channel_id: int):
    """Тестирование доступа к каналу по ID"""
    bot = Bot(token=bot_token)
    
    try:
        chat = await bot.get_chat(channel_id)
        print(f"✅ Доступ к каналу {channel_id}: OK")
        print(f"📝 Название: {chat.title}")
        print(f"👥 Тип: {chat.type}")
        return True
    except Exception as e:
        print(f"❌ Нет доступа к каналу {channel_id}: {e}")
        return False

async def main():
    """Основная функция"""
    print("🔍 ПОЛУЧЕНИЕ ID КАНАЛОВ ДЛЯ TELEGRAM БОТА")
    print("=" * 60)
    
    if BOT_TOKEN == 'YOUR_BOT_TOKEN_HERE':
        print("❌ Необходимо указать BOT_TOKEN в config.py")
        return
    
    try:
        # Тестируем подключение к боту
        bot = Bot(token=BOT_TOKEN)
        bot_info = await bot.get_me()
        print(f"✅ Бот подключен: @{bot_info.username}")
        print()
        
        # Показываем инструкции
        await get_my_chats(BOT_TOKEN)
        
        print("\n" + "=" * 60)
        print("🧪 ТЕСТИРОВАНИЕ КАНАЛОВ")
        print("=" * 60)
        
        # Тестируем каналы из конфигурации
        from config import CHANNELS
        
        if CHANNELS and CHANNELS[0] != -1001234567890:  # Если каналы уже настроены
            print("🔍 Тестируем каналы из config.py:")
            for i, channel_id in enumerate(CHANNELS, 1):
                if isinstance(channel_id, int):
                    print(f"\n📢 Канал {i}: {channel_id}")
                    await test_channel_access(BOT_TOKEN, channel_id)
                else:
                    print(f"\n📢 Канал {i}: {channel_id} (не ID)")
        else:
            print("⚠️ Каналы в config.py не настроены")
            print("💡 Замените примеры ID на реальные ID ваших каналов")
        
    except Exception as e:
        print(f"❌ Ошибка: {e}")

if __name__ == "__main__":
    asyncio.run(main())
