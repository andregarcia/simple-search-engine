import time
import logging
from flask import Flask, request

from src.controller_dict_encoder import ControllerDictEncoder
from src.index_data import IndexData
from src.index_instance import IndexSingleton

app = Flask(__name__)
app.json_encoder = ControllerDictEncoder


@app.route('/search', methods=['GET'])
def search():
    t_initial = time.time()
    q = request.args.get('q')
    size = request.args.get('size')
    index = IndexSingleton().get_instance()
    results = index.search('main', q, size)
    results = [r.doc['id'] for r in results]
    formatted_results = '\n'.join(results) + '\n'
    total_time = time.time() - t_initial
    formatted_execution_time_in_millis = str(total_time/1000).split('.')[0]
    formatted_results = f'Foram encontradas {len(results)} ocorrências pelo termo "{q}". Tempo de execução={formatted_execution_time_in_millis}ms\n' + formatted_results
    logging.info(f"Executed search for q={q}. Took [{total_time}] seconds")
    return str(formatted_results)


@app.route('/index', methods=['POST'])
def index_data():
    index = IndexData.index_data()
    return f"Index size is {index.size()}"
