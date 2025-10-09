# django-todo
A test bot with a django admin panel | ChatLabs.ru

В гите есть файл .env.example, необхдимо добавить env.dev или env.prod и исправить данные на верные значения для запуска апки

Запуск апки (prod):
ENV=prod docker compose --env-file .env.prod up # можно добавить --build если необходима пересборка
