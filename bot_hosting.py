#!/usr/bin/env python3
"""
Telegram Bot для хостинга с веб-интерфейсом
Работает 24/7 на сервере
"""

import asyncio
import logging
import schedule
import time
import threading
from datetime import datetime
from typing import List, Dict, Optional
import pytz
from telegram import Bot
from telegram.error import TelegramError
from flask import Flask, render_template_string, jsonify
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

# Flask приложение для веб-интерфейса
app = Flask(__name__)

# Глобальные переменные для мониторинга
bot_status = {
    'running': False,
    'last_publish': None,
    'total_published': 0,
    'errors': 0,
    'start_time': None
}

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
            bot_status['errors'] += 1
            return False
        except Exception as e:
            logger.error(f"❌ Неожиданная ошибка при отправке в {channel}: {e}")
            bot_status['errors'] += 1
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
        
        # Обновляем статистику
        bot_status['total_published'] += successful
        bot_status['last_publish'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
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
        
        while bot_status['running']:
            schedule.run_pending()
            time.sleep(60)  # Проверяем каждую минуту

# Веб-интерфейс
@app.route('/')
def dashboard():
    """Главная страница с мониторингом"""
    template = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Telegram Bot Monitor</title>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <style>
            body { font-family: Arial, sans-serif; margin: 20px; background: #f5f5f5; }
            .container { max-width: 800px; margin: 0 auto; background: white; padding: 20px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
            .status { padding: 15px; margin: 10px 0; border-radius: 5px; }
            .status.running { background: #d4edda; border: 1px solid #c3e6cb; color: #155724; }
            .status.stopped { background: #f8d7da; border: 1px solid #f5c6cb; color: #721c24; }
            .stats { display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 15px; margin: 20px 0; }
            .stat-card { background: #e9ecef; padding: 15px; border-radius: 5px; text-align: center; }
            .stat-number { font-size: 24px; font-weight: bold; color: #007bff; }
            .schedule { background: #f8f9fa; padding: 15px; border-radius: 5px; margin: 20px 0; }
            .schedule-item { padding: 5px 0; border-bottom: 1px solid #dee2e6; }
            .refresh-btn { background: #007bff; color: white; padding: 10px 20px; border: none; border-radius: 5px; cursor: pointer; }
            .refresh-btn:hover { background: #0056b3; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🤖 Telegram Bot Monitor</h1>
            
            <div class="status {{ 'running' if status.running else 'stopped' }}">
                <strong>Статус:</strong> {{ 'Работает' if status.running else 'Остановлен' }}
            </div>
            
            <div class="stats">
                <div class="stat-card">
                    <div class="stat-number">{{ status.total_published }}</div>
                    <div>Опубликовано постов</div>
                </div>
                <div class="stat-card">
                    <div class="stat-number">{{ status.errors }}</div>
                    <div>Ошибок</div>
                </div>
                <div class="stat-card">
                    <div class="stat-number">{{ channels_count }}</div>
                    <div>Каналов</div>
                </div>
                <div class="stat-card">
                    <div class="stat-number">{{ schedule_count }}</div>
                    <div>Публикаций в день</div>
                </div>
            </div>
            
            <div class="schedule">
                <h3>📅 Расписание публикации</h3>
                {% for time in schedule_times %}
                <div class="schedule-item">{{ time }} МСК</div>
                {% endfor %}
            </div>
            
            <div>
                <strong>Последняя публикация:</strong> {{ status.last_publish or 'Нет данных' }}
            </div>
            
            <div>
                <strong>Время запуска:</strong> {{ status.start_time or 'Нет данных' }}
            </div>
            
            <button class="refresh-btn" onclick="location.reload()">🔄 Обновить</button>
        </div>
        
        <script>
            // Автообновление каждые 30 секунд
            setTimeout(function() {
                location.reload();
            }, 30000);
        </script>
    </body>
    </html>
    """
    
    return render_template_string(template, 
                                status=bot_status,
                                channels_count=len(CHANNELS),
                                schedule_count=len(PUBLISH_SCHEDULE),
                                schedule_times=PUBLISH_SCHEDULE)

@app.route('/api/status')
def api_status():
    """API для получения статуса"""
    return jsonify(bot_status)

@app.route('/api/test')
def test_publish():
    """API для тестовой публикации"""
    async def test():
        publisher = TelegramPublisher(BOT_TOKEN)
        message = "🧪 Тестовое сообщение с хостинга"
        results = await publisher.publish_to_all_channels(message)
        return {"success": True, "results": results}
    
    # Запускаем тест в новом цикле событий
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    result = loop.run_until_complete(test())
    loop.close()
    
    return jsonify(result)

async def main():
    """Основная функция"""
    logger.info("🤖 Запуск Telegram бота для хостинга")
    
    # Проверяем токен
    if BOT_TOKEN == 'YOUR_BOT_TOKEN_HERE':
        logger.error("❌ Необходимо указать BOT_TOKEN в config.py")
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
    
    # Устанавливаем статус
    bot_status['running'] = True
    bot_status['start_time'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    # Запускаем планировщик в отдельном потоке
    scheduler_thread = threading.Thread(target=scheduler.run_scheduler, daemon=True)
    scheduler_thread.start()
    
    logger.info("⏰ Планировщик настроен и запущен")
    logger.info(f"📅 Расписание: {', '.join(PUBLISH_SCHEDULE)} МСК")
    logger.info(f"📢 Каналы: {len(CHANNELS)} каналов")
    logger.info("🌐 Веб-интерфейс доступен на http://localhost:5000")
    
    # Запускаем Flask сервер
    app.run(host='0.0.0.0', port=5000, debug=False)

if __name__ == "__main__":
    asyncio.run(main())
