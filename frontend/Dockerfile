FROM node:20 as base
WORKDIR /home/nkl/frontend/
COPY package*.json yarn.lock angular.json tsconfig*.json ./
RUN yarn global add @angular/cli && \
    yarn install && \
    useradd -m nkl && \
    chown -R nkl:nkl /home/nkl

FROM base as ci
USER nkl
CMD sh -c "tail -f /dev/null"

FROM base as dev
RUN apt update && apt upgrade -y && \
    apt install zsh -y && \
    chsh -s /bin/zsh nkl
USER nkl
RUN zsh -c "$(wget -O- https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh)" && \
    git clone https://github.com/zsh-users/zsh-autosuggestions ${ZSH_CUSTOM:-~/.oh-my-zsh/custom}/plugins/zsh-autosuggestions && \
    sed -i "s/plugins=(git)/plugins=(git zsh-autosuggestions)/" ~/.zshrc
CMD zsh -c "ng serve --host 0.0.0.0 --poll=2000"

FROM base as prod
# Nginx
