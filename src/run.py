"""This is the module where the app will run and we create the app instance"""

import os
from dotenv import load_dotenv, find_dotenv

from src.app import create_app

load_dotenv(find_dotenv())

env_name = os.getenv('FLASK_ENV')
app = create_app(env_name)

if __name__ == '__main__':
    port = os.getenv('FLASK_RUN_PORT')
    # run app
    app.run(host='0.0.0.0', port=port)
