FROM python:3.12-slim
ENV POETRY_VIRTUALENVS_CREATE=false

WORKDIR /app
COPY pyproject.toml poetry.lock /app

RUN pip install poetry

RUN poetry config installer.max-workers 10
RUN poetry install --no-interaction --no-ansi --only main

COPY . /app

EXPOSE 8000
CMD ["poetry", "run", "uvicorn", "--host", "0.0.0.0", "--port", "8000", "madr.app:app"]