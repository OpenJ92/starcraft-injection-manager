FROM python:3.9-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    libpq-dev gcc && \
    rm -rf /var/lib/apt/lists/*

# Ensure the /submodules directory exists
RUN mkdir -p /submodules && chown -R root:root /submodules
RUN mkdir -p /external && chown -R root:root /external

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV DB_HOST=starcraft-db \
    DB_PORT=5432 \
    DB_USER=postgres \
    DB_PASSWORD=password \
    DB_NAME=starcraft_dev

CMD ["bash"]

