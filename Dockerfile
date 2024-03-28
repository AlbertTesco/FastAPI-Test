#FROM python:3.11-slim
#
#COPY . .
#
#RUN pip install -r requirements.txt
#
#CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]
# Используем официальный образ Python, который поддерживает работу с asyncio и Python 3.11
FROM python:3.11-slim

# Устанавливаем рабочую директорию внутри контейнера
WORKDIR /app

# Копируем файлы requirements.txt и все проектные файлы внутрь контейнера
COPY . /app/

# Устанавливаем зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Запускаем приложение
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]