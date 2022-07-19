# Torrent Scrapper
## Running the app in the development mode

Run the following command to launch the project in dev mode 

```bash
  uvicorn app.main:app --proxy-headers --host 0.0.0.0 --port 8000 --http h11 --use-colors --log-level debug --access-log  --reload
```

## Docker for development

Run the following command to launch the project inside a docker container

```bash
  docker-compose -f docker-compose.dev.yml up
```

## Docker for Production

Run the following command build & run a distroless docker container for production

```bash
  docker-compose up
```
