#!/usr/bin/env python3
"""
Интерактивный Telegram бот для Render.com
Совместим с python-telegram-bot версии 13.x
"""

import asyncio
import logging
import schedule
import time
import threading
from datetime import datetime
from typing import List, Dict, Optional
import pytz
import os
from flask import Flask, render_template_string, jsonify

# Импортируем конфигурацию
try:
    from config import (
        BOT_TOKEN, 
        CHANNELS, 
        PUBLISH_SCHEDULE, 
        TIMEZONE, 
        POST_TEMPLATES,
        LOG_LEVEL,
        LOG_FILE
    )
except ImportError:
    # Если config.py недоступен, используем переменные окружения
    BOT_TOKEN = os.getenv('BOT_TOKEN', 'YOUR_BOT_TOKEN_HERE')
    CHANNELS = [
        -1002277035159, -1002195443836, -1003138556967, -1003073283084,
        -1003009581774, -1003095553897, -1003107072222, -1003127705651,
        -1002845102398, -1003109538114, -1003188704305, -1003175391285,
        -1003007890686, -1002910404940, -1003183362739, -1003193174512,
        -1003103796345, -1003173861260, -1003049221239, -1003142157172,
        -1003001850127, -1003164923728, -1003180273662, -1003129428375,
        -1003047357295, -1003112731633, -1003179889345, -1002793918718,
        -1003043204491
    ]
    PUBLISH_SCHEDULE = ['08:00', '12:00', '16:00', '19:00']
    TIMEZONE = 'Europe/Moscow'
    POST_TEMPLATES = {
        '08:00': {'text': '🌅 Доброе утро! Начинаем новый день с позитивом!', 'parse_mode': 'HTML'},
        '12:00': {'text': '☀️ Полдень! Время для обеда и перерыва!', 'parse_mode': 'HTML'},
        '16:00': {'text': '☕ Время для кофе-брейка! Как дела?', 'parse_mode': 'HTML'},
        '19:00': {'text': '🌆 Вечер! Завершаем день на позитивной ноте!', 'parse_mode': 'HTML'}
    }
    LOG_LEVEL = 'INFO'
    LOG_FILE = 'bot.log'

# Настройка логирования
logging.basicConfig(
    level=getattr(logging, LOG_LEVEL),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(LOG_FILE, encoding='utf-8'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Импорты для старой версии python-telegram-bot
try:
    from telegram import Bot, Update
    from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
    from telegram.error import TelegramError
    TELEGRAM_BOT_VERSION = "13.x"
except ImportError:
    try:
        from telegram import Bot, Update
        from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters
        from telegram.error import TelegramError
        TELEGRAM_BOT_VERSION = "20.x"
    except ImportError:
        logger.error("❌ Не удалось импортировать python-telegram-bot")
        exit(1)

class TelegramPublisher:
    """Класс для публикации сообщений в Telegram каналы"""
    
    def __init__(self, bot_token: str):
        self.bot = Bot(token=bot_token)
        self.channels = CHANNELS
        self.timezone = pytz.timezone(TIMEZONE)
        
    async def publish_to_channel(self, channel: str, message: str, parse_mode: str = 'HTML') -> bool:
        """Публикация сообщения в один канал"""
        try:
            await self.bot.send_message(
                chat_id=channel,
                text=message,
                parse_mode=parse_mode
            )
            logger.info(f"✅ Сообщение успешно отправлено в {channel}")
            return True
        except TelegramError as e:
            logger.error(f"❌ Ошибка при отправке в {channel}: {e}")
            return False
        except Exception as e:
            logger.error(f"❌ Неожиданная ошибка при отправке в {channel}: {e}")
            return False
    
    async def publish_to_all_channels(self, message: str, parse_mode: str = 'HTML') -> Dict[str, bool]:
        """Публикация сообщения во все каналы"""
        results = {}
        
        logger.info(f"🚀 Начинаем публикацию сообщения в {len(self.channels)} каналов")
        
        # Создаем задачи для всех каналов
        tasks = []
        for channel in self.channels:
            task = self.publish_to_channel(channel, message, parse_mode)
            tasks.append((channel, task))
        
        # Выполняем все задачи параллельно
        for channel, task in tasks:
            try:
                result = await task
                results[channel] = result
            except Exception as e:
                logger.error(f"❌ Ошибка при обработке канала {channel}: {e}")
                results[channel] = False
        
        # Подсчитываем результаты
        successful = sum(1 for success in results.values() if success)
        failed = len(results) - successful
        
        logger.info(f"📊 Результаты публикации: {successful} успешно, {failed} с ошибками")
        
        return results
    
    def get_current_time_moscow(self) -> datetime:
        """Получение текущего времени в МСК"""
        return datetime.now(self.timezone)
    
    def get_post_for_time(self, time_str: str) -> Optional[Dict[str, str]]:
        """Получение шаблона поста для указанного времени"""
        return POST_TEMPLATES.get(time_str)

class Scheduler:
    """Планировщик для автоматической публикации"""
    
    def __init__(self, publisher: TelegramPublisher):
        self.publisher = publisher
        self.schedule_times = PUBLISH_SCHEDULE
        
    def schedule_posts(self):
        """Настройка расписания публикации"""
        for time_str in self.schedule_times:
            schedule.every().day.at(time_str).do(self.publish_scheduled_post, time_str)
            logger.info(f"⏰ Запланирована публикация на {time_str} МСК")
    
    async def publish_scheduled_post(self, time_str: str):
        """Публикация по расписанию"""
        current_time = self.publisher.get_current_time_moscow()
        logger.info(f"🕐 Время публикации: {time_str} МСК, текущее время: {current_time.strftime('%H:%M')}")
        
        # Получаем шаблон поста для этого времени
        post_template = self.publisher.get_post_for_time(time_str)
        
        if not post_template:
            logger.warning(f"⚠️ Не найден шаблон поста для времени {time_str}")
            return
        
        message = post_template['text']
        parse_mode = post_template.get('parse_mode', 'HTML')
        
        # Публикуем во все каналы
        results = await self.publisher.publish_to_all_channels(message, parse_mode)
        
        # Логируем результаты
        for channel, success in results.items():
            status = "✅" if success else "❌"
            logger.info(f"{status} {channel}: {'Успешно' if success else 'Ошибка'}")
    
    def run_scheduler(self):
        """Запуск планировщика"""
        logger.info("🚀 Планировщик запущен")
        self.schedule_posts()
        
        while True:
            schedule.run_pending()
            time.sleep(60)  # Проверяем каждую минуту

# Глобальные переменные для бота
publisher = None
scheduler = None

def start_command(update, context):
    """Обработчик команды /start"""
    welcome_text = """
🤖 <b>Добро пожаловать в бот автопостов!</b>

<b>Доступные команды:</b>
/post - Отправить пост во все каналы
/status - Проверить статус бота
/help - Показать справку

<b>Автоматические посты:</b>
Бот автоматически публикует посты по расписанию:
"""
    for time in PUBLISH_SCHEDULE:
        welcome_text += f"• {time} МСК\n"
    
    update.message.reply_text(welcome_text, parse_mode='HTML')

def help_command(update, context):
    """Обработчик команды /help"""
    help_text = """
📖 <b>Справка по командам:</b>

<b>/post</b> - Отправить пост во все каналы
Использование: /post [текст сообщения]
Пример: /post Привет всем!

<b>/status</b> - Проверить статус бота
Показывает количество каналов и время следующей публикации

<b>/help</b> - Показать эту справку

<b>Автоматические посты:</b>
Бот публикует посты по расписанию в указанное время.
"""
    update.message.reply_text(help_text, parse_mode='HTML')

def post_command(update, context):
    """Обработчик команды /post"""
    global publisher
    
    # Получаем текст сообщения (все после /post)
    if context.args:
        message_text = ' '.join(context.args)
    else:
        # Если текст не указан, используем шаблон по умолчанию
        current_time = publisher.get_current_time_moscow()
        time_str = current_time.strftime('%H:%M')
        
        # Ищем ближайший шаблон
        template = None
        for scheduled_time in sorted(POST_TEMPLATES.keys()):
            if scheduled_time >= time_str:
                template = POST_TEMPLATES[scheduled_time]
                break
        
        if not template:
            # Если не найден шаблон, используем первый доступный
            template = list(POST_TEMPLATES.values())[0]
        
        message_text = template['text']
    
    # Отправляем сообщение о начале публикации
    update.message.reply_text(
        f"🚀 Начинаю публикацию в {len(publisher.channels)} каналов...\n"
        f"📝 Текст: {message_text[:100]}{'...' if len(message_text) > 100 else ''}"
    )
    
    # Запускаем публикацию в отдельном потоке
    def publish_async():
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            results = loop.run_until_complete(publisher.publish_to_all_channels(message_text))
            
            # Подсчитываем результаты
            successful = sum(1 for success in results.values() if success)
            failed = len(results) - successful
            
            # Отправляем отчет
            report = f"""
📊 <b>Результаты публикации:</b>

✅ Успешно: {successful}
❌ Ошибки: {failed}
📤 Всего каналов: {len(results)}

<b>Детали:</b>
"""
            
            for channel, success in results.items():
                status = "✅" if success else "❌"
                report += f"{status} {channel}\n"
            
            update.message.reply_text(report, parse_mode='HTML')
            
        except Exception as e:
            update.message.reply_text(f"❌ Ошибка при публикации: {e}")
            logger.error(f"Ошибка в команде /post: {e}")
        finally:
            loop.close()
    
    # Запускаем в отдельном потоке
    thread = threading.Thread(target=publish_async)
    thread.start()

def status_command(update, context):
    """Обработчик команды /status"""
    global publisher
    
    try:
        # Получаем информацию о боте
        bot_info = publisher.bot.get_me()
        current_time = publisher.get_current_time_moscow()
        
        status_text = f"""
🤖 <b>Статус бота:</b>

👤 Бот: @{bot_info.username}
🕐 Текущее время: {current_time.strftime('%H:%M:%S')} МСК
📢 Каналов: {len(publisher.channels)}
⏰ Расписание: {', '.join(PUBLISH_SCHEDULE)} МСК

<b>Следующие публикации:</b>
"""
        
        # Показываем ближайшие запланированные посты
        for time_str in sorted(POST_TEMPLATES.keys()):
            template = POST_TEMPLATES[time_str]
            status_text += f"• {time_str} - {template['text'][:50]}...\n"
        
        update.message.reply_text(status_text, parse_mode='HTML')
        
    except Exception as e:
        update.message.reply_text(f"❌ Ошибка при получении статуса: {e}")
        logger.error(f"Ошибка в команде /status: {e}")

def handle_message(update, context):
    """Обработчик обычных сообщений"""
    update.message.reply_text(
        "👋 Привет! Используй /help для просмотра доступных команд."
    )

def main():
    """Основная функция"""
    global publisher, scheduler
    
    logger.info("🤖 Запуск интерактивного Telegram бота для Render")
    
    # Проверяем токен
    if BOT_TOKEN == 'YOUR_BOT_TOKEN_HERE':
        logger.error("❌ Необходимо указать BOT_TOKEN в config.py или переменной окружения")
        return
    
    # Создаем экземпляр publisher
    publisher = TelegramPublisher(BOT_TOKEN)
    
    # Создаем планировщик
    scheduler = Scheduler(publisher)
    
    # Запускаем планировщик в отдельном потоке
    scheduler_thread = threading.Thread(target=scheduler.run_scheduler, daemon=True)
    scheduler_thread.start()
    
    logger.info("⏰ Планировщик настроен и запущен")
    logger.info(f"📅 Расписание: {', '.join(PUBLISH_SCHEDULE)} МСК")
    logger.info(f"📢 Каналы: {len(CHANNELS)} каналов")
    logger.info("🎯 Интерактивные команды: /start, /help, /post, /status")
    
    # Создаем бота в зависимости от версии библиотеки
    if TELEGRAM_BOT_VERSION == "13.x":
        # Старая версия с Updater
        updater = Updater(token=BOT_TOKEN, use_context=True)
        dispatcher = updater.dispatcher
        
        # Добавляем обработчики команд
        dispatcher.add_handler(CommandHandler("start", start_command))
        dispatcher.add_handler(CommandHandler("help", help_command))
        dispatcher.add_handler(CommandHandler("post", post_command))
        dispatcher.add_handler(CommandHandler("status", status_command))
        dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))
        
        # Запускаем бота
        updater.start_polling()
        logger.info("🚀 Бот запущен и готов к работе!")
        
        # Держим бота активным
        updater.idle()
    else:
        # Новая версия с Application
        app = Application.builder().token(BOT_TOKEN).build()
        
        # Добавляем обработчики команд
        app.add_handler(CommandHandler("start", start_command))
        app.add_handler(CommandHandler("help", help_command))
        app.add_handler(CommandHandler("post", post_command))
        app.add_handler(CommandHandler("status", status_command))
        app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
        
        # Запускаем бота
        app.run_polling()
        logger.info("🚀 Бот запущен и готов к работе!")

if __name__ == "__main__":
    main()
