FROM python:latest

# Update dep
RUN apt update -y && \ 
    apt upgrade -y

# Additional packages
RUN apt install vim -y

# Pipenv
COPY Pipfile /home/backend/
RUN pip install --upgrade pip && \
    pip install pipenv && \
    pipenv install

# Start server
WORKDIR /home/backend
CMD ["pipenv", "run", "python", "manage.py", "runserver", "0.0.0.0:8000"]
