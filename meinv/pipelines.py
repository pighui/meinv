# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import csv
import os

from scrapy import Request
from scrapy.pipelines.images import ImagesPipeline
from meinv import settings
from util.sha_1 import sha_name


class MvImagePipeline(ImagesPipeline):
    def get_media_requests(self, item, info):
        for url in item['image_urls']:
            yield Request(url, meta={'name': item['name']})

    def item_completed(self, results, item, info):
        #将下载完成后的图片路径设置到item中
        item['images'] = [x for ok, x in results if ok]
        return item


    def file_path(self, request, response=None, info=None):
        # 为每位人员创建一个目录，存放她自己所有的图片
        author_name = request.meta['name']
        author_dir = os.path.join(settings.IMAGES_STORE, author_name)
        if not os.path.exists(author_dir):
            os.makedirs(author_dir)
        #从连接中提取文件名和扩展名
        try:
            filename = request.url.split("/")[-1].split(".")[0]
        except:
            filename = sha_name(request.url)
        try:
            ext_name = request.url.split(".")[-1]
        except:
            ext_name = 'jpg'

        # 返回的相对路径
        return '%s/%s.%s' % (author_name, filename, ext_name)


class MeinvPipeline(object):
    def __init__(self):
        self.csv_filename = 'meinv.csv'
        self.existed_header = False
    def process_item(self, item, spider):
        # item dict对象，是spider.detail_parse() yield{}输出模块
        with open(self.csv_filename, 'a', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=(
                'name', 'hometown', 'birthday', 'detail_url'))
            if not self.existed_header:
                # 如果文件不存在，则表示第一次写入
                writer.writeheader()
                self.existed_header = True
            image_urls = ''
            for image_url in item['image_urls']:
                image_urls += image_url + ','
            image_urls.strip("\"").strip("\'")
            data = {
                'name': item['name'].strip(),
                'hometown': item['hometown'],
                'birthday': item['birthday'].replace('年', '-').replace('月', '-').replace('日', ''),
                'detail_url': item['detail_url'],
            }
            writer.writerow(data)
            f.close()
        return item