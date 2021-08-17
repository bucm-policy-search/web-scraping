#!/usr/bin/python
# -*- coding: UTF-8 -*-

import smtplib
import os
import logging
from email.mime.text import MIMEText
from email.header import Header
from time import strftime

current_time = strftime("%Y-%m-%dT%H:%M:%S%z")
subject = f"{current_time} scrapy result"


def sendMail(sender, receivers, subject=subject):

    # 三个参数：第一个为文本内容，第二个 plain 设置文本格式，第三个 utf-8 设置编码
    message = MIMEText("爬虫完成", "plain", "utf-8")
    message["From"] = Header(sender, "utf-8")  # 发送者
    message["To"] = Header(receivers.as_string(), "utf-8")  # 接收者
    message["Subject"] = Header(subject, "utf-8")

    try:
        smtpObj = smtplib.SMTP("localhost")
        smtpObj.sendmail(sender, receivers, message.as_string())
        print("邮件发送成功")
    except smtplib.SMTPException:
        print("Error: 无法发送邮件")
