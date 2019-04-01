from flask import render_template

from core import core


@core.route('/')
def index_route():
    return render_template('index.html')
