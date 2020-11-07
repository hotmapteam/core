FROM python
RUN mkdir /app
WORKDIR /app
RUN DEBIAN_FRONTEND=noninteractive
RUN apt update -yq && apt install -yq gcc python3-dev && rm -rf /var/lib/apt/lists/*
RUN python3 -m pip install pipenv
ADD Pipfile .
ADD Pipfile.lock .
RUN pipenv install --deploy
ADD src/ .
