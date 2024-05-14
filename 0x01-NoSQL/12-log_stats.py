#!/usr/bin/env python3
""" provides some stats about Nginx logs stored in MongoDB """
from pymongo import MongoClient


def log_stats():
    """ provides some stats about Nginx logs stored in MongoDB """
    client = MongoClient()

    db = client.logs
    collection = db.nginx

    total_logs = collection.count_documents({})

    print(f"{total_logs} logs")

    print('Methods:')
    http_methods = ["GET", "POST", "PUT", "PATCH", "DELETE"]
    for method in http_methods:
        count = collection.count_documents({"method": method})
        print(f"\tmethod {method}: {count}")

    count_status_check = collection.count_documents({"method": "GET", "path": "/status"})
    print(f"{count_status_check} status check")

    client.close()

if __name__ == "__main__":
    log_stats()

