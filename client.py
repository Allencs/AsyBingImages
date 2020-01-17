from configuration import logger
import aiohttp
from bs4 import BeautifulSoup
import asyncio


class Client(object):

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
                      ' (KHTML, like Gecko) Chrome/67.0.3396.87 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Connection': 'keep-alive'
    }

    lock = asyncio.Lock()

    def __init__(self):
        pass

    async def get_link(self, url, management):
        """
        获取图片链接
        :param url: 页面地址
        :param management: URL管理器
        :return: None
        """
        async with aiohttp.ClientSession(headers=self.headers) as session:
            async with session.get(url) as resp:
                data = await resp.text()
                for tag in self.parser(data):
                    async with self.lock:
                        management(tag['href'])

    @staticmethod
    def parser(html):
        """
        解析HTML页面，获取相关元素
        :param html:
        :return:
        """
        soup = BeautifulSoup(html, 'html.parser')
        tags = soup.find_all("a", attrs={'class': 'mark'})
        return tags

    @staticmethod
    async def download(download_link):
        """
        下载图片
        :param download_link: 下载链接
        :return: None
        """
        # async with aiohttp.ClientSession() as session:
        #     for link in download_links:
        #         image_name = link[0]
        #         async with session.get(link[1]) as resp:
        #             with open(r".\images\{}.jpg".format(image_name), "wb+") as f:
        #                 while True:
        #                     chunk = await resp.content.read(1024)
        #                     if not chunk:
        #                         break
        #                     f.write(chunk)
        #             logger.info(image_name)

        async with aiohttp.ClientSession() as session:
            image_name = download_link[0]
            try:
                async with session.get(download_link[1]) as resp:
                    with open(r".\images\{}.jpg".format(image_name), "wb+") as f:
                        while True:
                            chunk = await resp.content.read(1024)
                            if not chunk:
                                break
                            f.write(chunk)
                    logger.info(image_name)

            except asyncio.TimeoutError:
                print("{} 下载超时".format(image_name))
            except Exception as e:
                raise e


if __name__ == '__main__':
    pass












