FROM python:3.11-alpine as base
ENV PYTHONDONTWRITEBYTECODE 1
ENV DJANGO_SETTINGS_MODULE=core.settings
WORKDIR /home/nkl/backend
COPY pyproject.toml poetry.lock manage.py ./
RUN pip install poetry && \
    poetry config virtualenvs.in-project true && \
    addgroup -S nkl && adduser -S nkl -G nkl && \
    chown -R nkl:nkl /home/nkl

FROM base as dev
RUN poetry install --no-root && \
    apk update && apk upgrade && \
    apk add zsh git && \
    sed -i 's/ash/zsh/' /etc/passwd
USER nkl
RUN zsh -c "$(wget https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh -O -)" && \
    git clone https://github.com/zsh-users/zsh-autosuggestions ${ZSH_CUSTOM:-~/.oh-my-zsh/custom}/plugins/zsh-autosuggestions && \
    sed -i "s/plugins=(git)/plugins=(git zsh-autosuggestions)/" ~/.config/zsh/.zshrc
EXPOSE 8000
CMD zsh -c "poetry run python manage.py migrate && \
    poetry run python manage.py runserver 0.0.0.0:8000"

FROM base as prod
ARG DJANGO_SECRET_KEY
RUN poetry install --no-dev --no-root
COPY --chown=nkl:nkl . .
USER nkl
RUN poetry run python manage.py collectstatic --noinput
EXPOSE 8000
CMD ["poetry", "run", "gunicorn", "core.wsgi:application", "--bind", "0.0.0.0:8000"]
