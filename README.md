# MLOps Домашнее задание №3

**Автор:** Мартиросова Анастасия Гургеновна
**Модуль:** "Модуль 3: Настройка стратегий развертывания модели"

## 1. Цель задания

Реализация стратегии Blue-Green развертывания для ML-модели с автоматизацией через CI/CD (GitHub Actions). Проект включает:

- REST API на FastAPI с эндпоинтами `/health` и `/predict`
- Контейнеризацию с Docker
- Blue-Green deployment стратегию
- CI/CD pipeline с GitHub Actions
- Автоматическое тестирование и деплой

## 2. Как запустить проект

### Шаг 1: Клонировать репозиторий

```bash
git clone <repository-url>
cd mlops_hw3_Martirosova_Anastasia
```

### Шаг 2: Настроить окружение

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Шаг 3: Обучить модели

```bash
python train_model.py
```

Создаст:
- `models/model_v1.0.0.pkl` - модель для Blue версии
- `models/model_v1.1.0.pkl` - модель для Green версии

### Шаг 4: Запустить локально (опция 1 - FastAPI)

```bash
MODEL_VERSION=v1.0.0 uvicorn main:app --host 0.0.0.0 --port 8080
```

Проверка:
```bash
curl http://localhost:8080/health
curl -X POST http://localhost:8080/predict -H "Content-Type: application/json" -d '{"features": [1.0, 2.0, 3.0]}'
```

### Шаг 5: Запустить через Docker Compose (опция 2 - Blue-Green)

```bash
docker-compose up -d --build
```

Проверка:
```bash
curl http://localhost/health
curl -X POST http://localhost/predict -H "Content-Type: application/json" -d '{"features": [1.0, 2.0, 3.0]}'
```

## 3. Структура проекта

### API сервис
**Файл:** `main.py`
- `/health` - возвращает статус и версию модели
- `/predict` - выполняет предсказание
- Версия модели через переменную `MODEL_VERSION`

### Обучение моделей
**Файл:** `train_model.py`
- Создает две версии модели (LinearRegression)
- Сохраняет как `model_v1.0.0.pkl` и `model_v1.1.0.pkl`

### Docker развертывание
**Файл:** `docker-compose.yml`
- Blue service (v1.0.0) на порту 8081
- Green service (v1.1.0) на порту 8082
- Nginx балансировщик на порту 80

### Переключение версий

```bash
# Переключить на Green версию
./switch-version.sh green

# Вернуться на Blue версию
./switch-version.sh blue
```

## 4. CI/CD Pipeline

### Настройка GitHub Secrets

Перед запуском workflow настройте секреты:

1. Откройте репозиторий на GitHub
2. Settings → Secrets and variables → Actions
3. New repository secret
4. Добавьте:
   - `CLOUD_TOKEN` - токен облачного провайдера (например: `demo-token-12345`)
   - `MODEL_VERSION` - версия для деплоя (например: `v1.0.0`)

### Workflow

GitHub Actions автоматически выполняет:

1. **build-and-test**
   - Обучение моделей
   - Валидация моделей
   - Тестирование API endpoints

2. **build-docker**
   - Сборка Docker образов для обеих версий
   - Публикация в GitHub Container Registry
   - Тестирование контейнеров

3. **deploy** (симуляция)
   - Загрузка secrets (CLOUD_TOKEN, MODEL_VERSION)
   - Имитация деплоя в облако
   - Проверка health и predict endpoints
   - Отображение deployment summary

Просмотр результатов: **GitHub → Actions → Model Deployment**

## 5. Blue-Green Deployment

**Blue (v1.0.0)** - стабильная версия
**Green (v1.1.0)** - новая версия

Преимущества:
- Мгновенное переключение
- Простой откат
- Нулевой downtime
- Тестирование перед переключением

## 6. Остановка сервисов

```bash
docker-compose down
```
