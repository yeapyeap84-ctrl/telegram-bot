# 🚀 Деплой Telegram бота на хостинг

Этот гайд поможет вам развернуть Telegram бота на различных хостинг-платформах для работы 24/7.

## 📋 Требования

- Python 3.8+
- Telegram Bot Token
- Аккаунт на выбранной хостинг-платформе

## 🎯 Варианты хостинга

### 1. 🖥️ Локальная машина (Docker)

**Для тестирования и разработки:**

```bash
# Установите Docker и Docker Compose
# Затем запустите:
python deploy.py
# Выберите опцию 1
```

**Ручной запуск:**
```bash
docker-compose up -d
```

**Веб-интерфейс:** http://localhost:5000

### 2. ☁️ Heroku (Бесплатно)

**Преимущества:**
- ✅ Бесплатный тариф
- ✅ Автоматический деплой
- ✅ Простота настройки

**Инструкции:**
1. Установите [Heroku CLI](https://devcenter.heroku.com/articles/heroku-cli)
2. Войдите в аккаунт: `heroku login`
3. Создайте приложение: `heroku create your-bot-name`
4. Установите переменные:
   ```bash
   heroku config:set BOT_TOKEN=your_bot_token_here
   ```
5. Деплой: `git push heroku main`
6. Запуск: `heroku ps:scale web=1`

**Ограничения бесплатного тарифа:**
- 550 часов в месяц
- Спит после 30 минут неактивности

### 3. 🚂 Railway (Рекомендуется)

**Преимущества:**
- ✅ $5 в месяц за 24/7
- ✅ Автоматический деплой
- ✅ Простой интерфейс

**Инструкции:**
1. Зарегистрируйтесь на [railway.app](https://railway.app)
2. Установите Railway CLI: `npm install -g @railway/cli`
3. Войдите: `railway login`
4. Создайте проект: `railway init`
5. Установите переменные:
   ```bash
   railway variables set BOT_TOKEN=your_bot_token_here
   ```
6. Деплой: `railway up`

### 4. 🎨 Render (Бесплатно)

**Преимущества:**
- ✅ Бесплатный тариф
- ✅ Автоматический деплой из GitHub
- ✅ Простая настройка

**Инструкции:**
1. Зарегистрируйтесь на [render.com](https://render.com)
2. Подключите GitHub репозиторий
3. Создайте Web Service
4. Настройки:
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `python bot_hosting.py`
   - **Environment Variables:** `BOT_TOKEN=your_bot_token_here`

### 5. 🌐 DigitalOcean (VPS)

**Преимущества:**
- ✅ Полный контроль
- ✅ $5-10 в месяц
- ✅ Высокая производительность

**Инструкции:**
1. Создайте Droplet на [DigitalOcean](https://digitalocean.com)
2. Подключитесь по SSH
3. Установите Docker:
   ```bash
   curl -fsSL https://get.docker.com -o get-docker.sh
   sh get-docker.sh
   ```
4. Клонируйте репозиторий
5. Запустите: `docker-compose up -d`

## 🔧 Настройка переменных окружения

Создайте файл `.env` в корне проекта:

```env
BOT_TOKEN=your_bot_token_here
WEB_HOST=0.0.0.0
WEB_PORT=5000
LOG_LEVEL=INFO
```

## 📊 Мониторинг

После деплоя доступен веб-интерфейс:

- **Главная страница:** `http://your-domain.com`
- **API статуса:** `http://your-domain.com/api/status`
- **Тест публикации:** `http://your-domain.com/api/test`

## 🛠️ Автоматический деплой

Используйте скрипт для быстрого деплоя:

```bash
python deploy.py
```

Выберите нужную платформу и следуйте инструкциям.

## 🔄 Обновление бота

Для обновления бота на хостинге:

1. **Heroku:** `git push heroku main`
2. **Railway:** `railway up`
3. **Render:** Автоматически при push в GitHub
4. **Docker:** `docker-compose down && docker-compose up -d`

## 📝 Логи и отладка

**Просмотр логов:**
- **Heroku:** `heroku logs --tail`
- **Railway:** `railway logs`
- **Render:** В панели управления
- **Docker:** `docker-compose logs -f`

## 🚨 Устранение неполадок

### Бот не запускается
1. Проверьте токен бота
2. Убедитесь, что бот добавлен в каналы
3. Проверьте логи на ошибки

### Веб-интерфейс недоступен
1. Проверьте, что порт 5000 открыт
2. Убедитесь, что переменные окружения установлены
3. Проверьте статус контейнера

### Публикация не работает
1. Проверьте права бота в каналах
2. Убедитесь в правильности ID каналов
3. Проверьте расписание в конфигурации

## 💡 Рекомендации

1. **Для тестирования:** Используйте локальный Docker
2. **Для продакшена:** Railway или DigitalOcean
3. **Для бесплатного хостинга:** Render или Heroku
4. **Для максимального контроля:** DigitalOcean VPS

## 📞 Поддержка

При возникновении проблем:
1. Проверьте логи бота
2. Убедитесь в правильности настроек
3. Проверьте статус хостинг-платформы

---

**Удачного деплоя! 🚀**
