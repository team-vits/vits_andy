# very lightweight fast image
FROM python:3.9-alpine3.13
LABEL maintainer="Andy Lopez"

# tells python that to unbuffer the output = faster response
ENV PYTHONUNBUFFERED 1

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
    /py/bin/pip install -r /tmp/requirements.txt && \
    if [ $DEV = "true" ]; \
        then /py/bin/pip install -r /tmp/requirements.dev.txt ; \
    fi && \
    rm -rf /tmp && \
    adduser \
        --disabled-password \
        --no-create-home \
        django-user

# run cmd from the venv
ENV PATH="/py/bin:$PATH"

USER django-user
