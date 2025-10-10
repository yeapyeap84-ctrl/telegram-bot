# Dockerfile для Telegram бота
FROM python:3.11-slim

# Устанавливаем рабочую директорию
WORKDIR /app

# Копируем файлы зависимостей
COPY requirements.txt .

# Устанавливаем зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Добавляем Flask для веб-интерфейса
RUN pip install --no-cache-dir flask

# Копируем исходный код
COPY . .

# Создаем пользователя для безопасности
RUN useradd -m -u 1000 botuser && chown -R botuser:botuser /app
USER botuser

# Открываем порт для веб-интерфейса
EXPOSE 5000

# Команда запуска
CMD ["python", "bot_hosting.py"]
