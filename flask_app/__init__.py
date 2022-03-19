from flask import Flask
from os.path import join, dirname, realpath


UPLOAD_FOLDER_RECIPE = join(dirname(realpath(__file__)), 'static/uploads/recipe/')
UPLOAD_FOLDER_TRAVEL = join(dirname(realpath(__file__)), 'static/uploads/travel/')
UPLOAD_FOLDER_USER = join(dirname(realpath(__file__)), 'static/uploads/user/')

app = Flask(__name__)

app.secret_key = "Goku is Awesome!!!"
app.config['UPLOAD_FOLDER_RECIPE'] = UPLOAD_FOLDER_RECIPE
app.config['UPLOAD_FOLDER_TRAVEL'] = UPLOAD_FOLDER_TRAVEL
app.config['UPLOAD_FOLDER_USER'] = UPLOAD_FOLDER_USER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024