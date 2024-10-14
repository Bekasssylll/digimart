
FROM python:3.10-slim

WORKDIR /code

COPY requirements.txt /code/

RUN pip install --no-cache-dir -r requirements.txt

COPY . /code/

# Выполним миграции и запустим сервер
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
