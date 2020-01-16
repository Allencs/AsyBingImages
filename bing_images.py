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
        asyncio.run(self.download_links())

    async def download_links(self):
        for url in self.management.pageUrls:
            t = asyncio.create_task(
                self.client.get_link(url, self.management))
            self.tasks.append(t)

        for t in self.tasks:
            await t

    async def main(self):
        while True:
            count = 0
            for task in self.tasks:
                if not task.done:
                    count += 1

            if count == 0:
                logger.info('下载连接获取完成，开始下载')
                self.tasks.clear()
                break
            else:
                await asyncio.sleep(1)

        for downloadLink in self.management.downloadLinks:
            t = asyncio.create_task(self.client.download(downloadLink))
            self.tasks.append(t)

        for task in self.tasks:
            await task


if __name__ == '__main__':
    bing = BingImages()
    asyncio.run(bing.main())





