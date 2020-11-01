# Retic
from retic import App as app

"""Define all other apps"""


APP_BACKEND = {}

"""Add Backend apps"""
app.use(APP_BACKEND, "backend")
