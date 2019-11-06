import os
from gunicorn.app.base import Application
import app

class Nima(Application):
    def __init__(self):
        super().__init__()

    def init(self, parser, opts, args):
        self.load_config_from_module_name_or_filename('instance/config_gunicorn.py')

    def load(self):
        config_name = os.getenv('FLASK_CONFIG')
        _app = app.app
        return _app

 
if __name__ == '__main__':
    _app = Nima()
    _app.run()