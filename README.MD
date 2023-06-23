# Для запуска проекта
- создать файл .env
- в него положить переменные:
    - ES_PORT - порт Elasticsearch
    - REDIS_PORT - порт Redis
- в терминале выполнить команду "docker-compose build"
- в терминале выполнить команду "docker-compose up"
- данные из дампа загружаются около 2-х минут
- данные из Faker (сгенерированные случайные данные) загружаются около 10 минут


# Для запуска тестов
- из папки .tests/functional запустить команду "docker-compose rm && docker-compose up --build"


# Ссылка для BlueDeep
https://github.com/maxjamchuk/Async_API_sprint_2
