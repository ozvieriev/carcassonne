from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

app = FastAPI(title="Carcassonne", debug=True)

# import and include routers (they must expose `router`)
from .routes import router

app.include_router(router)          # api routes (e.g. /user/{userId})
