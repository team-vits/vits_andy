# very lightweight fast image
FROM python:3.9.6-alpine
LABEL maintainer="Andy Lopez"

# tells python that to unbuffer the output = faster response
ENV PYTHONUNBUFFERED 1
# Prevents Python from writing pyc files to disc (equivalent to python -B option)
ENV PYTHONDONTWRITEBYTECODE 1

# copy files to the docker image
COPY ./requirements.txt /tmp/requirements.txt
COPY ./requirements.dev.txt /tmp/requirements.dev.txt
COPY ./app /app
WORKDIR /app
EXPOSE 8000

ARG DEV=false
# avoid using root
# block cmd instead of running individual to avoid creating img layers
RUN python -m venv /py && \
    /py/bin/pip install --upgrade pip && \
    apk update && apk add mysql-client && \
    apk add gcc musl-dev mariadb-connector-c-dev && \
    /py/bin/pip install -r /tmp/requirements.txt && \
    if [ $DEV = "true" ]; \
        then /py/bin/pip install -r /tmp/requirements.dev.txt ; \
    fi && \
    rm -rf /tmp && \
    adduser \
        --disabled-password \
        --no-create-home \
        devuser

# run cmd from the venv
ENV PATH="/py/bin:$PATH"

USER devuser
