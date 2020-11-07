## Dev
1. Install (docker-compose)[https://docs.docker.com/compose/install/].
2. Put `telegram.session` into the working directory.
3. export `TELEGRAM_API_ID`, `TELEGRAM_API_HASH`, 'SIMPLE_SETTINGS=settings.base`
4. `docker-compose -f compose.yml up`.

## How to login scrapper to Telegram
1. `pipenv install --dev`
2. `SIMPLE_SETTINGS=settings.base pipenv run src/telegram.py`