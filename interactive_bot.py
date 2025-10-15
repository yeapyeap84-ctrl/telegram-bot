#!/usr/bin/env python3
"""
Интерактивный Telegram бот с командой /post
Позволяет отправлять посты в каналы по команде
"""

import asyncio
import logging
import schedule
import time
import threading
from datetime import datetime
from typing import List, Dict, Optional
import pytz
from telegram import Bot, Update
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters
from telegram.error import TelegramError
from config import (
    BOT_TOKEN, 
    CHANNELS, 
    PUBLISH_SCHEDULE, 
    TIMEZONE, 
    POST_TEMPLATES,
    LOG_LEVEL,
    LOG_FILE
)

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

class InteractiveBot:
    """Интерактивный бот с командами"""
    
    def __init__(self, bot_token: str):
        self.bot_token = bot_token
        self.publisher = TelegramPublisher(bot_token)
        self.application = None
        
    async def start_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
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
        
        await update.message.reply_text(welcome_text, parse_mode='HTML')
    
    async def help_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
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
        await update.message.reply_text(help_text, parse_mode='HTML')
    
    async def post_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Обработчик команды /post"""
        # Получаем текст сообщения (все после /post)
        if context.args:
            message_text = ' '.join(context.args)
        else:
            # Если текст не указан, используем шаблон по умолчанию
            current_time = self.publisher.get_current_time_moscow()
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
        await update.message.reply_text(
            f"🚀 Начинаю публикацию в {len(self.publisher.channels)} каналов...\n"
            f"📝 Текст: {message_text[:100]}{'...' if len(message_text) > 100 else ''}"
        )
        
        try:
            # Публикуем во все каналы
            results = await self.publisher.publish_to_all_channels(message_text)
            
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
            
            await update.message.reply_text(report, parse_mode='HTML')
            
        except Exception as e:
            await update.message.reply_text(f"❌ Ошибка при публикации: {e}")
            logger.error(f"Ошибка в команде /post: {e}")
    
    async def status_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Обработчик команды /status"""
        try:
            # Получаем информацию о боте
            bot_info = await self.publisher.bot.get_me()
            current_time = self.publisher.get_current_time_moscow()
            
            status_text = f"""
🤖 <b>Статус бота:</b>

👤 Бот: @{bot_info.username}
🕐 Текущее время: {current_time.strftime('%H:%M:%S')} МСК
📢 Каналов: {len(self.publisher.channels)}
⏰ Расписание: {', '.join(PUBLISH_SCHEDULE)} МСК

<b>Следующие публикации:</b>
"""
            
            # Показываем ближайшие запланированные посты
            for time_str in sorted(POST_TEMPLATES.keys()):
                template = POST_TEMPLATES[time_str]
                status_text += f"• {time_str} - {template['text'][:50]}...\n"
            
            await update.message.reply_text(status_text, parse_mode='HTML')
            
        except Exception as e:
            await update.message.reply_text(f"❌ Ошибка при получении статуса: {e}")
            logger.error(f"Ошибка в команде /status: {e}")
    
    async def handle_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Обработчик обычных сообщений"""
        await update.message.reply_text(
            "👋 Привет! Используй /help для просмотра доступных команд."
        )

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

async def main():
    """Основная функция"""
    logger.info("🤖 Запуск интерактивного Telegram бота")
    
    # Проверяем токен
    if BOT_TOKEN == 'YOUR_BOT_TOKEN_HERE':
        logger.error("❌ Необходимо указать BOT_TOKEN в config.py или переменной окружения")
        return
    
    # Создаем экземпляр интерактивного бота
    interactive_bot = InteractiveBot(BOT_TOKEN)
    
    # Создаем приложение
    application = Application.builder().token(BOT_TOKEN).build()
    interactive_bot.application = application
    
    # Добавляем обработчики команд
    application.add_handler(CommandHandler("start", interactive_bot.start_command))
    application.add_handler(CommandHandler("help", interactive_bot.help_command))
    application.add_handler(CommandHandler("post", interactive_bot.post_command))
    application.add_handler(CommandHandler("status", interactive_bot.status_command))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, interactive_bot.handle_message))
    
    # Тестируем подключение к боту
    try:
        bot_info = await interactive_bot.publisher.bot.get_me()
        logger.info(f"✅ Бот подключен: @{bot_info.username}")
    except Exception as e:
        logger.error(f"❌ Ошибка подключения к боту: {e}")
        return
    
    # Запускаем планировщик в отдельном потоке
    scheduler = Scheduler(interactive_bot.publisher)
    scheduler_thread = threading.Thread(target=scheduler.run_scheduler, daemon=True)
    scheduler_thread.start()
    
    logger.info("⏰ Планировщик настроен и запущен")
    logger.info(f"📅 Расписание: {', '.join(PUBLISH_SCHEDULE)} МСК")
    logger.info(f"📢 Каналы: {len(CHANNELS)} каналов")
    logger.info("🎯 Интерактивные команды: /start, /help, /post, /status")
    
    # Запускаем бота
    try:
        await application.run_polling()
    except KeyboardInterrupt:
        logger.info("👋 Бот остановлен пользователем")

if __name__ == "__main__":
    asyncio.run(main())
