FROM python:latest

# Update dep
RUN apt update -y && \ 
    apt upgrade -y

# Pipenv
COPY Pipfile /home/backend/
WORKDIR /home/backend
RUN pip install --upgrade pip && \
    pip install pipenv && \
    pipenv install

CMD ["pipenv", "run", "python", "manage.py", "runserver", "0.0.0.0:8000"]
