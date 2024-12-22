# Указываем базовый образ Python
FROM python:3.11

# Устанавливаем зависимости системы
RUN apt-get update && apt-get install -y \
    libpq-dev \
    && apt-get clean

# Создаем рабочую директорию
WORKDIR /app

# Копируем зависимости и устанавливаем их
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Копируем проект
COPY . .

# Собираем статику
RUN python manage.py collectstatic --noinput

# Запускаем сервер Gunicorn
CMD ["gunicorn", "freelance.wsgi:application", "--bind", "0.0.0.0:8000"]
