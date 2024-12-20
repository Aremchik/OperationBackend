# Используем Python образ
FROM python:3.12-slim

# Устанавливаем рабочую директорию
WORKDIR /app

# Копируем файлы зависимостей
COPY requirements.txt requirements.txt

# Устанавливаем зависимости
RUN apt-get update && apt-get install -y build-essential libffi-dev gcc

# Установка Python-зависимостей
RUN pip3 install --no-cache-dir -r requirements.txt --upgrade pip setuptools wheel
# Копируем исходный код
COPY . .

# Открываем порт для FastAPI
EXPOSE 8000

# Запускаем приложение
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
