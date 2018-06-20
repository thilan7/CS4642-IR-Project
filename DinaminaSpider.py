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
        url = response.url
        title = response.css("#page-title::text").extract()
        date = response.css(".date-display-single::text").extract()
        authors = response.xpath(    ".//div[@class='field field-name-field-author-s- field-type-node-reference field-label-hidden']/descendant::text()").extract()
        category = response.xpath(    ".//div[@class='field field-name-field-section field-type-taxonomy-term-reference field-label-hidden']/descendant::text()").extract()
        context = response.xpath(    ".//div[@class='field field-name-body field-type-text-with-summary field-label-hidden']/descendant::text()").extract()
        tags = response.xpath(    ".//div[@class='field field-name-field-articletags field-type-taxonomy-term-reference field-label-above']/descendant::text()").extract()[1:]
        relatedNews = response.xpath(    ".//div[@class='field field-name-field-related-content field-type-node-reference field-label-above']/div/div/a/@href").extract()
        yield {'URL': ''.join(url), 'Title': ''.join(title), 'Date': ''.join(date), 'Author(s)': ''.join(authors),'Category': ''.join(category), 'Context': ''.join(context), 'Tags': ''.join(tags),'RelatedNews': ''.join(relatedNews)}

