# 📤 Загрузка проекта на GitHub

## 🛠️ Установка Git

Если Git не установлен, скачай его с официального сайта:
- **Скачать Git:** https://git-scm.com/download/win
- Выбери "Windows" и скачай установщик
- Запусти установщик и следуй инструкциям

## 🚀 Пошаговая инструкция

### 1. Установи Git (если не установлен)
```bash
# Проверь, установлен ли Git
git --version
```

### 2. Создай репозиторий на GitHub
1. Зайди на https://github.com
2. Нажми кнопку "New repository" (зеленая кнопка)
3. Введи название: `TelegramBOT` или `telegram-autopost-bot`
4. Выбери "Public" или "Private"
5. **НЕ** ставь галочки на "Add a README file", "Add .gitignore", "Choose a license"
6. Нажми "Create repository"

### 3. Инициализируй Git в проекте
```bash
# Перейди в папку проекта
cd C:\Users\admin\Desktop\TelegramBOT

# Инициализируй Git
git init

# Добавь все файлы
git add .

# Сделай первый коммит
git commit -m "Initial commit: Telegram bot with interactive commands"
```

### 4. Подключи к GitHub
```bash
# Замени YOUR_USERNAME на свой GitHub username
# Замени YOUR_REPOSITORY на название репозитория
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPOSITORY.git

# Загрузи на GitHub
git branch -M main
git push -u origin main
```

### 5. Альтернативный способ (через GitHub Desktop)
1. Скачай GitHub Desktop: https://desktop.github.com/
2. Установи и войди в аккаунт
3. Нажми "Add an Existing Repository from your Hard Drive"
4. Выбери папку `C:\Users\admin\Desktop\TelegramBOT`
5. Нажми "Publish repository"
6. Введи название и описание
7. Нажми "Publish repository"

## 📝 Что будет загружено

### Основные файлы:
- `interactive_bot.py` - Интерактивный бот с командами
- `telegram_bot.py` - Автоматический бот
- `config.py` - Конфигурация
- `requirements.txt` - Зависимости
- `README.md` - Документация

### Новые файлы:
- `start_interactive_bot.py` - Запуск интерактивного бота
- `start_interactive.bat` - Удобный запуск
- `test_final.py` - Тестирование
- `QUICK_START.md` - Быстрый старт
- `.gitignore` - Исключения для Git

### НЕ будет загружено:
- `bot.log` - Логи (в .gitignore)
- `__pycache__/` - Кэш Python
- `.env` - Переменные окружения

## 🔒 Безопасность

**ВАЖНО:** В файле `config.py` есть твой токен бота. Перед загрузкой на GitHub:

1. **Создай файл `config_example.py`:**
```python
# Конфигурация бота (пример)
import os
from typing import List, Dict

# Токен бота (получите у @BotFather)
BOT_TOKEN = os.getenv('BOT_TOKEN', 'YOUR_BOT_TOKEN_HERE')

# Список каналов для публикации
CHANNELS = [
    -1001234567890,  # Замените на ваши ID каналов
    -1001234567891,
    # ... добавьте все каналы
]

# Остальные настройки...
```

2. **Обнови `config.py`** - замени токен на `'YOUR_BOT_TOKEN_HERE'`

3. **Добавь в README инструкцию** по настройке токена

## 📋 После загрузки

1. Обнови README.md с инструкциями по установке
2. Добавь секцию "Установка" с командами
3. Укажи, что нужно настроить `config.py`
4. Добавь примеры использования

## 🎯 Готовые команды для копирования

```bash
# Инициализация
git init
git add .
git commit -m "Initial commit: Telegram bot with interactive commands"

# Подключение к GitHub (замени на свои данные)
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPOSITORY.git
git branch -M main
git push -u origin main
```

---

**Готово! Твой проект будет на GitHub! 🚀**
