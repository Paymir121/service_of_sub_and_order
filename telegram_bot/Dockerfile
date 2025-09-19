FROM python:3.9

RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /telegram_bot

COPY requirements.txt .
RUN pip install -r requirements.txt --no-cache-dir
EXPOSE 8080

COPY . .
ENTRYPOINT ["sh", "entrypoint.sh"]