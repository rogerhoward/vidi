#!/usr/bin/env python
import requests


def add(path, id):
    url = 'http://localhost:8000/index/images/%s' % (id)
    # files = {'file': open(path, 'rb')}
    # r = requests.put(url, files=files)
    # return r.json()

    with open(path) as fo:
        body_data = fo.read()
        r = requests.put(url, data=body_data, headers={'content-type':'image/jpeg'})

    return r.json()

def find(path):
    url = 'http://localhost:8000/index/searcher'

    with open(path) as fo:
        body_data = fo.read()
        r = requests.post(url, data=body_data, headers={'content-type':'image/jpeg'})

    return r.json()

if __name__ == '__main__':
    import optparse
    parser = optparse.OptionParser()
    options, args = parser.parse_args()

    if args:
        if args[0] == 'add':
            input_path = args[1]
            this_file_num = input_path[-8:][0:4]
            print input_path, this_file_num
            the_result = add(input_path, this_file_num)
            print the_result
        elif args[0] == 'find':
            input_path = args[1]
            the_result = find(input_path)
            print the_result