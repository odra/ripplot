import json

import requests


def do(body, protocol='https', host='s1.ripple.com', port=51234):
    headers = {
        'Content-Type': 'application/json'
    }
    res = requests.post(f'{protocol}://{host}:{port}', data=json.dumps(body), headers=headers)
    return res.status_code, res.text


def ping(**kwargs):
    body = {
        'method': 'ping'
    }
    code, data = do(body, **kwargs)
    return json.loads(data)


def server_info(**kwargs):
    body = {
        'method': 'server_info'
    }
    code, data = do(body, **kwargs)
    return json.loads(data)


def tx(tx_hash, **kwargs):
    body = {
        'method': 'tx',
        'params': [
            {'transaction': tx_hash}
        ]
    }
    code, data = do(body, **kwargs)
    return json.loads(data)