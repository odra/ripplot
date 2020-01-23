import datetime


def total(data):
    i = 0
    for item in data:
        if 'age' in item:
            i += int(item['age'])
    return i


def format_plot(data):
    output = []
    for (total, seq) in data:
        output.append(f'{total}\t{seq}')
    return '\n'.join(output)


def diff_ts(start, end, date_format='%Y-%m-%d %H:%M:%S.%f'):
    a = datetime.datetime.strptime(start, date_format)
    b = datetime.datetime.strptime(end, date_format)
    delta = b - a
    return delta.seconds