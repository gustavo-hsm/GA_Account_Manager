from src.view import Interface as i
from src.controller import Log_Handler as lh
from src.controller import GA_API_Handler as ga

from flask import Flask
from logging import INFO

app = Flask(__name__, template_folder='src/view/templates')
app.config['SECRET_KEY'] = 'temporary-key'
app.logger.addHandler(lh.error_logger_file_handler())
app.logger.setLevel(INFO)

@app.route('/', methods=['GET'])
@app.route('/index', methods=['GET'])
def welcome():
    return i.render_welcome()

@app.route('/summary', methods=['POST'])
def start_engine():
    return i.render_account_summary()

@app.route('/dbsync', methods=['POST'])
def import_to_database():
    return i.render_db_sync()

@app.errorhandler(404)
def resource_not_found(error):
    return i.render_error_page(404)

@app.errorhandler(500)
def internal_error(error):
    return i.render_error_page(500)
