from typing import Any, Dict, Text, Tuple
import logging

from flask import Flask, render_template  # type: ignore[import]

from ...schema import Schema


app = Flask(__name__)
schemas_by_project_dir: Dict[str, Schema] = {}


def run_server() -> None:
    # silence request log
    log = logging.getLogger('werkzeug')
    log.setLevel(logging.WARNING)

    app.run()


@app.route('/')
def index() -> Text:
    return render(
        'index.html.j2',
        schemas_by_project_dir=schemas_by_project_dir
    )


@app.errorhandler(404)
def not_found(_error: Any) -> Tuple[Text, int]:
    return render('not-found.html.j2'), 404


def render(template: str, **kwargs: Any) -> Text:
    return render_template(
        template,
        hostname="devbox.localhost",
        **kwargs
    )