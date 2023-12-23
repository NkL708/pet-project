FROM python:3.11

ENV PYTHONDONTWRITEBYTECODE 1
ENV DJANGO_SETTINGS_MODULE=core.settings

RUN apt update && apt upgrade -y && \
    apt install zsh -y && \
    rm -rf /var/lib/apt/lists/*

RUN useradd -m nkl
RUN chsh -s /bin/zsh nkl

WORKDIR /home/nkl/backend
COPY pyproject.toml poetry.lock manage.py ./
RUN chown -R nkl:nkl /home/nkl/backend

USER nkl

RUN zsh -c "$(wget -O- https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh)" && \
    git clone https://github.com/zsh-users/zsh-autosuggestions ${ZSH_CUSTOM:-~/.oh-my-zsh/custom}/plugins/zsh-autosuggestions && \
    sed -i "s/plugins=(git)/plugins=(git zsh-autosuggestions)/" ~/.zshrc

ENV PATH="/home/nkl/.local/bin:$PATH"
RUN pip install poetry && \
    poetry config virtualenvs.in-project true && \
    poetry install --no-root

CMD zsh -c "poetry run python manage.py migrate && \
    poetry run python manage.py runserver 0.0.0.0:8000"
