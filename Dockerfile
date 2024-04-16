FROM python:3.11.4

# ENV PYTHONUNBUFFERED 1

RUN mkdir -p /home/app

WORKDIR /home/app

COPY requirements.txt .

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

COPY . .

EXPOSE 5000

# CMD python manage.py makemigrations && python manage.py migrate && python manage.py runserver 0.0.0.0:8000
# CMD python manage.py runserver 0.0.0.0:8000

ENV FLASK_DEBUG: on
ENV FLASK_APP=./test.py
CMD ["flask", "--debug", "run", "--host", "0.0.0.0"]

