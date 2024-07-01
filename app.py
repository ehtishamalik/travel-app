import logging
from logging.handlers import RotatingFileHandler
from website import create_app

app = create_app()

if __name__ == "__main__":
    file_handler = RotatingFileHandler('error.log', maxBytes=10240, backupCount=10)
    file_handler.setLevel(logging.ERROR)
    formatter = logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
    )
    file_handler.setFormatter(formatter)
    app.logger.addHandler(file_handler)
    app.run()
