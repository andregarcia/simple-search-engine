import logging
logging.basicConfig(level=logging.INFO)


from src.controller import app
from src.index_data import IndexData

if __name__ == '__main__':
    IndexData.index_data()
    app.logger.setLevel(logging.INFO)
    app.run()
