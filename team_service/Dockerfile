# Используем Python образ
FROM python:3.12-slim

# Устанавливаем рабочую директорию
WORKDIR /app

# Копируем файлы зависимостей
COPY requirements.txt requirements.txt

# Устанавливаем зависимости
RUN pip3 install --no-cache-dir -r requirements.txt

# Копируем исходный код
COPY . /app

# Настраиваем PYTHONPATH
ENV PYTHONPATH=/app

# Открываем порт для FastAPI
EXPOSE 8000

# Запускаем приложение
CMD ["gunicorn", "-k", "uvicorn.workers.UvicornWorker", "app.main:app", "--bind", "0.0.0.0:8000"]
