FROM node:18-alpine

WORKDIR /app

COPY budget-tracker-vue/package*.json ./
RUN npm install

COPY budget-tracker-vue ./

RUN npm run build

RUN aws --endpoint-url=https://storage.yandexcloud.net s3 rm --recursive s3://frontend-budget-tracker
RUN aws --endpoint-url=https://storage.yandexcloud.net s3 cp --recursive build/ s3://frontend-budget-tracker/


RUN aws --endpoint-url=https://storage.yandexcloud.net s3 rm --recursive s3://media-budget-tracker
RUN aws --endpoint-url=https://storage.yandexcloud.net s3 cp --recursive build/ s3://media-budget-tracker/