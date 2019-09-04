```
#! -*- coding: utf-8 -*-


import json
import pprint


from flask import Flask
from flask import request
from multiprocessing import cpu_count
from concurrent.futures import ProcessPoolExecutor


app = Flask(__name__)
executor = ProcessPoolExecutor(cpu_count())


def async_handler(data):
    """put you code here ~"""
    pprint.pprint(('Got data: ', data))


@app.errorhandler(404)
def not_found(error):
    return 'Not found', 404


@app.route('/tradingview/', methods=['POST'])
def tradingview_service():
    try:
        request_data = json.loads(request.data)
    except ValueError:
        return 'Invalid data', 400
    future = executor.submit(async_handler, request_data)
    future.done()
    return 'Do success', 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)
```

