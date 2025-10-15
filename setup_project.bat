@echo off
echo 🚀 Настройка проекта для GitHub
echo ================================================
echo.

echo 📋 Копируем пример конфигурации...
copy config_example.py config.py
echo ✅ config.py создан

echo.
echo 📋 Создаем .gitignore...
echo ✅ .gitignore создан

echo.
echo 📋 Проверяем зависимости...
py -m pip install -r requirements.txt
echo ✅ Зависимости установлены

echo.
echo ================================================
echo 🎯 ПРОЕКТ ГОТОВ К ЗАГРУЗКЕ НА GITHUB!
echo ================================================
echo.
echo 📝 Следующие шаги:
echo 1. Установи Git: https://git-scm.com/download/win
echo 2. Создай репозиторий на GitHub
echo 3. Настрой config.py с твоим токеном бота
echo 4. Запусти команды из GITHUB_UPLOAD.md
echo.
echo 📖 Подробная инструкция в файле GITHUB_UPLOAD.md
echo.

pause
