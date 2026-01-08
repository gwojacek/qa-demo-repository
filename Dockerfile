# Dockerfile
FROM python:3.12-slim

# 1. System deps
RUN apt-get update && apt-get install -y \
    curl git \
    && apt-get clean

# 2. Install Poetry
RUN pip install poetry

# 3. Tell Poetry *not* to create venvs
RUN poetry config virtualenvs.create false

# 4. Copy manifest & install deps
WORKDIR /app
COPY pyproject.toml poetry.lock ./
RUN poetry install --no-root --no-interaction
RUN playwright install --with-deps

# 5. Copy your code in
COPY . .

# 6. Default to pytest (so `docker compose run` just adds flags)
ENTRYPOINT ["pytest"]
