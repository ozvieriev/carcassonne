"""
Routes and views for the flask application.
"""
from . import app
from datetime import datetime
from flask import render_template, request, jsonify
from fastapi import APIRouter, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

router = APIRouter()
templates = Jinja2Templates(directory="proj/templates")


@app.route('/')
@app.route('/home')
def home():
    """Renders the home page."""
    return render_template(
        'index.html',
        title='Home Page',
        year=datetime.now().year,
    )


@app.route('/contact')
def contact():
    """Renders the contact page."""
    return render_template(
        'contact.html',
        title='Contact',
        year=datetime.now().year,
        message='Your contact page.'
    )


@app.route('/about')
def about():
    """Renders the about page."""
    return render_template(
        'about.html',
        title='About',
        year=datetime.now().year,
        message='Your application description page.'
    )


@router.get("/signin", response_class=HTMLResponse)
def signin_get(request: Request):
    return templates.TemplateResponse("signin.html", {"request": request})


@router.post("/signin", response_class=HTMLResponse)
def signin_post(request: Request, username: str = Form(...), password: str = Form(...)):
    if not username or not password:
        return templates.TemplateResponse("signin.html", {"request": request, "error": "Username and password required"})
    return templates.TemplateResponse("signin_success.html", {"request": request, "username": username})
