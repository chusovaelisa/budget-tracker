FROM node:18-alpine AS build

WORKDIR /app

COPY budget-tracker-vue/package*.json ./

RUN npm install

COPY budget-tracker-vue ./

RUN npm run build

FROM nginx:alpine

COPY --from=build /app/dist /usr/share/nginx/html

# Копируем кастомный конфиг для Nginx, если он есть
# COPY nginx.conf /etc/nginx/nginx.conf

EXPOSE 80

# Запускаем Nginx
CMD ["nginx", "-g", "daemon off;"]