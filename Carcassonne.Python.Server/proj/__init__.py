from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

app = FastAPI(title="Carcassonne", debug=True)

# serve your static files (adjust path if different)
app.mount("/static", StaticFiles(directory="proj/static"), name="static")

# import and include routers (they must expose `router`)
from .api import router
from . import views as views_module

app.include_router(router)          # api routes (e.g. /user/{userId})
app.include_router(views_module.router) # template/view routes (e.g. /signin)
