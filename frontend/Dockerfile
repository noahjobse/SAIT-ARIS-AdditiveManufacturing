FROM node:20-slim

WORKDIR /app

# Install dependencies
COPY package.json package-lock.json ./
RUN npm install

# Copy source
COPY . .

EXPOSE 3000

# Run Next.js dev server
CMD ["npm", "run", "dev", "--", "-H", "0.0.0.0", "-p", "3000"]
