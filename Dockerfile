FROM python:3.10-slim

ARG USER_ID=1000
ARG USER_GID=1000
ARG USERNAME=cycle-calc

RUN apt-get update -y && \
  apt-get install python3-pip -y

WORKDIR /code

RUN groupadd --gid $USER_GID $USERNAME \
  && useradd --uid $USER_ID -g $USER_GID -m $USERNAME \
  && chown -R ${USER_ID}:${USER_GID} /code

# Install Poetry
# https://github.com/python-poetry/poetry/issues/6397#issuecomment-1236327500

ENV POETRY_HOME=/opt/poetry

# install poetry into its own venv
RUN python3 -m venv $POETRY_HOME && \
  $POETRY_HOME/bin/pip install poetry==1.7.1

ENV VIRTUAL_ENV=/poetry-env \
  PATH="/poetry-env/bin:$POETRY_HOME/bin:$PATH"

RUN python3 -m venv $VIRTUAL_ENV && \
  chown -R ${USER_ID}:${USER_GID} $POETRY_HOME /poetry-env

USER $USERNAME

COPY . .

RUN poetry install --with dev
