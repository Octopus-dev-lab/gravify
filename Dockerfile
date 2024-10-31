FROM python:3.12.6

WORKDIR /app

RUN apt-get update && apt-get install -y \
    php \
    php-curl \
    php-zip

RUN curl -sSL https://install.python-poetry.org | python3 -

ENV PATH="/root/.local/bin:$PATH"

COPY pyproject.toml .

RUN poetry install

CMD [ "poetry", "run", "python", "src/main.py" ]