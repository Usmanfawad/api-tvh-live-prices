# tvh-api-live-prices

A FastAPI server that fetches live product prices from TVH.

- async funcs enabled
- MySQL, Access support

## Running the fastAPI server

Pip installation
```
pip install fastapi

███████████████████████████ 68%
```

```
pip install "uvicorn[standard]"

████████████████████████████████████████ 100%
```

Running the server: CD to the main directory and run the command

```
uvicorn App.main:app --reload --port 8000
```

