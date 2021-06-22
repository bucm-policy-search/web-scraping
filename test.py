from elasticsearch import Elasticsearch
import uuid
from dotenv import load_dotenv
import os

load_dotenv()

username = os.environ["USERNAME"]
PASSWORD = os.environ["PASSWORD"]
URL = os.environ["URL"]
es = Elasticsearch(["http://{}:{}@{}/".format(username, PASSWORD, URL)])

body = {
    "query": {
        "bool": {
            "must": [
                {
                    "match": {
                        "title": {
                            "query": "北京市中医管理局2021年政府采购意向",
                            "operator": "and",
                        }
                    }
                },
                {"match": {"publishingDate": {"query": "2021-04-08", "operator": "and"}}},
            ]
        }
    }
}

insert_body = {"title": "test"}

print(es.count(index="test", body=body)["count"] == 0)
# print(es.create(index="test", body=insert_body, id=uuid.uuid1()))
