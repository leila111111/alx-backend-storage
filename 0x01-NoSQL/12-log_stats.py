#!/usr/bin/env python3
'''Python script that provides some stats about Nginx logs stored in MongoDB:'''
from pymongo import MongoClient

if __name__ == '__main__':
    client = MongoClient('mongodb://127.0.0.1:27017')
    print_nginx_request_logs(client.logs.nginx)
    print('{} logs'.format(client.logs.nginx.count_documents({})))
    print('Methods:')
    methods = ['GET', 'POST', 'PUT', 'PATCH', 'DELETE']
    for method in methods:
        meth_count = client.logs.nginx.count_documents({"method": method})
        print('\tmethod {}: {}'.format(method, meth_count))
    count_stat = client.logs.nginx.count_documents({"method": "GET", "path": "/status"})
    print('{} status check'.format(count_stat))