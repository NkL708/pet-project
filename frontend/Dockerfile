FROM node:20

RUN apt update && apt upgrade -y && \
    apt install zsh -y && \
    rm -rf /var/lib/apt/lists/*

RUN useradd -m nkl && \
    chsh -s /bin/zsh nkl

WORKDIR /home/nkl/frontend/
COPY package*.json yarn.lock angular.json tsconfig*.json ./
RUN yarn global add @angular/cli && \
    yarn install

RUN chown -R nkl:nkl /home/nkl/frontend
USER nkl

RUN zsh -c "$(wget -O- https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh)" && \
    git clone https://github.com/zsh-users/zsh-autosuggestions ${ZSH_CUSTOM:-~/.oh-my-zsh/custom}/plugins/zsh-autosuggestions && \
    sed -i "s/plugins=(git)/plugins=(git zsh-autosuggestions)/" ~/.zshrc

CMD zsh -c "ng serve --host 0.0.0.0 --poll=2000"
