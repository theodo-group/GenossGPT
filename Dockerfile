# Docker multi-stage building, as recommended by https://fastapi.tiangolo.com/deployment/docker/#docker-image-with-poetry
FROM python:3.11.3-slim-buster as curl-stage

# Install curl ; remove apt cache to reduce image size
# TODO: check if liblzma-dev is necessary
RUN apt-get -y update && apt-get -y install curl liblzma-dev && rm -rf /var/lib/apt/lists/*
RUN pip install --upgrade pip

FROM curl-stage as poetry-requirements-stage

ARG poetry_groups=main,llms

WORKDIR /tmp

ENV HOME /root
ENV PATH=${PATH}:$HOME/.local/bin

# Install poetry
RUN curl -sSL https://install.python-poetry.org | POETRY_VERSION=1.5.1 python3 -

# Export requirements.txt
COPY ./pyproject.toml ./poetry.lock* /tmp/
RUN poetry export -f requirements.txt --output requirements.txt --without-hashes --no-interaction --no-cache --only=${poetry_groups}


FROM curl-stage
WORKDIR /app

ENV \
    # Prevent Python from buffering stdout and stderr and loosing some logs (equivalent to python -u option)
    PYTHONUNBUFFERED=1 \
    # Prevent Pip from timing out when installing heavy dependencies
    PIP_DEFAULT_TIMEOUT=600 \
    # Prevent Pip from creating a cache directory to reduce image size
    PIP_NO_CACHE_DIR=1

ENV UVICORN_HOST="0.0.0.0" \
    UVICORN_PORT=4321

# Install dependencies with pip from exported requirements.txt
COPY --from=poetry-requirements-stage /tmp/requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt

# Copy API files
COPY . /app

# Add and set a non-root user
RUN useradd appuser
USER appuser

# Start FastAPI
CMD ["uvicorn", "main:app"]

# Healthcheck
HEALTHCHECK --interval=10s --timeout=1s --retries=3 CMD curl --fail http://localhost:${PORT}/ || exit 1
