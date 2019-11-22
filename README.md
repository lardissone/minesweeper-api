# Minesweeper API

API for Minesweeper game.

## Links

- **API**: [https://lardissone-minesweeper-api.herokuapp.com/api/](https://lardissone-minesweeper-api.herokuapp.com/api/)
- **Front End**: [Demo](https://minesweeper-web.lardissone.now.sh/) - [Source](https://github.com/lardissone/minesweeper-web)
- **API Documentation (Swagger)**: [https://lardissone-minesweeper-api.herokuapp.com/api/docs/](https://lardissone-minesweeper-api.herokuapp.com/api/docs/)
- **API Documentation (ReDoc)**: [https://lardissone-minesweeper-api.herokuapp.com/api/docs/redoc](https://lardissone-minesweeper-api.herokuapp.com/api/docs/redoc)

## Decisions

- Used Django and Django REST Framework because I prefer not to DRY (specially on authentication and user sessions)
- Used JWT for authentication

## Running locally

### Requirements

- Python 3.x
- Pipenv

### Running

```python
pipenv install
pipenv run python minesweeper/manage.py migrate
pipenv run python minesweeper/manage.py runserver
```

## Missing

- Add tests
- Add pause/resume feature
- Add some kind of captcha to avoid massive registrations
- Allow editing of games (update and delete)