import logging
import schedule
import time
from time import strftime
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

from webSpider.spiders.websites.BATCM import BATCM

import argparse

parser = argparse.ArgumentParser(description="Crawl Parameters")
parser.add_argument(
    "-m",
    "--mode",
    help=' 爬虫模式：测试模式 or 生产模式 - "dev(development)" / "pro(production)"，默认 "dev" ',
    default="develop",
)
parser.add_argument(
    "-a",
    "--auto",
    help=' 是否开启定点自动爬虫 - "auto(Automatic)" / "non(Non-automatic)"，默认 "auto" ',
    default="auto",
)
args = parser.parse_args()

crawl_mode = args.mode

crawl_auto = args.auto


def job():

    current_time = strftime("%Y-%m-%dT%H:%M:%S%z")

    logging.basicConfig(
        format="%(asctime)s %(levelname)s:%(message)s",
        filename=f"./logs/scrapy_{current_time}.log",
        level=logging.DEBUG,
    )  # ISO 8601 Timestamp format

    process = CrawlerProcess(get_project_settings())
    process.crawl(BATCM, mode=crawl_mode)
    process.start()


if crawl_auto == "non":
    job()
else:
    schedule.every().day.at("03:30").do(job)

    while 1:
        schedule.run_pending()
        time.sleep(1)
