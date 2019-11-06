import os

import app

config_name = os.getenv('FLASK_CONFIG')
app = app.app

if __name__ == '__main__':
    app.run()