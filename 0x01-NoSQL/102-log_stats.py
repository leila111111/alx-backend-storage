#!/usr/bin/env python3
'''Improve 12-log_stats.py by adding the top 10 of the most present IPs in the collection nginx of the database logs:'''
from pymongo import MongoClient

if __name__ == '__main__':
    client = MongoClient('mongodb://127.0.0.1:27017')
    print('{} logs'.format(client.logs.nginx.count_documents({})))
    print('Methods:')
    methods = ['GET', 'POST', 'PUT', 'PATCH', 'DELETE']
    for method in methods:
        meth_count = client.logs.nginx.count_documents({"method": method})
        print('\tmethod {}: {}'.format(method, meth_count))
    count_stat = client.logs.nginx.count_documents({"method": "GET", "path": "/status"})
    print('{} status check'.format(count_stat))
    count_log = client.logs.nginx.aggregate(
        [
            {
                '$group': {'_id': "$ip", 'req': {'$sum': 1}}
            },
            {
                '$sort': {'req': -1}
            },
            {
                '$limit': 10
            },
        ]
    )
    for log in count_log:
        print('\t{}: {}'.format(log['_id'], log['req']))