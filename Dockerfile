FROM python:3.13-slim

RUN pip install poetry

COPY . .

RUN poetry install --no-root

ENV APP_HOST="0.0.0.0"

EXPOSE 8000

ENTRYPOINT ["poetry", "run", "python", "-m", "main"]