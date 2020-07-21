# simple-search-engine

Pequena aplicação para indexação e busca de documentos.


Esta aplicação foi desenvolvida e testada com Python 3.7.4

Modo de execução:

1. `pip install -r requirements.txt` (instala as dependências)
2. `PYTHONPATH=./:$PYTHONPATH python src/main.py` (sobe o servidor contendo a aplicação com os dado a serem indexados)
3. Aguardar os documentos serem indexados e o servidor estar disponível. Isso leva alguns segundos, mas é rápido e pode ser visto no log do console.
4. Em outro terminal, execute `python src/search.py "termo a ser buscado"` (Executa uma busca. Troque o termo a ser buscado de acordo com sua busca)

Executar testes:

1. `python -m unittest test/*.py`

