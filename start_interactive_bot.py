#!/usr/bin/env python3
"""
Скрипт для запуска интерактивного бота
"""

import asyncio
import sys
import os

# Добавляем текущую директорию в путь для импорта
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from interactive_bot import main

if __name__ == "__main__":
    print("🤖 Запуск интерактивного Telegram бота...")
    print("=" * 50)
    print("Доступные команды:")
    print("/start - Начать работу с ботом")
    print("/post - Отправить пост во все каналы")
    print("/status - Проверить статус бота")
    print("/help - Показать справку")
    print("=" * 50)
    
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n👋 Бот остановлен пользователем")
    except Exception as e:
        print(f"❌ Ошибка при запуске бота: {e}")
        sys.exit(1)
