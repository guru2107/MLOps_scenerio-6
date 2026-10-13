# Scenario 6 - Flask prediction app with Docker Compose

This scenario runs the prediction web application and the database API as
separate Compose services:

- `webapp` serves the prediction UI on port 5000.
- `dbapp` stores prediction history in SQLite. It is reachable by `webapp`
  over the internal Compose network and is not exposed directly to the host.
- `sqlite_data` is mounted into `dbapp` so records persist when containers are
  recreated.

## Run with Docker Compose

From this directory, build and start both services:

```powershell
docker compose up --build
```

Open http://localhost:5000, then use the **Records** page to view saved
predictions. Stop the services with `Ctrl+C`, or run:

```powershell
docker compose down
```

The SQLite database remains in `sqlite_data/app.db`. To remove the containers
and the persisted database, delete that file separately.

## Run in the background

```powershell
docker compose up --build -d
docker compose ps
docker compose logs -f
```

## Retrain the model

`train_model.py` can be used to retrain
`webapp/models/gaussian_nb_model.pkl` from `data/Iris (1).csv`.
