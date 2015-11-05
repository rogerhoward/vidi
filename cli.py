#!/usr/bin/env python
import requests, os, sys
from vidi import Server

command_list = ['add','search','ping', 'save', 'load', 'clear', 'bulk']

if __name__ == '__main__':
    import optparse
    parser = optparse.OptionParser()

    parser.add_option('-i', '--input', dest='path', help='read image from FILE', metavar="FILE")
    parser.add_option('-d', '--id', dest='id', help='index id', type=int)
    parser.add_option('-c', '--command', dest='command', help='command mode')
    parser.add_option('-p', '--port', dest='port', help='port number', type=int)
    parser.add_option('-o', '--host', dest='host', help='hostname')

    options, args = parser.parse_args()

    # if options.path is None:
    #     print ('sorry, you must provide the -i option at minimum')
        
    # elif os.path.exists(options.path) is False:
    #     print ('sorry, the path provided does not exist')
        
    # elif os.path.isfile(options.path) is False:
    #     print ('sorry, the path provided is not a file')
        


    if options.command is None:
        options.command = 'search'
    elif options.command not in command_list:
        print ('sorry, %s is not a supported command.' % (options.command))
        print ('supported commands are: %s' % (', '.join(command_list)))
        exit

    if options.port is None:
        options.port = 8001

    if options.host is None:
        options.host = 'localhost'

    server = Server(host=options.host, port=options.port)

    if options.command == 'ping':
        result = server.ping()
    elif options.command == 'bulk':
        if options.id is None:
            options.id = 1
        result = server.bulk(path=options.path, start=options.id)
    elif options.command == 'save':
        result = server.save(options.path)
    elif options.command == 'load':
        result = server.load(options.path)
    elif options.command == 'clear':
        result = server.clear()
    elif options.command == 'search':
        result = server.find(options.path)
    elif options.command == 'add':
        if options.id is None:
            print ('Sorry, the add command requires the -d ID parameter')
            sys.exit(0)
        else:
            result = server.add(options.path, options.id)


    print(result)