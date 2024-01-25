FROM node:20-alpine as build
WORKDIR /home/nkl/frontend/
RUN addgroup -S nkl && adduser -S nkl -G nkl && \
    chown -R nkl:nkl /home/nkl
USER nkl
COPY package*.json yarn.lock angular.json tsconfig*.json ./
RUN yarn install
COPY --chown=nkl:nkl src ./src
RUN yarn ng build

FROM build as dev
USER root
RUN apk update && apk upgrade && \
    apk add zsh git && \
    sed -i 's/ash/zsh/' /etc/passwd
USER nkl
RUN zsh -c "$(wget https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh -O -)" && \
    git clone https://github.com/zsh-users/zsh-autosuggestions ${ZSH_CUSTOM:-~/.oh-my-zsh/custom}/plugins/zsh-autosuggestions && \
    sed -i "s/plugins=(git)/plugins=(git zsh-autosuggestions)/" ~/.config/zsh/.zshrc
EXPOSE 4200
CMD ["yarn", "ng", "serve", "--host", "0.0.0.0", "--poll=2000"]
