FROM python:3.11

ENV PYTHONDONTWRITEBYTECODE 1
ENV DJANGO_SETTINGS_MODULE=core.settings

# Update dependencies
RUN apt update -y && \ 
    apt upgrade -y

# Pipenv
WORKDIR /home/backend
COPY Pipfile manage.py ./
RUN pip install --upgrade pip && \
    pip install pipenv && \
    pipenv install

CMD sh -c "pipenv run python manage.py migrate && \ 
    pipenv run python manage.py runserver 0.0.0.0:8000"