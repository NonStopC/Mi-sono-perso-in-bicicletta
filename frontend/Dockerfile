FROM node:22-alpine

WORKDIR /app

# Copia package.json e installa dipendenze
COPY package*.json ./
RUN npm install

# Copia il codice
COPY . .

# Esponi porta Vite
EXPOSE 5173

# Comando per development con hot reload
CMD ["npm", "run", "dev", "--", "--host"]
