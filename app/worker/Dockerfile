FROM python:3.12-slim

WORKDIR /app

RUN apt-get update && apt-get install -y curl

# Install Poetry to /opt/poetry and symlink it
RUN curl -sSL https://install.python-poetry.org | python3 - && \
    ln -s /root/.local/bin/poetry /usr/local/bin/poetry

RUN poetry self add poetry-plugin-export

RUN pip install -U pip

RUN poetry --version

COPY ./pyproject.toml ./app/worker/
RUN --mount=type=ssh poetry lock -C ./app/worker && \
    poetry export -C ./app/worker --without-hashes -o ./requirements.txt
RUN --mount=type=ssh pip install --no-cache-dir --no-warn-script -r ./app/worker/requirements.txt
