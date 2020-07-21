
import sys

import requests

if __name__ == '__main__':
    q = sys.argv[1]
    print(q)
    results = requests.get(f'http://localhost:5000/search?q={q}')
    print(results.text)

