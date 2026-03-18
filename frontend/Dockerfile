FROM node:20-slim

RUN npm install -g pnpm

WORKDIR /app

# Install dependencies
COPY package.json pnpm-lock.yaml ./
RUN pnpm install --frozen-lockfile

# Copy source
COPY . .

EXPOSE 3000

# Run Next.js dev server
CMD ["pnpm", "dev", "-H", "0.0.0.0", "-p", "3000"]
