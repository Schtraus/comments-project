FROM node:16

WORKDIR /app

COPY package*.json /app/

RUN npm install

COPY . /app/

CMD ["npm", "run", "serve"]
