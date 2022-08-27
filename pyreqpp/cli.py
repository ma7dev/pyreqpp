"""PyReqPP CLI implementation."""
# inspired by: https://github.com/hadialqattan/pycln
import os

import typer

from .utils import check
from . import __doc__, __name__

app = typer.Typer(name=__name__, add_completion=True)


@app.command(context_settings=dict(help_option_names=["-h", "--help"]))
def main(  # pyreqpp: disable=R0913,R0914
    requirements_path: str = typer.Option(
        f"{os.getcwd()}/requirements.txt",
        "--requirements-path",
        "-r",
        show_default=False,
        help=("Where does requirements.txt live?"),
    ),
    verbose: bool = typer.Option(
        False,
        "--verbose",
        "-v",
        show_default=True,
        help=(
            "Also emit messages to stderr about files"
            " that were not changed and about files/imports that were ignored."
        ),
    ),
):
    print(requirements_path)
    print(verbose)
    requirements_path = os.path.abspath(requirements_path)
    check(requirements_path, verbose)


# Override main function `__doc__`.
# This `__doc__` has read from `pyproject.toml`.
main.__doc__ = __doc__
