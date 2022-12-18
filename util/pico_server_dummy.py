

from flask import Flask
from flask_cors import CORS
import json

app = Flask(__name__)
CORS(app)

@app.route("/state")
def hello_world():
    
    obj = {"kebab_lvl":1337, "svarv_lvl":420, "kebab_margins":"5 pommes dB"}

    return json.dumps(obj)


