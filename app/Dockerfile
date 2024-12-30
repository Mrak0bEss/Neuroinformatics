FROM python:3.13-slim

# Установим рабочую директорию внутри контейнера
WORKDIR /app

# Скопируем файл зависимостей в контейнер
COPY requirements.txt ./

# Установим зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Скопируем все файлы приложения
COPY . .

EXPOSE 8000

CMD ["uvicorn", "main:app","--host","0.0.0.0","--port", "8000"]
