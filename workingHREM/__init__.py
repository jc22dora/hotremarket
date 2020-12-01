
from flask import Flask

app = Flask(__name__)
app.config['SECRET_KEY'] = 'key'

FLASK_APP='workingHREM'

import routes
