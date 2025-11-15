FROM python:3.11-slim

WORKDIR /app

ENV POETRY_VIRTUALENVS_IN_PROJECT=true
RUN pip install poetry

COPY ./entrypoint.sh /usr/local/bin/entrypoint.sh
RUN chmod +x /usr/local/bin/entrypoint.sh

ENTRYPOINT ["entrypoint.sh"]

COPY poetry.lock pyproject.toml ./

CMD ["poetry", "run", "python", "-m", "src.main"]
