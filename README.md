# invites_app
поднимаем docker-compose up -d --build

накатываем миграции docker-compose exec invites_app alembic upgrade head

В репе есть post коллекция с основными запросами + запрос для создания тестового пользователя и приглащения.
