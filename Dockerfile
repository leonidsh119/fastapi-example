FROM python:3.13-slim

RUN pip install poetry

COPY . .

RUN poetry install --no-root

EXPOSE 8000

ENTRYPOINT ["poetry", "run", "python", "-m", "main"]