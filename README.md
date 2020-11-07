## Dev
### docker-compose
1. Install [docker-compose](https://docs.docker.com/compose/install/).
2. Put `telegram.session` into the working directory.
3. export `TELEGRAM_API_ID`, `TELEGRAM_API_HASH`, 'SIMPLE_SETTINGS=settings.base`
4. `docker-compose -f compose.yml up`.

### Localhost
```sh
export SIMPLE_SETTINGS=settings.base
# Run mongodb inside a docker container
docker run -v "$(pwd)/.db:/data/db" -p 27017:27017 mongo
# Or install and run systemd-wide, checkout documentation for your distribution how to install mongo
sudo apt install mongodb && sudo systemctl enable --now mongod

pipenv run python src/articlectl.py --add-feed "telegram,telegram channel 1,-10000000"
pipenv run python src/articlectl.py --fetch
pipenv run python src/api.py
```

## How to login scrapper to Telegram
`pipenv run src/telegram.py`

## List telegram dialogs
`pipenv src/telegram.py --list-dialogs`.
