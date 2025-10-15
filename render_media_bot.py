#!/usr/bin/env python3
"""
Telegram бот с поддержкой медиа для Render.com
Поддерживает текст, фото, видео, документы
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
import requests
import json
import base64
import io

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

class MediaTelegramBot:
    """Telegram бот с поддержкой медиа"""
    
    def __init__(self, bot_token: str):
        self.bot_token = bot_token
        self.api_url = f"https://api.telegram.org/bot{bot_token}"
        self.channels = CHANNELS
        self.timezone = pytz.timezone(TIMEZONE)
        self.last_update_id = 0
        
    def send_message(self, chat_id: str, text: str, parse_mode: str = 'HTML') -> bool:
        """Отправка текстового сообщения"""
        try:
            url = f"{self.api_url}/sendMessage"
            data = {
                'chat_id': chat_id,
                'text': text,
                'parse_mode': parse_mode
            }
            response = requests.post(url, data=data, timeout=10)
            
            if response.status_code == 200:
                logger.info(f"✅ Сообщение отправлено в {chat_id}")
                return True
            else:
                logger.error(f"❌ Ошибка отправки в {chat_id}: {response.text}")
                return False
                
        except Exception as e:
            logger.error(f"❌ Ошибка при отправке в {chat_id}: {e}")
            return False
    
    def send_photo(self, chat_id: str, photo_url: str, caption: str = "", parse_mode: str = 'HTML') -> bool:
        """Отправка фотографии"""
        try:
            url = f"{self.api_url}/sendPhoto"
            data = {
                'chat_id': chat_id,
                'photo': photo_url,
                'caption': caption,
                'parse_mode': parse_mode
            }
            response = requests.post(url, data=data, timeout=15)
            
            if response.status_code == 200:
                logger.info(f"✅ Фото отправлено в {chat_id}")
                return True
            else:
                logger.error(f"❌ Ошибка отправки фото в {chat_id}: {response.text}")
                return False
                
        except Exception as e:
            logger.error(f"❌ Ошибка при отправке фото в {chat_id}: {e}")
            return False
    
    def send_video(self, chat_id: str, video_url: str, caption: str = "", parse_mode: str = 'HTML') -> bool:
        """Отправка видео"""
        try:
            url = f"{self.api_url}/sendVideo"
            data = {
                'chat_id': chat_id,
                'video': video_url,
                'caption': caption,
                'parse_mode': parse_mode
            }
            response = requests.post(url, data=data, timeout=20)
            
            if response.status_code == 200:
                logger.info(f"✅ Видео отправлено в {chat_id}")
                return True
            else:
                logger.error(f"❌ Ошибка отправки видео в {chat_id}: {response.text}")
                return False
                
        except Exception as e:
            logger.error(f"❌ Ошибка при отправке видео в {chat_id}: {e}")
            return False
    
    def send_document(self, chat_id: str, document_url: str, caption: str = "", parse_mode: str = 'HTML') -> bool:
        """Отправка документа"""
        try:
            url = f"{self.api_url}/sendDocument"
            data = {
                'chat_id': chat_id,
                'document': document_url,
                'caption': caption,
                'parse_mode': parse_mode
            }
            response = requests.post(url, data=data, timeout=20)
            
            if response.status_code == 200:
                logger.info(f"✅ Документ отправлен в {chat_id}")
                return True
            else:
                logger.error(f"❌ Ошибка отправки документа в {chat_id}: {response.text}")
                return False
                
        except Exception as e:
            logger.error(f"❌ Ошибка при отправке документа в {chat_id}: {e}")
            return False
    
    def send_media_to_all_channels(self, media_type: str, media_url: str, caption: str = "", parse_mode: str = 'HTML') -> Dict[str, bool]:
        """Отправка медиа во все каналы"""
        results = {}
        
        logger.info(f"🚀 Начинаем публикацию {media_type} в {len(self.channels)} каналов")
        
        for channel in self.channels:
            if media_type == 'photo':
                success = self.send_photo(str(channel), media_url, caption, parse_mode)
            elif media_type == 'video':
                success = self.send_video(str(channel), media_url, caption, parse_mode)
            elif media_type == 'document':
                success = self.send_document(str(channel), media_url, caption, parse_mode)
            else:
                success = self.send_message(str(channel), caption, parse_mode)
            
            results[channel] = success
        
        successful = sum(1 for success in results.values() if success)
        failed = len(results) - successful
        
        logger.info(f"📊 Результаты: {successful} успешно, {failed} с ошибками")
        return results
    
    def send_message_to_all_channels(self, text: str, parse_mode: str = 'HTML') -> Dict[str, bool]:
        """Отправка текстового сообщения во все каналы"""
        results = {}
        
        logger.info(f"🚀 Начинаем публикацию в {len(self.channels)} каналов")
        
        for channel in self.channels:
            success = self.send_message(str(channel), text, parse_mode)
            results[channel] = success
        
        successful = sum(1 for success in results.values() if success)
        failed = len(results) - successful
        
        logger.info(f"📊 Результаты: {successful} успешно, {failed} с ошибками")
        return results
    
    def get_updates(self):
        """Получение обновлений от Telegram"""
        try:
            url = f"{self.api_url}/getUpdates"
            params = {
                'offset': self.last_update_id + 1,
                'timeout': 10
            }
            response = requests.get(url, params=params, timeout=15)
            
            if response.status_code == 200:
                data = response.json()
                if data.get('ok'):
                    return data.get('result', [])
            return []
            
        except Exception as e:
            logger.error(f"❌ Ошибка получения обновлений: {e}")
            return []
    
    def process_message(self, message):
        """Обработка сообщения"""
        try:
            chat_id = message['chat']['id']
            text = message.get('text', '')
            
            if text.startswith('/start'):
                welcome_text = """
🤖 <b>Добро пожаловать в бот автопостов!</b>

<b>Доступные команды:</b>
/post - Отправить пост во все каналы
/photo - Отправить фото во все каналы
/video - Отправить видео во все каналы
/status - Проверить статус бота
/help - Показать справку

<b>Автоматические посты:</b>
Бот автоматически публикует посты по расписанию:
"""
                for time in PUBLISH_SCHEDULE:
                    welcome_text += f"• {time} МСК\n"
                
                self.send_message(chat_id, welcome_text, 'HTML')
                
            elif text.startswith('/help'):
                help_text = """
📖 <b>Справка по командам:</b>

<b>/post</b> - Отправить текст во все каналы
Использование: /post [текст сообщения]
Пример: /post Привет всем!

<b>/photo</b> - Отправить фото во все каналы
Использование: /photo [URL фото] [подпись]
Пример: /photo https://example.com/photo.jpg Моя фотография

<b>/video</b> - Отправить видео во все каналы
Использование: /video [URL видео] [подпись]
Пример: /video https://example.com/video.mp4 Мое видео

<b>/status</b> - Проверить статус бота
Показывает количество каналов и время следующей публикации

<b>/help</b> - Показать эту справку

<b>Автоматические посты:</b>
Бот публикует посты по расписанию в указанное время.
"""
                self.send_message(chat_id, help_text, 'HTML')
                
            elif text.startswith('/post'):
                # Получаем текст после /post
                post_text = text[5:].strip()
                
                if not post_text:
                    # Если текст не указан, используем шаблон
                    current_time = datetime.now(self.timezone)
                    time_str = current_time.strftime('%H:%M')
                    
                    template = None
                    for scheduled_time in sorted(POST_TEMPLATES.keys()):
                        if scheduled_time >= time_str:
                            template = POST_TEMPLATES[scheduled_time]
                            break
                    
                    if not template:
                        template = list(POST_TEMPLATES.values())[0]
                    
                    post_text = template['text']
                
                # Отправляем сообщение о начале публикации
                self.send_message(chat_id, f"🚀 Начинаю публикацию в {len(self.channels)} каналов...")
                
                # Публикуем во все каналы
                results = self.send_message_to_all_channels(post_text)
                
                # Отправляем отчет
                successful = sum(1 for success in results.values() if success)
                failed = len(results) - successful
                
                report = f"""
📊 <b>Результаты публикации:</b>

✅ Успешно: {successful}
❌ Ошибки: {failed}
📤 Всего каналов: {len(results)}
"""
                self.send_message(chat_id, report, 'HTML')
                
            elif text.startswith('/photo'):
                # Получаем URL фото и подпись после /photo
                parts = text[6:].strip().split(' ', 1)
                photo_url = parts[0] if parts else ""
                caption = parts[1] if len(parts) > 1 else ""
                
                if not photo_url:
                    self.send_message(chat_id, "❌ Укажите URL фото: /photo https://example.com/photo.jpg [подпись]")
                    return
                
                # Отправляем сообщение о начале публикации
                self.send_message(chat_id, f"📸 Начинаю публикацию фото в {len(self.channels)} каналов...")
                
                # Публикуем во все каналы
                results = self.send_media_to_all_channels('photo', photo_url, caption)
                
                # Отправляем отчет
                successful = sum(1 for success in results.values() if success)
                failed = len(results) - successful
                
                report = f"""
📊 <b>Результаты публикации фото:</b>

✅ Успешно: {successful}
❌ Ошибки: {failed}
📤 Всего каналов: {len(results)}
"""
                self.send_message(chat_id, report, 'HTML')
                
            elif text.startswith('/video'):
                # Получаем URL видео и подпись после /video
                parts = text[6:].strip().split(' ', 1)
                video_url = parts[0] if parts else ""
                caption = parts[1] if len(parts) > 1 else ""
                
                if not video_url:
                    self.send_message(chat_id, "❌ Укажите URL видео: /video https://example.com/video.mp4 [подпись]")
                    return
                
                # Отправляем сообщение о начале публикации
                self.send_message(chat_id, f"🎥 Начинаю публикацию видео в {len(self.channels)} каналов...")
                
                # Публикуем во все каналы
                results = self.send_media_to_all_channels('video', video_url, caption)
                
                # Отправляем отчет
                successful = sum(1 for success in results.values() if success)
                failed = len(results) - successful
                
                report = f"""
📊 <b>Результаты публикации видео:</b>

✅ Успешно: {successful}
❌ Ошибки: {failed}
📤 Всего каналов: {len(results)}
"""
                self.send_message(chat_id, report, 'HTML')
                
            elif text.startswith('/status'):
                current_time = datetime.now(self.timezone)
                
                status_text = f"""
🤖 <b>Статус бота:</b>

🕐 Текущее время: {current_time.strftime('%H:%M:%S')} МСК
📢 Каналов: {len(self.channels)}
⏰ Расписание: {', '.join(PUBLISH_SCHEDULE)} МСК

<b>Поддерживаемые типы медиа:</b>
• Текст (/post)
• Фото (/photo)
• Видео (/video)

<b>Следующие публикации:</b>
"""
                
                for time_str in sorted(POST_TEMPLATES.keys()):
                    template = POST_TEMPLATES[time_str]
                    status_text += f"• {time_str} - {template['text'][:50]}...\n"
                
                self.send_message(chat_id, status_text, 'HTML')
                
            else:
                # Обычное сообщение
                self.send_message(chat_id, "👋 Привет! Используй /help для просмотра доступных команд.")
                
        except Exception as e:
            logger.error(f"❌ Ошибка обработки сообщения: {e}")
    
    def run_polling(self):
        """Запуск polling для получения сообщений"""
        logger.info("🚀 Запуск polling для получения сообщений")
        
        while True:
            try:
                updates = self.get_updates()
                
                for update in updates:
                    self.last_update_id = update['update_id']
                    
                    if 'message' in update:
                        self.process_message(update['message'])
                
                time.sleep(1)  # Небольшая пауза между запросами
                
            except Exception as e:
                logger.error(f"❌ Ошибка в polling: {e}")
                time.sleep(5)  # Пауза при ошибке

class Scheduler:
    """Планировщик для автоматической публикации"""
    
    def __init__(self, bot: MediaTelegramBot):
        self.bot = bot
        self.schedule_times = PUBLISH_SCHEDULE
        
    def schedule_posts(self):
        """Настройка расписания публикации"""
        for time_str in self.schedule_times:
            schedule.every().day.at(time_str).do(self.publish_scheduled_post, time_str)
            logger.info(f"⏰ Запланирована публикация на {time_str} МСК")
    
    def publish_scheduled_post(self, time_str: str):
        """Публикация по расписанию"""
        current_time = datetime.now(self.bot.timezone)
        logger.info(f"🕐 Время публикации: {time_str} МСК, текущее время: {current_time.strftime('%H:%M')}")
        
        # Получаем шаблон поста для этого времени
        post_template = POST_TEMPLATES.get(time_str)
        
        if not post_template:
            logger.warning(f"⚠️ Не найден шаблон поста для времени {time_str}")
            return
        
        message = post_template['text']
        parse_mode = post_template.get('parse_mode', 'HTML')
        
        # Публикуем во все каналы
        results = self.bot.send_message_to_all_channels(message, parse_mode)
        
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

def main():
    """Основная функция"""
    logger.info("🤖 Запуск Telegram бота с поддержкой медиа для Render")
    
    # Проверяем токен
    if BOT_TOKEN == 'YOUR_BOT_TOKEN_HERE':
        logger.error("❌ Необходимо указать BOT_TOKEN в config.py или переменной окружения")
        return
    
    # Создаем экземпляр бота
    bot = MediaTelegramBot(BOT_TOKEN)
    
    # Создаем планировщик
    scheduler = Scheduler(bot)
    
    # Запускаем планировщик в отдельном потоке
    scheduler_thread = threading.Thread(target=scheduler.run_scheduler, daemon=True)
    scheduler_thread.start()
    
    logger.info("⏰ Планировщик настроен и запущен")
    logger.info(f"📅 Расписание: {', '.join(PUBLISH_SCHEDULE)} МСК")
    logger.info(f"📢 Каналы: {len(CHANNELS)} каналов")
    logger.info("🎯 Интерактивные команды: /start, /help, /post, /photo, /video, /status")
    
    # Запускаем polling для получения сообщений
    try:
        bot.run_polling()
    except KeyboardInterrupt:
        logger.info("👋 Бот остановлен пользователем")
    except Exception as e:
        logger.error(f"❌ Ошибка при запуске бота: {e}")

if __name__ == "__main__":
    main()
