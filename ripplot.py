#!/usr/bin/env python
import time
import argparse
import sys
import os
import datetime

from ripple import rpc, storage, const, utils


parser = argparse.ArgumentParser()
subparsers = parser.add_subparsers(help='ripplot subparsers')
#sync command
parser_sync = subparsers.add_parser('sync', help='syncs ledgers')
parser_sync.add_argument('--delay', '-d', type=int, default=1, help='delay between checks in seconds, defaults to 5')
parser_sync.add_argument('--cache', '-c', type=str, default=f'{const.RIPPLE_HOME}', help='ripple folder to store cached content')
parser_sync.set_defaults(fn='sync')
#plot command
parser_plot = subparsers.add_parser('plot', help='generates a plot file to be used by gnuplot')
parser_plot.add_argument('--cache', '-c', type=str, default=f'{const.RIPPLE_HOME}', help='ripple folder to store cached content')
parser_plot.add_argument('--output', '-o', type=str, default='', help='path to write the plot file, prints to stdout if empty')
parser_plot.set_defaults(fn='plot')
#status command
status_plot = subparsers.add_parser('status', help='shows ripplot status')
status_plot.add_argument('--cache', '-c', type=str, default=f'{const.RIPPLE_HOME}', help='ripple folder to store cached content')
status_plot.set_defaults(fn='status')


def sync(ns):
    if rpc.ping().get('result', {}).get('status', '') != 'success':
        print('[ERROR] Server is not for usage')
        os.exit(const.ERROR_CODE)
    else:
        print('[INFO] Server is ready and available, start pooling')
    storage.ensure_dir(ns.cache)
    while True:
        data = rpc.server_info()
        info = data['result']['info'] 
        ledger = info['validated_ledger']
        ledger['ts'] = str(datetime.datetime.now())
        print(f'[INFO] Storing ledger {ledger["hash"]}')
        storage.store(ns.cache, ledger)
        print(f'[INFO] Stored ledger {ledger["hash"]}')
        time.sleep(ns.delay)


def plot(ns):
    output = []
    for fname in os.listdir(ns.cache):
        data = storage.retrieve(ns.cache, fname)
        ages = [i for i in data if 'age' in data]
        if len(data) > 1:
            #diff = utils.diff_ts(data[0]['ts'], data[-1:][0]['ts'])
            output.append((data[-1:][0]['ts'], data[0]['seq']))
    if not ns.output:
        print(utils.format_plot(output))
        sys.exit(const.EXIT_CODE)
    with open(ns.output, 'w+') as f:
        f.write(format_plot(output))
    os.exit(const.EXIT_CODE)


def status(ns):
    ts = []
    total_ledgers = len(os.listdir(ns.cache))
    for fname in os.listdir(ns.cache):
        data = storage.retrieve(ns.cache, fname)
        if len(data) > 1:
            diff = utils.diff_ts(data[0]['ts'], data[-1:][0]['ts'])
            ts.append(diff)
    output = [
        f'Total ledgers: {total_ledgers}',
        f'Fatest validation time: {min(ts)} seconds',
        f'Slowest validation time: {max(ts)} seconds',
        f'Average validation time: {int(sum(ts) / len(ts))} seconds'
    ]
    print('\n'.join(output))


ref = {
    'sync': sync,
    'plot': plot,
    'status': status
}


def main():
    ns = parser.parse_args()
    if not hasattr(ns, 'fn'):
        parser.print_help()
        sys.exit(1)
    fn = ref.get(ns.fn)
    if not fn:
        parser.print_help()
        sys.exit(1)
    fn(ns)


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('[INFO] Exiting gracefully...')
        sys.exit(const.EXIT_CODE)