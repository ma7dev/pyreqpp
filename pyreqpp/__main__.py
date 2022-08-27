"""Entry point to run PyReqPP as a module."""
from . import __name__
from .cli import app

app(prog_name=__name__)
