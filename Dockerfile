FROM python:3.11

# Устанавливаем переменные окружения
ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

# Устанавливаем рабочую директорию
WORKDIR /app

# Копируем файл требований и устанавливаем зависимости
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Копируем все файлы проекта в рабочую директорию
COPY . /app/

EXPOSE 5000

CMD ["python", "app.py"]

