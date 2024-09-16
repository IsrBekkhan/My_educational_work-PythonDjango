FROM python:3.11

# отключение буфферизации в python
ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY requirements.txt requirements.txt

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# примечание: копирование содержимого папки mysite, а не самой папки
COPY mysite .

#CMD ["python", "manage.py", "runserver"]