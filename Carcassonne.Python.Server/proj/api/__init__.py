from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pathlib import Path


# Resolve directories: prefer `proj/web` (same level as `proj/api`); fall back to repo-level `templates`/`static`.
API_DIR = Path(__file__).resolve().parent

PROJ_DIR = API_DIR.parent
DIST = PROJ_DIR / "web/dist"



WEB_DIR = PROJ_DIR / "web/dist"
TEMPLATES_DIR = PROJ_DIR / "web/dist"

app = FastAPI(title="Carcassonne", debug=True)


app.mount("/js", StaticFiles(directory=str(WEB_DIR / "js")), name="js")
app.mount("/css", StaticFiles(directory=str(WEB_DIR / "css")), name="css")
app.mount("/img", StaticFiles(directory=str(WEB_DIR / "img")), name="img")
app.mount("/partial", StaticFiles(directory=str(WEB_DIR / "partial")), name="partial")
app.mount("/views", StaticFiles(directory=str(WEB_DIR / "views")), name="views")
app.mount("/i18n", StaticFiles(directory=str(WEB_DIR / "i18n")), name="i18n")
		
templates = Jinja2Templates(directory=str(DIST))

from .routes import router

@app.get("/", response_class=HTMLResponse)
def index(request: Request):
	return templates.TemplateResponse("index.html", {"request": request})

app.include_router(router)
