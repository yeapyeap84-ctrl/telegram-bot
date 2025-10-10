import asyncio
import logging
import schedule
import time
from datetime import datetime
from typing import List, Dict, Optional
import pytz
from telegram import Bot
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
    logger.info("🤖 Запуск Telegram бота для публикации постов")
    
    # Проверяем токен
    if BOT_TOKEN == 'YOUR_BOT_TOKEN_HERE':
        logger.error("❌ Необходимо указать BOT_TOKEN в config.py или переменной окружения")
        return
    
    # Создаем экземпляры классов
    publisher = TelegramPublisher(BOT_TOKEN)
    scheduler = Scheduler(publisher)
    
    # Тестируем подключение к боту
    try:
        bot_info = await publisher.bot.get_me()
        logger.info(f"✅ Бот подключен: @{bot_info.username}")
    except Exception as e:
        logger.error(f"❌ Ошибка подключения к боту: {e}")
        return
    
    # Запускаем планировщик в отдельном потоке
    import threading
    scheduler_thread = threading.Thread(target=scheduler.run_scheduler, daemon=True)
    scheduler_thread.start()
    
    logger.info("⏰ Планировщик настроен и запущен")
    logger.info(f"📅 Расписание: {', '.join(PUBLISH_SCHEDULE)} МСК")
    logger.info(f"📢 Каналы: {len(CHANNELS)} каналов")
    
    # Основной цикл
    try:
        while True:
            await asyncio.sleep(1)
    except KeyboardInterrupt:
        logger.info("👋 Бот остановлен пользователем")

if __name__ == "__main__":
    asyncio.run(main())

