FROM node:20-alpine

WORKDIR /app

COPY package*.json ./

RUN npm ci

COPY . .

EXPOSE 5173

# Запускаем Vite с флагом --host, чтобы он слушал внешние запросы в докере
CMD ["npm", "run", "dev", "--", "--host", "0.0.0.0"]