import os
import shutil
import scrapy
from scrapy.exceptions import NotSupported

class QuoteSpider(scrapy.Spider):
    name = 'quote-spdier'
    start_urls = ['https://kvadrat.se/', 'https://kvadrat.se/anlita-kvadrat/hitta-konsult/?q=#results']
    walk_urls = []
    url_file = open('urls.txt', mode='w')
    content_file_dir = 'contents/'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        shutil.rmtree(self.content_file_dir, ignore_errors=False)

    def parse(self, response):
        if response.status >= 400:
            return
        os.makedirs(self.content_file_dir, exist_ok=True)
        CONTENT_SELECTOR = 'article *::text'
        NEXT_LINK_SELECTOR = 'a::attr("href")'
        NEXT_FORM_SELECTOR = 'form'
        file_url = f'{self.content_file_dir}/index_{response.url.split("//")[-1].replace("/", "_")}'
        with open(file_url, mode='ab') as f:
            try:
                content = '\n'.join(c for c in response.css(CONTENT_SELECTOR).getall() if c.strip())
                f.write(content.encode('utf-8') + b'\n')
                yield { 'text': content }
            except NotSupported:
                print(f"Found another document format saving {file_url}")
                f.write(response.body)
                return

        for next_page in response.css(NEXT_LINK_SELECTOR):
            new_url = next_page.get()
            for base in self.start_urls:
                new_url = new_url.replace(base, '/')
            if new_url[0] not in ['.', '/', '?']:
                continue
            if new_url in self.walk_urls:
                continue
            url = response.urljoin(new_url)
            self.url_file.write(url + '\n')
            self.walk_urls.append(new_url)
            yield scrapy.Request(url)
        for next_form in response.css(NEXT_FORM_SELECTOR):
            form = scrapy.FormRequest.from_response(
                response,
                formdata={},
                callback=self.after_login,
            )
            yield form
