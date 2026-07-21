import dash
from dash import dcc, html, dash_table, Input, Output, State, callback_context
import dash_bootstrap_components as dbc
import logging
from flask import Flask, send_from_directory, render_template, send_file, make_response, request
from weasyprint import HTML
import webbrowser
import io
import pandas as pd
from dash.exceptions import PreventUpdate
import base64
import os
from urllib.parse import urlparse, parse_qs
from dotenv import load_dotenv

load_dotenv()

from apps.extensions import bcrypt   # safe: extensions.py has no circular deps

server = Flask(__name__)

# Required for flask.session (used by login/router code) to work.
# Set FLASK_SECRET_KEY in your .env file — generate one with:
#   python -c "import secrets; print(secrets.token_hex(32))"
server.secret_key = os.environ["FLASK_SECRET_KEY"]

app = dash.Dash(
    __name__,
    server=server,  # <-- bind Dash to the SAME Flask instance we configured above
    external_stylesheets=["assets/bootstrap.css", dbc.themes.BOOTSTRAP, dbc.icons.BOOTSTRAP],
)

bcrypt.init_app(server)

app.config.suppress_callback_exceptions = True
app.css.config.serve_locally = True
app.scripts.config.serve_locally = True
app.title = 'TINQAD'

log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

# dbconnect (and anything else under apps/) is safe to import now —
# server, app, and bcrypt all exist at this point, so no circular import.
from apps import dbconnect as db

#if __name__ == '__main__':
    # app.run_server(host='10.206.100.41',port=8050)
   # webbrowser.open('http://10.206.100.41:8050/',autoraise=True)


# if __name__ == '__main__':
#     # Run the app on all network interfaces (10.206.100.41) on port 8050
#     app.run_server(host='10.206.100.41', port=8050)
    
#     # Optionally, open the web browser to the correct URL
#     url = 'http://10.206.100.41:8050/'
#     webbrowser.open(url, new=0, autoraise=True)