from urllib.parse import urljoin
from configuration import CONFIG
from configuration import logger


class Management(object):

    downloadLinks = set()
    baseUrl = "https://bing.ioliu.cn"
    pageUrls = set()

    def __init__(self):
        self.assign_urls()

    def __call__(self, *args, **kwargs):
        partial_link = args[0]
        image_link = urljoin(self.baseUrl,
                             partial_link.split("?")[0] + "?force=download")
        image_name = partial_link.split("?")[0].split("/")[2]
        self.downloadLinks.add((image_name, image_link))

    def assign_urls(self):
        count = 0
        while count < CONFIG['PageCount']:
            count += 1
            url = urljoin(self.baseUrl, "/?p={}".format(count))
            self.pageUrls.add(url)
        logger.info("finish assigning urls")


