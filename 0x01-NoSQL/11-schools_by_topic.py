#!/usr/bin/env python3
""" Python function that returns the list of school having a specific topic:"""


def schools_by_topic(mongo_collection, topic):
    """  Python function that returns the list of school having a specific topic:"""
    topic = {'topics': topic}
    return [doc for doc in mongo_collection.find(topic)]