import time
from configuration import logger
from client import Client
from url_management import Management
import os
import asyncio

"""
说明：用于下载Bing壁纸，使用asyncio进行异步操作
主要分为两步：
1、获取图片下载链接
2、下载
两个步骤分别采用异步执行
"""


def check_path():
    """
    检查文件路径是否存在
    :return:
    """
    if not os.path.exists(r".\images"):
        os.mkdir(r".\images")


class BingImages(object):

    tasks = []  # 异步任务列表

    def __init__(self):
        check_path()
        self.management = Management()
        self.client = Client()
        self.startTime = time.time()
        asyncio.run(self.download_links())

    async def download_links(self):
        for url in self.management.pageUrls:
            t = asyncio.create_task(
                self.client.get_link(url, self.management))
            self.tasks.append(t)

        await asyncio.gather(*self.tasks)

        logger.info('下载链接获取完成，开始下载')
        self.tasks.clear()

    async def main(self):

        # t = asyncio.create_task(self.client.download(self.management.downloadLinks))
        # self.tasks.append(t)

        for downloadLink in self.management.downloadLinks:
            t = asyncio.create_task(self.client.download(downloadLink))
            self.tasks.append(t)

        await asyncio.gather(*self.tasks)

        duration = time.time() - self.startTime
        logger.info("用时： %.2fs" % duration)


if __name__ == '__main__':
    bing = BingImages()
    asyncio.run(bing.main())





