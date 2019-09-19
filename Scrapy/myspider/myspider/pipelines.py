# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import json
import logging

logger = logging.getLogger(__name__)


class MyspiderPipeline(object):
    def process_item(self, item, spider):
        # 这个地方名字也是不能改，定死了的
        # print(item)
        with open('save_test.txt', 'a') as f:
            json.dump(item, f, ensure_ascii=False, indent=2)

        logger.warning('-'*10)
        return item


