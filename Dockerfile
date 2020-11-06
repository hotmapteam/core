FROM python:alpine
RUN mkdir /app
WORKDIR /app
RUN python3 -m pip install pipenv
ADD Pipfile .
ADD Pipfile.lock .
RUN pipenv install --deploy
ADD src/ .
