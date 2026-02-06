from fastapi import FastAPI, Request

app = FastAPI(title="Carcassonne", debug=True)
from .routes import router

app.include_router(router)          # api routes (e.g. /user/{userId})
