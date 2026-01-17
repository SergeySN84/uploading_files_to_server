# Приложение для загрузки файлов на сервер


Проект создан для интеграции в сервисы, в которые нужно загружать какой-либо контент на сервер разработчика проекта.
В проекте реализованы тесты для backend (Django/DRF) и frontend (Selenium WebDriver) с использованием Poetry и Docker.

---

## 🛠️ Технологии

- Python 3.10+
- Django + DRF
- pytest + pytest-django
- Selenium WebDriver (Python)
- Poetry (менеджер зависимостей)
- Docker & Docker Compose

---

# Установка

## 1. Клонировать репозиторий
```bash
git clone https://github.com/SergeySN84/uploading_files_to_server.git /home/test/uploading-files-to-server
cd /home/test/uploading-files-to-server
```
## 2. Создайте и настройте .env
poetry install

## 3. Активировать окружение
poetry shell

## 4. Создать .env (пример ниже)
cp .env.example .env

## 5. Применить миграции
python manage.py migrate

## 6. Запустить сервер
python manage.py runserver

# Деплой на удалённый сервер

## Требования к серверу:
- Ubuntu 22.04+ 
- Публичный IP: 84.252.141.96
- Открытые порты: 22 (SSH), 80 (HTTP)

## Шаги настройки сервера:

## 1. Подключитесь по SSH
```bash
ssh test@84.252.141.96 или ssh -i ~/.ssh/github_actions test@84.252.141.96
```
## 2. Установите Docker и Docker Compose
```bash
sudo apt update
sudo apt install -y docker.io docker-compose
sudo usermod -aG docker test
```

## 3. Создайте рабочую директорию
```bash
mkdir -p ~/home/test/uploading-files-to-server
cd ~/home/test/uploading-files-to-server
```

## 4. Клонируйте проект
```bash
git clone https://github.com/SergeySN84/uploading_files_to_server.git /home/test/uploading-files-to-server
```

## 5. Создайте .env. вручную
```bash
nano .env

SECRET_KEY=
DEBUG=
ALLOWED_HOSTS=

DB_NAME=b
DB_USER=
DB_PASSWORD=
DB_HOST=
DB_PORT=

REDIS_URL=
```

## 6. Запустите сервисы
```bash
docker-compose -f docker-compose.prod.yml up -d --build
```

# CI/CD через GitHub Actions

## 1. При пуше в ветку feature/diplom или develop запускается workflow.
## 2. Выполняются:
- Линтинг (flake8)
- Тесты (pytest) с покрытием ≥80%
- Сборка Docker-образов

## 3. При успехе — код обновляется на сервере, контейнеры перезапускаются.

# Настройка секретов в GitHub

```bash
SERVER_IP - 84.252.141.96
SSH_KEY - содержимое приватного ключа
DEPLOY_DIR - /home/test/uploading-files-to-server
DJANGO_SECRET_KEY - сгенерированный ключ для тестов
```

# После деплоя откройте:
```bash
API: http://84.252.141.96/api/
Swagger UI: http://84.252.141.96/schema/swagger-ui/
```
Если видите ошибку 502 Bad Gateway:

Проверьте, что .env.prod содержит ALLOWED_HOSTS=84.252.141.96
Убедитесь, что контейнеры запущены: docker-compose -f docker-compose.prod.yml ps