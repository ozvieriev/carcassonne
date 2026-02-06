from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pathlib import Path


# Resolve directories: prefer `proj/ui` (same level as `proj/api`); fall back to repo-level `templates`/`static`.
API_DIR = Path(__file__).resolve().parent
PROJ_DIR = API_DIR.parent
UI_DIR = PROJ_DIR / "ui"

if UI_DIR.exists():
	TEMPLATES_DIR = UI_DIR / "templates"
	STATIC_DIR = UI_DIR / "static"
else:
	# fallback to repository root `templates` and `static`
	ROOT = API_DIR.parent.parent
	TEMPLATES_DIR = ROOT / "templates"
	STATIC_DIR = ROOT / "static"


app = FastAPI(title="Carcassonne", debug=True)

# Mount static files at /static if they exist in the chosen UI location
if STATIC_DIR.exists():
	app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")

# Jinja2 templates
templates = Jinja2Templates(directory=str(TEMPLATES_DIR))

from .routes import router


@app.get("/", response_class=HTMLResponse)
def index(request: Request):
	"""Render the main index page from the selected templates directory."""
	return templates.TemplateResponse("index.html", {"request": request})

app.include_router(router)          # api routes (e.g. /user/{userId})
