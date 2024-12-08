# Веб-фреймворк "DIDPY"
Веб-фреймворк, написанный на хакатоне от VK education 08.12.2024

## Документация
Фреймворк "DIDPY" разработан для простоты и модульности, 
используя WebOb и Gunicorn для обработки HTTP-запросов и ответов.

### Обзор
Этот веб-фреймворк позволяет создавать веб-приложения, ориентируясь на простоту и модульность. Он включает:

- Класс сервера для запуска приложения с использованием Gunicorn.
- Систему маршрутизации для обработки HTTP-методов и путей.
- Поддержку пользовательских мидлваров.
- Шаблонную систему на основе Jinja2.
- Утилиты для работы с JSON и HTML ответами.

### Роутер (router.py)
Класс Router управляет маршрутизацией HTTP-запросов.

Создание роутера:
```python
router = web.Router()
```

Прикрепление эндпойнта к роутеру:
```python
@router.get('/hello')
def get_example(_request):
    return web.responses.JsonResponse({'message': 'hello, world!'})
```

Роутер может обрабатывать следующие http-методы:
- get
- post
- put
- patch
- delete

Декораторы методов принимают на вход путь до эндпойнта, 
а так же опционально могут принимать middleware.
```python
@router.get('/hello', middlewares=[ExampleMiddleware])
def get_example(_request):
    return web.responses.JsonResponse({'message': 'hello, world!'})
```
Более подробно про middleware будет рассказано дальше.

### Создание собственного обработчика для страницы 404

Фреймворк предоставляет обработчик для несуществующих страниц, однако вы можете переопределить его самостоятельно.
```python
@router.not_found
def custom_404(_request):
    return web.responses.JsonResponse({'error': 'route not found'})
```

### Возможные ответы (responses.py):
Обработчики принимают на вход запрос request и ответ response.

Фреймворк предоставляет возможность отдавать ответ в формате JSON и HTML,
для этого воспользуйтесь соответсвующими классами ответов.

```python
"""JSON"""
@router.get('/hello', middlewares=[ExampleMiddleware])
def get_example(request):
    logger.info(f'got {request=}')
    return web.responses.JsonResponse({'message': 'hello, world!'})
```
```python
"""HTML"""
@router.get('/main')
def html_example(_request):
    response = web.responses.HTMLResponse(
        template_path='templates/index.html',
        context={'today_date': datetime.date.today()}
    )
    return response
```

Вы можете создавать свои классы ответов, для этого унаследуйтесь от класса Response,
который определен в router.py


### Сервер (server.py)
Для запуска сервера необходимо воспользоваться классом Server из server.py
```python
server = web.Server(router, config)
```

Сервер принимает роутер, который мы создали ранее, а также словарь с конфигурацией. 
Этот словар может выглядеть следующим образом:
```python
HOST = os.getenv('HOST', default='0.0.0.0')
PORT = os.getenv('PORT', default='8080')
WORKERS_COUNT = os.getenv('WORKERS_COUNT', default=os.cpu_count())
LOG_LEVEL = os.getenv('LOG_LEVEL', default='info')


def get_config() -> dict:
    config = {
        'bind': f'{HOST}:{PORT}',
        'workers': WORKERS_COUNT,
        'loglevel': LOG_LEVEL,
    }
    return config
 
config = get_config()
```

Для запуска сервера воспользуйтесь методом run:
```python
server.run()
```



## Результаты нагрузочного тестирования
1. **Total Requests per Second** (Общее количество запросов в секунду)
Зелёная линия (RPS):
Частота запросов растёт до определённого уровня (около 800 запросов в секунду) и демонстрирует колебания. Это указывает на то, что приложение справляется с нагрузкой до определённого момента, но периодические снижения RPS могут свидетельствовать о перегрузке.
Красная линия (Failures/s):
Число отказов остаётся низким, что говорит о стабильной обработке запросов, хотя могут быть случаи перегрузки.
2. **Response Times** (Время ответа)
95th percentile (Фиолетовая линия):
Время ответа иногда подскакивает до 10–15 секунд. Это означает, что в пиковых нагрузках некоторые запросы обрабатываются значительно дольше.
50th percentile (Оранжевая линия):
Среднее время ответа остаётся стабильным, что говорит о том, что большинство запросов обрабатываются в разумные сроки. Однако заметны небольшие всплески, которые могут быть связаны с увеличением нагрузки.
3. **Number of Users** (Количество пользователей)
Количество виртуальных пользователей постепенно увеличивается до 1200, что соответствует росту нагрузки. Приложение в основном справляется с запросами, однако увеличение задержек и нестабильность RPS при максимальной нагрузке указывают на потенциальные узкие места. 
