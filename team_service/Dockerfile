FROM python:3.12-slim

WORKDIR /app

# Установка необходимых зависимостей
RUN apt-get update && apt-get install -y \
    build-essential \
    libffi-dev \
    libssl-dev \
    gcc \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Копируем зависимости и устанавливаем их
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Копируем приложение
COPY . .

# Открываем порт
EXPOSE 8000

# Запуск приложения
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
