#!/usr/bin/env python3
"""
Веб-интерфейс для управления Telegram ботом
Позволяет запускать автопосты вручную и мониторить работу
"""

import asyncio
import logging
import threading
import time
from datetime import datetime
from flask import Flask, render_template_string, jsonify, request
from telegram_bot import TelegramPublisher
from config import BOT_TOKEN, CHANNELS, PUBLISH_SCHEDULE, POST_TEMPLATES

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Flask приложение
app = Flask(__name__)

# Глобальные переменные для мониторинга
bot_status = {
    'running': False,
    'last_publish': None,
    'total_published': 0,
    'errors': 0,
    'start_time': None,
    'publisher': None
}

def init_bot():
    """Инициализация бота"""
    if not bot_status['publisher']:
        bot_status['publisher'] = TelegramPublisher(BOT_TOKEN)
        bot_status['running'] = True
        bot_status['start_time'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

@app.route('/')
def dashboard():
    """Главная страница с мониторингом"""
    init_bot()
    
    template = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Telegram Bot Control Panel</title>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <style>
            body { 
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; 
                margin: 0; 
                padding: 20px; 
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                min-height: 100vh;
            }
            .container { 
                max-width: 1200px; 
                margin: 0 auto; 
                background: white; 
                padding: 30px; 
                border-radius: 15px; 
                box-shadow: 0 10px 30px rgba(0,0,0,0.2);
            }
            .header {
                text-align: center;
                margin-bottom: 30px;
                padding-bottom: 20px;
                border-bottom: 2px solid #f0f0f0;
            }
            .status { 
                padding: 20px; 
                margin: 20px 0; 
                border-radius: 10px; 
                font-size: 18px;
                text-align: center;
            }
            .status.running { 
                background: linear-gradient(135deg, #d4edda, #c3e6cb); 
                border: 2px solid #28a745; 
                color: #155724; 
            }
            .status.stopped { 
                background: linear-gradient(135deg, #f8d7da, #f5c6cb); 
                border: 2px solid #dc3545; 
                color: #721c24; 
            }
            .stats { 
                display: grid; 
                grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); 
                gap: 20px; 
                margin: 30px 0; 
            }
            .stat-card { 
                background: linear-gradient(135deg, #e9ecef, #f8f9fa); 
                padding: 25px; 
                border-radius: 10px; 
                text-align: center;
                box-shadow: 0 5px 15px rgba(0,0,0,0.1);
                transition: transform 0.3s ease;
            }
            .stat-card:hover {
                transform: translateY(-5px);
            }
            .stat-number { 
                font-size: 32px; 
                font-weight: bold; 
                color: #007bff; 
                margin-bottom: 10px;
            }
            .controls {
                background: #f8f9fa;
                padding: 25px;
                border-radius: 10px;
                margin: 20px 0;
            }
            .btn {
                background: #007bff;
                color: white;
                padding: 12px 25px;
                border: none;
                border-radius: 8px;
                cursor: pointer;
                font-size: 16px;
                margin: 10px 10px 10px 0;
                transition: all 0.3s ease;
                text-decoration: none;
                display: inline-block;
            }
            .btn:hover { 
                background: #0056b3; 
                transform: translateY(-2px);
                box-shadow: 0 5px 15px rgba(0,0,0,0.2);
            }
            .btn-success { background: #28a745; }
            .btn-success:hover { background: #1e7e34; }
            .btn-warning { background: #ffc107; color: #212529; }
            .btn-warning:hover { background: #e0a800; }
            .btn-danger { background: #dc3545; }
            .btn-danger:hover { background: #c82333; }
            .schedule { 
                background: linear-gradient(135deg, #f8f9fa, #e9ecef); 
                padding: 25px; 
                border-radius: 10px; 
                margin: 20px 0; 
            }
            .schedule-item { 
                padding: 10px 0; 
                border-bottom: 1px solid #dee2e6; 
                font-size: 16px;
            }
            .refresh-btn { 
                background: #6c757d; 
                color: white; 
                padding: 10px 20px; 
                border: none; 
                border-radius: 5px; 
                cursor: pointer; 
                margin-top: 20px;
            }
            .refresh-btn:hover { background: #5a6268; }
            .loading {
                display: none;
                text-align: center;
                padding: 20px;
                color: #007bff;
            }
            .result {
                margin-top: 20px;
                padding: 15px;
                border-radius: 8px;
                display: none;
            }
            .result.success {
                background: #d4edda;
                border: 1px solid #c3e6cb;
                color: #155724;
            }
            .result.error {
                background: #f8d7da;
                border: 1px solid #f5c6cb;
                color: #721c24;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>🤖 Telegram Bot Control Panel</h1>
                <p>Управление автопостами и мониторинг работы бота</p>
            </div>
            
            <div class="status {{ 'running' if status.running else 'stopped' }}">
                <strong>Статус:</strong> {{ '🟢 Работает' if status.running else '🔴 Остановлен' }}
            </div>
            
            <div class="stats">
                <div class="stat-card">
                    <div class="stat-number">{{ status.total_published }}</div>
                    <div>📊 Опубликовано постов</div>
                </div>
                <div class="stat-card">
                    <div class="stat-number">{{ status.errors }}</div>
                    <div>❌ Ошибок</div>
                </div>
                <div class="stat-card">
                    <div class="stat-number">{{ channels_count }}</div>
                    <div>📢 Каналов</div>
                </div>
                <div class="stat-card">
                    <div class="stat-number">{{ schedule_count }}</div>
                    <div>⏰ Публикаций в день</div>
                </div>
            </div>
            
            <div class="controls">
                <h3>🎮 Управление</h3>
                <p>Запустите тестовую публикацию в любое время:</p>
                
                <button class="btn btn-success" onclick="testPublish('morning')">🌅 Утренний пост</button>
                <button class="btn btn-success" onclick="testPublish('noon')">☀️ Дневной пост</button>
                <button class="btn btn-success" onclick="testPublish('afternoon')">☕ Послеобеденный пост</button>
                <button class="btn btn-success" onclick="testPublish('evening')">🌆 Вечерний пост</button>
                
                <br><br>
                
                <button class="btn btn-warning" onclick="testCustomMessage()">📝 Пользовательский пост</button>
                <button class="btn" onclick="testAllTemplates()">🚀 Тест всех шаблонов</button>
                
                <div class="loading" id="loading">
                    <p>⏳ Отправка сообщений...</p>
                </div>
                
                <div class="result" id="result"></div>
            </div>
            
            <div class="schedule">
                <h3>📅 Расписание публикации</h3>
                {% for time in schedule_times %}
                <div class="schedule-item">🕐 {{ time }} МСК</div>
                {% endfor %}
            </div>
            
            <div style="background: #f8f9fa; padding: 20px; border-radius: 10px; margin: 20px 0;">
                <strong>📈 Последняя публикация:</strong> {{ status.last_publish or 'Нет данных' }}<br>
                <strong>🚀 Время запуска:</strong> {{ status.start_time or 'Нет данных' }}
            </div>
            
            <button class="refresh-btn" onclick="location.reload()">🔄 Обновить страницу</button>
        </div>
        
        <script>
            function showLoading() {
                document.getElementById('loading').style.display = 'block';
                document.getElementById('result').style.display = 'none';
            }
            
            function hideLoading() {
                document.getElementById('loading').style.display = 'none';
            }
            
            function showResult(message, isSuccess = true) {
                const result = document.getElementById('result');
                result.style.display = 'block';
                result.className = 'result ' + (isSuccess ? 'success' : 'error');
                result.innerHTML = message;
            }
            
            async function testPublish(template) {
                showLoading();
                try {
                    const response = await fetch('/api/test/' + template);
                    const data = await response.json();
                    hideLoading();
                    
                    if (data.success) {
                        const successful = data.successful || 0;
                        const total = data.total || 0;
                        showResult(`✅ Успешно отправлено в ${successful} из ${total} каналов`, true);
                    } else {
                        showResult('❌ Ошибка при отправке: ' + (data.error || 'Неизвестная ошибка'), false);
                    }
                } catch (error) {
                    hideLoading();
                    showResult('❌ Ошибка соединения: ' + error.message', false);
                }
            }
            
            async function testCustomMessage() {
                const message = prompt('Введите текст сообщения:', '🧪 Тестовое сообщение - ' + new Date().toLocaleTimeString());
                if (!message) return;
                
                showLoading();
                try {
                    const response = await fetch('/api/test/custom', {
                        method: 'POST',
                        headers: {'Content-Type': 'application/json'},
                        body: JSON.stringify({message: message})
                    });
                    const data = await response.json();
                    hideLoading();
                    
                    if (data.success) {
                        const successful = data.successful || 0;
                        const total = data.total || 0;
                        showResult(`✅ Сообщение "${message}" отправлено в ${successful} из ${total} каналов`, true);
                    } else {
                        showResult('❌ Ошибка при отправке: ' + (data.error || 'Неизвестная ошибка'), false);
                    }
                } catch (error) {
                    hideLoading();
                    showResult('❌ Ошибка соединения: ' + error.message, false);
                }
            }
            
            async function testAllTemplates() {
                showLoading();
                try {
                    const response = await fetch('/api/test/all');
                    const data = await response.json();
                    hideLoading();
                    
                    if (data.success) {
                        showResult(`✅ Все шаблоны протестированы. Успешно: ${data.successful}, Ошибок: ${data.failed}`, true);
                    } else {
                        showResult('❌ Ошибка при тестировании: ' + (data.error || 'Неизвестная ошибка'), false);
                    }
                } catch (error) {
                    hideLoading();
                    showResult('❌ Ошибка соединения: ' + error.message, false);
                }
            }
            
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

@app.route('/api/test/<template>')
def test_template(template):
    """API для тестирования конкретного шаблона"""
    async def test():
        init_bot()
        publisher = bot_status['publisher']
        
        # Маппинг шаблонов
        template_map = {
            'morning': '08:00',
            'noon': '12:00', 
            'afternoon': '16:00',
            'evening': '19:00'
        }
        
        time_key = template_map.get(template, '08:00')
        post_template = POST_TEMPLATES.get(time_key, {
            'text': f'🧪 Тестовое сообщение ({template})',
            'parse_mode': 'HTML'
        })
        
        message = post_template['text']
        parse_mode = post_template.get('parse_mode', 'HTML')
        
        results = await publisher.publish_to_all_channels(message, parse_mode)
        
        successful = sum(1 for success in results.values() if success)
        total = len(results)
        
        # Обновляем статистику
        bot_status['total_published'] += successful
        bot_status['last_publish'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        bot_status['errors'] += (total - successful)
        
        return {
            "success": True,
            "successful": successful,
            "total": total,
            "results": results
        }
    
    try:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        result = loop.run_until_complete(test())
        loop.close()
        return jsonify(result)
    except Exception as e:
        return jsonify({"success": False, "error": str(e)})

@app.route('/api/test/custom', methods=['POST'])
def test_custom():
    """API для тестирования пользовательского сообщения"""
    async def test():
        init_bot()
        publisher = bot_status['publisher']
        
        data = request.get_json()
        message = data.get('message', '🧪 Пользовательское сообщение')
        
        results = await publisher.publish_to_all_channels(message)
        
        successful = sum(1 for success in results.values() if success)
        total = len(results)
        
        # Обновляем статистику
        bot_status['total_published'] += successful
        bot_status['last_publish'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        bot_status['errors'] += (total - successful)
        
        return {
            "success": True,
            "successful": successful,
            "total": total,
            "results": results
        }
    
    try:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        result = loop.run_until_complete(test())
        loop.close()
        return jsonify(result)
    except Exception as e:
        return jsonify({"success": False, "error": str(e)})

@app.route('/api/test/all')
def test_all_templates():
    """API для тестирования всех шаблонов"""
    async def test():
        init_bot()
        publisher = bot_status['publisher']
        
        total_successful = 0
        total_failed = 0
        
        for time_key, template in POST_TEMPLATES.items():
            message = template['text']
            parse_mode = template.get('parse_mode', 'HTML')
            
            results = await publisher.publish_to_all_channels(message, parse_mode)
            
            successful = sum(1 for success in results.values() if success)
            failed = len(results) - successful
            
            total_successful += successful
            total_failed += failed
        
        # Обновляем статистику
        bot_status['total_published'] += total_successful
        bot_status['last_publish'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        bot_status['errors'] += total_failed
        
        return {
            "success": True,
            "successful": total_successful,
            "failed": total_failed
        }
    
    try:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        result = loop.run_until_complete(test())
        loop.close()
        return jsonify(result)
    except Exception as e:
        return jsonify({"success": False, "error": str(e)})

if __name__ == "__main__":
    print("🌐 Запуск веб-интерфейса для управления ботом...")
    print("📱 Откройте браузер и перейдите по адресу: http://localhost:5000")
    print("🎮 Теперь вы можете запускать автопосты в любое время!")
    
    app.run(host='0.0.0.0', port=5000, debug=True)


