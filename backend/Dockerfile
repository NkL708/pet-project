FROM python:3.11 as base
ENV PYTHONDONTWRITEBYTECODE 1
ENV DJANGO_SETTINGS_MODULE=core.settings
WORKDIR /home/nkl/backend
COPY pyproject.toml poetry.lock manage.py ./
RUN pip install poetry && \
    poetry config virtualenvs.in-project true && \
    useradd -m nkl && \
    chown -R nkl:nkl /home/nkl

FROM base as dev
RUN poetry install --no-root
RUN apt update && apt upgrade -y && \
    apt install zsh -y && \
    chsh -s /bin/zsh nkl
USER nkl
RUN zsh -c "$(wget -O- https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh)" && \
    git clone https://github.com/zsh-users/zsh-autosuggestions ${ZSH_CUSTOM:-~/.oh-my-zsh/custom}/plugins/zsh-autosuggestions && \
    sed -i "s/plugins=(git)/plugins=(git zsh-autosuggestions)/" ~/.zshrc
CMD zsh -c "poetry run python manage.py migrate && \
    poetry run python manage.py runserver 0.0.0.0:8000"

FROM base as prod
RUN poetry install --no-dev --no-root
USER nkl
# Gunicorn и Nginx
