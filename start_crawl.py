import os
import logging
import schedule
import time
from time import strftime
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from dotenv import load_dotenv

from mail import sendMail
from webSpider.spiders.BATCM import BATCM
from webSpider.spiders.NATCM import NATCM
from webSpider.spiders.HCOHP import HCOHP


import argparse

parser = argparse.ArgumentParser(description="Crawl Parameters")
parser.add_argument(
    "-m",
    "--mode",
    help=' 爬虫模式：测试模式 or 生产模式 - "dev(development)" / "prod(production)"，默认 "prod" ',
    default="prod",
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
    check_folder = os.path.isdir("./logs")
    if not check_folder:
        os.makedirs("./logs/", mode=0o755)

    current_time = strftime("%Y-%m-%dT%H:%M:%S%z")
    logging.basicConfig(
        format="%(asctime)s %(levelname)s:%(message)s",
        filename=f"./logs/scrapy_{current_time}.log",
        level=logging.WARNING,
    )  # ISO 8601 Timestamp format

    process = CrawlerProcess(get_project_settings())

    process.crawl(BATCM, mode=crawl_mode)
    process.crawl(NATCM, mode=crawl_mode)
    process.crawl(HCOHP, mode=crawl_mode)

    process.start()

    load_dotenv()

    if ("SENDER" in os.environ) and ("RECEIVERS" in os.environ):
        SENDER = os.environ["SENDERS"]
        RECEIVERS = os.environ.get["RECEIVERS"]
        sendMail(sender=SENDER, receivers=RECEIVERS)


if crawl_auto == "non":
    job()
else:
    schedule.every().day.at("19:35").do(job)

    logging.info("Start crawling.")

    while True:
        schedule.run_pending()
        time.sleep(1)
