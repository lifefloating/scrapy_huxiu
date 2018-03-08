from ..items import HuxiuItem
import scrapy
import logging


class HuxiuSpider(scrapy.Spider):
    name = "huxiu"
    allowed_domains = ["huxiu.com"]
    start_urls = [
        "https://www.huxiu.com/index.php"
    ]

    def parse(self, response):
        for sel in response.xpath('//div[@class="mod-info-flow"]/div/div[@class="mob-ctt"]'):  # 选取主页所有标题,返回列表
            item = HuxiuItem()
            item["title"] = sel.xpath("h2/a/text()").extract_first()  # 选取第一个标题
            item["link"] = sel.xpath("h2/a/@href").extract_first()  # 选取第一个标题的连接
            url = response.urljoin(item["link"])
            item["desc"] = sel.xpath("/div[@class='mob-sub']/text()").extract_first()  # 选取第一个新闻的简介
            yield scrapy.Request(url=url, callback=self.parse_article)

    def parse_article(self, response):
        detail = response.xpath('//div[@class="article-wrap"]')  # 选取相关的body
        item = HuxiuItem()
        item["title"] = detail.xpath("h1/text()")[0].extract().strip()  # 选取详细页标题
        item["link"] = response.url  # 这个URL就是response的url
        item["published"] = detail.xpath(
            'div[@class="article-author"]//span[@class="article-time pull-left"]/text()').extract()
        logging.info(item["title"], item["link"], item["published"])
        yield item


'''
		url_temp = response.url
		next_page = response.xpath(....) # 下一页标签xpath
		if next_page:
			next_page=response.urljoin(next_page)
'''
