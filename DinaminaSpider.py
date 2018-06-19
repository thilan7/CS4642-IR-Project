import scrapy

class DinaminaSpider(scrapy.Spider):
    i=0
    name = "dinamina"
    start_urls = ['http://www.dinamina.lk/date/2018-06-18']

    def parse(self, response):
        DinaminaSpider.i+=1
        for article_url in response.css('.field-content a ::attr("href")').extract():
            yield response.follow(article_url, callback=self.parse_article)
        older_posts = response.css('.date-prev a ::attr("href")').extract_first()
        print (DinaminaSpider.i)
        if (older_posts is not None) and (DinaminaSpider.i<501):
            yield response.follow(older_posts, callback=self.parse)

    def parse_article(self, response):
        content = response.xpath(".//div[@class='field-item even']/descendant::text()").extract()
        author = response.xpath(".//div[@class='field field-name-field-author-s- field-type-node-reference field-label-hidden']/descendant::text()").extract()
        yield {'author(s)': ''.join(author),'article': ''.join(content)}

