# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from elasticsearch import Elasticsearch
from dotenv import load_dotenv
import os
from time import strftime
import uuid
import logging


class ElasticSearchPipeline:
    def __init__(self):
        self.es = {}
        self.es_connected = True

    def connect_elasticsearch(self):
        load_dotenv()
        logging.debug("print config value: %s", os.environ)

        USERNAME = os.environ.get("USERNAME", False)
        PASSWORD = os.environ.get("PASSWORD", False)
        URL = os.environ.get("URL", False)

        if not (USERNAME and PASSWORD and URL):
            self.es_connected = False
        else:
            # 详情参考官方文档 https://elasticsearch-py.readthedocs.io/en/7.x/
            try:
                self.es = Elasticsearch(
                    ["http://{}:{}@{}/".format(USERNAME, PASSWORD, URL)]
                )
                logging.debug("ElasticSearch connected")

                INDEX = os.environ.get("ES_INDEX", "changeme")

                self.es.search(index=INDEX, filter_path=["hits.total.value"])
            except Exception:
                logging.error("Fail to connect ElasticSearch.")
                self.es_connected = False

    def open_spider(self, spider):
        self.connect_elasticsearch()

    def close_spider(self, spider):
        self.es.close()

    def process_item(self, item, spider):

        if self.es_connected:

            logging.debug("Processing items in pipelines: {}".format(item))

            index = os.environ["ES_INDEX"]

            logging.debug("publishingDate: " + item["publishingDate"])

            search_body = {
                "query": {
                    "bool": {
                        "must": [
                            {"term": {"title.keyword": {"value": item["title"]}}},
                            {"match": {"publishingDate": item["publishingDate"]}},
                            {
                                "term": {
                                    "urlSource.keyword": {"value": item["urlSource"]}
                                }
                            },
                        ]
                    }
                }
            }

            insert_body = ItemAdapter(item).asdict()
            insert_body["@timestamp"] = strftime("%Y-%m-%dT%H:%M:%S%z")

            result = self.es.search(
                index=index,
                body=search_body,
                filter_path=["hits.hits._id", "hits.total.value"],
            )

            id = ""
            count = result["hits"]["total"]["value"]

            if count == 0:
                self.es.create(index=index, body=insert_body, id=uuid.uuid1())
            else:
                id = result["hits"]["hits"][0]["_id"]
                self.es.update(index=index, id=id, body={"doc": insert_body})

        return item
