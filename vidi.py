#!/usr/bin/env python
import requests, os, sys
command_list = ['add', 'search']
url_base = ''


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

    parser.add_option('-i', '--input', dest='path', help='read image from FILE', metavar="FILE")
    parser.add_option('-d', '--id', dest='id', help='index id', type=int)
    parser.add_option('-c', '--command', dest='command', help='command mode')
    parser.add_option('-p', '--port', dest='port', help='port number', type=int)
    parser.add_option('-o', '--host', dest='host', help='hostname')

    options, args = parser.parse_args()

    if options.path is None:
        print 'sorry, you must provide the -i option at minimum'
        exit
    elif os.path.exists(options.path) is False:
        print 'sorry, the path provided does not exist'
        exit
    elif os.path.isfile(options.path) is False:
        print 'sorry, the path provided is not a file'
        exit


    if options.command is None:
        options.command = 'search'
    elif options.command not in command_list:
        print 'sorry, %s is not a supported command.' % (options.command)
        print 'supported commands are: %s' % (', '.join(command_list))
        exit

    if options.port is None:
        options.port = 8000

    if options.host is None:
        options.host = 'localhost'

    url_base = 'http://%s:%s' % (options.host, options.port)

    if options.command == 'search':
        the_result = find(options.path)
    elif options.command == 'add':
        if options.id is None:
            print 'Sorry, the add command requires the -d ID parameter'
            sys.exit(0)
        else:
            the_result = add(options.path, options.id)

    # print the_result