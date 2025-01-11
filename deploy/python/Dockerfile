FROM registry.gitlab.com/unienv/images/python:3.11

ENV PYTHONUNBUFFERED 1
ARG SITE_ID
ENV SITE_ID $SITE_ID

WORKDIR /app

RUN git init

RUN curl -sSL https://install.python-poetry.org | python3 - --version 1.8.2
ENV PATH="/root/.local/bin:$PATH"
RUN poetry config virtualenvs.create false

COPY pyproject.toml .
COPY poetry.lock .
RUN poetry install
RUN poetry add uwsgi==2.0.25.1

COPY .. .

RUN pre-commit run -a && python manage.py collectstatic --noinput

ENV PORT 8000


CMD python manage.py migrate && uwsgi --ini deploy/python/uwsgi.ini --http-socket :$PORT --static-map /api/static=/app/static
