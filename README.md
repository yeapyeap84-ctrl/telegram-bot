# Telegram Bot для автоматической публикации постов

Этот бот автоматически публикует сообщения в 10 Telegram каналов по расписанию (9:00 и 16:00 МСК).

## 🚀 Возможности

- ✅ Автоматическая публикация в 10 каналов одновременно
- ⏰ Настраиваемое расписание (по умолчанию 9:00 и 16:00 МСК)
- 🔄 Параллельная отправка сообщений для быстрой работы
- 📝 Настраиваемые шаблоны сообщений
- 📊 Подробное логирование всех операций
- 🛡️ Обработка ошибок и повторные попытки

## 📋 Требования

- Python 3.8+
- Telegram Bot Token (получить у @BotFather)
- Права администратора в каналах для публикации

## 🛠️ Установка

1. **Клонируйте репозиторий или скачайте файлы**

2. **Установите зависимости:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Настройте конфигурацию:**
   
   Отредактируйте файл `config.py`:
   ```python
   # Укажите токен вашего бота
   BOT_TOKEN = 'YOUR_BOT_TOKEN_HERE'
   
   # Укажите ваши каналы
   CHANNELS = [
       '@your_channel1',
       '@your_channel2',
       # ... добавьте все 10 каналов
   ]
   ```

4. **Создайте файл .env (опционально):**
   ```bash
   cp env_example.txt .env
   ```
   
   И заполните токен бота в .env файле.

## ⚙️ Настройка

### 1. Получение токена бота

1. Напишите @BotFather в Telegram
2. Отправьте команду `/newbot`
3. Следуйте инструкциям для создания бота
4. Скопируйте полученный токен

### 2. Настройка каналов

В файле `config.py` замените `CHANNELS` на ID ваших каналов:

```python
CHANNELS = [
    -1001234567890,  # ID первого канала
    -1001234567891,  # ID второго канала
    -1001234567892,  # ID третьего канала
    # ... добавьте все 10 каналов
]
```

**Как получить ID канала:**

1. **Способ 1 (через @userinfobot):**
   - Добавьте бота в канал как администратора
   - Отправьте любое сообщение в канал
   - Перешлите это сообщение боту @userinfobot
   - Скопируйте ID канала (начинается с -100)

2. **Способ 2 (через @RawDataBot):**
   - Отправьте сообщение в канал
   - Перешлите его боту @RawDataBot
   - Найдите 'chat_id' в ответе

3. **Способ 3 (автоматический):**
   ```bash
   python get_channel_ids.py
   ```

**Важно:** 
- Бот должен быть добавлен в каналы как администратор
- ID канала всегда начинается с -100
- Использование ID более надежно, чем @username

### 3. Настройка расписания

По умолчанию бот публикует в 08:00, 12:00, 16:00 и 19:00 МСК. Чтобы изменить время, отредактируйте `PUBLISH_SCHEDULE`:

```python
PUBLISH_SCHEDULE = [
    '08:00',  # 8:00 утра
    '12:00',  # 12:00 дня
    '16:00',  # 16:00 дня
    '19:00',  # 19:00 вечера
]
```

### 4. Настройка сообщений

В `config.py` настройте шаблоны сообщений:

```python
POST_TEMPLATES = {
    '08:00': {
        'text': '🌅 Доброе утро! Начинаем новый день с позитивом!',
        'parse_mode': 'HTML'
    },
    '12:00': {
        'text': '☀️ Полдень! Время для обеда и перерыва!',
        'parse_mode': 'HTML'
    },
    '16:00': {
        'text': '☕ Время для кофе-брейка! Как дела?',
        'parse_mode': 'HTML'
    },
    '19:00': {
        'text': '🌆 Вечер! Завершаем день на позитивной ноте!',
        'parse_mode': 'HTML'
    }
}
```

## 🚀 Запуск

```bash
python telegram_bot.py
```

Бот запустится и будет работать в фоновом режиме, публикуя сообщения по расписанию.

## 📊 Мониторинг

### Логи

Все действия бота записываются в файл `bot.log`:

```
2024-01-15 09:00:01 - INFO - 🚀 Начинаем публикацию сообщения в 10 каналов
2024-01-15 09:00:02 - INFO - ✅ Сообщение успешно отправлено в @channel1
2024-01-15 09:00:03 - INFO - ✅ Сообщение успешно отправлено в @channel2
...
```

### Статус публикации

Бот выводит подробную информацию о каждой публикации:
- ✅ Успешная отправка
- ❌ Ошибка отправки
- 📊 Общая статистика

## 🔧 Расширенные настройки

### Добавление медиафайлов

Чтобы отправлять изображения или видео, измените метод `publish_to_channel` в `telegram_bot.py`:

```python
# Для отправки фото
await self.bot.send_photo(
    chat_id=channel,
    photo='path/to/image.jpg',
    caption=message,
    parse_mode=parse_mode
)

# Для отправки видео
await self.bot.send_video(
    chat_id=channel,
    video='path/to/video.mp4',
    caption=message,
    parse_mode=parse_mode
)
```

### Добавление кнопок

Для добавления inline-кнопок используйте:

```python
from telegram import InlineKeyboardButton, InlineKeyboardMarkup

keyboard = [
    [InlineKeyboardButton("Кнопка 1", url="https://example.com")],
    [InlineKeyboardButton("Кнопка 2", callback_data="button2")]
]
reply_markup = InlineKeyboardMarkup(keyboard)

await self.bot.send_message(
    chat_id=channel,
    text=message,
    parse_mode=parse_mode,
    reply_markup=reply_markup
)
```

## 🛠️ Устранение неполадок

### Ошибка "Chat not found"
- Убедитесь, что бот добавлен в каналы как администратор
- Проверьте правильность написания @username или ID канала

### Ошибка "Forbidden: bot is not a member"
- Добавьте бота в каналы как администратора
- Убедитесь, что у бота есть права на отправку сообщений

### Ошибка "Invalid token"
- Проверьте правильность токена бота
- Убедитесь, что токен скопирован полностью

## 📝 Структура проекта

```
TelegramBOT/
├── telegram_bot.py      # Основной файл бота
├── config.py           # Конфигурация
├── test_bot.py         # Тестирование бота
├── get_channel_ids.py  # Получение ID каналов
├── start.py            # Удобный запуск
├── start.bat           # Запуск для Windows
├── requirements.txt    # Зависимости
├── env_example.txt     # Пример файла окружения
├── bot.log            # Логи (создается автоматически)
└── README.md          # Документация
```

## 🔄 Автозапуск (Linux/macOS)

Для автоматического запуска бота при загрузке системы создайте systemd сервис:

```bash
sudo nano /etc/systemd/system/telegram-bot.service
```

Содержимое файла:
```ini
[Unit]
Description=Telegram Bot
After=network.target

[Service]
Type=simple
User=your_username
WorkingDirectory=/path/to/TelegramBOT
ExecStart=/usr/bin/python3 /path/to/TelegramBOT/telegram_bot.py
Restart=always

[Install]
WantedBy=multi-user.target
```

Затем:
```bash
sudo systemctl enable telegram-bot.service
sudo systemctl start telegram-bot.service
```

## 📞 Поддержка

При возникновении проблем:
1. Проверьте логи в файле `bot.log`
2. Убедитесь в правильности настроек в `config.py`
3. Проверьте права бота в каналах

---

**Удачного использования! 🚀**

