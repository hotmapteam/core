FROM debian:bullseye
RUN mkdir /app
WORKDIR /app
RUN DEBIAN_FRONTEND=noninteractive
RUN apt update -yq && apt install -yq gcc python3.9 python3.9-dev pipenv && rm -rf /var/lib/apt/lists/*
ADD Pipfile .
ADD Pipfile.lock .
RUN pipenv install --system --deploy
ADD src/ .
