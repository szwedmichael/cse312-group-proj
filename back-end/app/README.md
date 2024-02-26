# Back-End

## Installation

### Pipenv

```bash
cd ./back-end
```

```bash
pipenv install
```

## Dev server

```bash
pipenv run uvicorn app.main:app --reload
```

## Example app structure

1. Install packages
2. Start the dev server
3. Visit http://127.0.0.1:8000/example
4. See the index.html served

- Main.py basically is all the setup before the app starts
- Routers/ has all of the top level routes we will declare
  - Depends means that it needs something else. In this case the service
- Services/ has all of the core logic. Any calculations or transformation
- Repos/ is any of the long ugly stuff. DB stuff, queries, long strings
