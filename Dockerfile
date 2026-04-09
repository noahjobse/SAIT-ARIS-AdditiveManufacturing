FROM python:3.12-slim

# Install Node.js 20 + pnpm + build tools for PyBullet
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc g++ curl \
    && curl -fsSL https://deb.nodesource.com/setup_20.x | bash - \
    && apt-get install -y nodejs \
    && npm install -g pnpm \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Install Python dependencies
COPY backend/requirements.txt ./backend/
RUN pip install --no-cache-dir -r backend/requirements.txt

# Install Node dependencies
COPY frontend/package.json frontend/pnpm-lock.yaml ./frontend/
RUN cd frontend && pnpm install --frozen-lockfile

# Copy rest of project
COPY . .

EXPOSE 8000 3000

CMD ["sh", "start.sh"]
