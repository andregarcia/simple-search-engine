import glob
import os
import pathlib
import logging
import time

from src.index import Document
from src.index_instance import IndexSingleton


class IndexData:

    @classmethod
    def index_data(cls):
        index = IndexSingleton.get_instance()
        data = cls.__load_documents()
        logging.info("Indexing data...")
        start_time = time.time()
        for id, content in data:
            index.index_one(Document(id, content))
        total_time = time.time() - start_time
        logging.info(f"Finished indexing. Took [{total_time}] seconds")
        return index

    @staticmethod
    def __load_documents():
        start_time = time.time()
        logging.info("Loading data files...")
        data_dir = os.path.join(str(pathlib.Path(__file__).parent), '..', 'data')
        data_files = glob.glob(os.path.join(data_dir, '*'))
        logging.info(f"Found {len(data_files)} file to index in data directory {data_dir}")
        file_contents = []
        for file in data_files:
            with open(file, 'r') as f:
                id = file.split('/')[-1]
                content = ' '.join(f.readlines())
                file_contents.append((id, {'id' : id, 'main' : content}))
        total_time = time.time() - start_time
        logging.info(f"Finished loading data files. Took [{total_time}] seconds")
        return file_contents
