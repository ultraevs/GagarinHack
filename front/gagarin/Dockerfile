FROM node:18-alpine

WORKDIR /app

COPY . /app

RUN npm install

CMD ["npm", "run", "dev", "--", "--host", "0.0.0.0"]