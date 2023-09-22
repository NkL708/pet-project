FROM node:latest

WORKDIR /home/frontend/
COPY package*.json angular.json tsconfig*.json ./
RUN npm install -g @angular/cli && \
    npm install

CMD sh -c "ng serve --host 0.0.0.0"