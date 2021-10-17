"""
Python知否：如何编写高效网络IO程序

如何侧写程序瓶颈？如何加速网络IO程序？9012年，别再多线程了，Asyncio一行拯救IO
源代码：https://github.com/wangzhe3224/Python-zhifou
欢迎关注微信视频号：Python知否
欢迎关注公众号：泛程序员 - 一个为非计算机专业程序员充电的地方
"""
import re
import logging
import pathlib
import requests
import httpx
import asyncio

logging.basicConfig()
logging.root.setLevel(logging.INFO)

path = pathlib.Path(__file__).parent.resolve()

def find():
    logging.info(f"Start...")
    with open(f'{path}/webside.md', 'r', encoding="utf-8") as f:
        urls = [line.strip() for line in f.readlines()]
    
    pages = []
    for url in urls:
        pages.append(requests.get(url).text)
        
    https, http = 0, 0
    for page in pages:
        https += len(re.findall("https://", page))
        http += len(re.findall("http://", page))
    
    logging.info(f"{https = } vs {http = }")
    logging.info(f"...")

async def find_fast():
    logging.info(f"Start...")
    with open(f'{path}/webside.md', 'r', encoding="utf-8") as f:
        urls = [line.strip() for line in f.readlines()]
    
    async with httpx.AsyncClient() as client:
        tasks = (client.get(url) for url in urls)
        resp = await asyncio.gather(*tasks)
    
    pages = [res.text for res in resp]
        
    https, http = 0, 0
    for page in pages:
        https += len(re.findall("https://", page))
        http += len(re.findall("http://", page))
    
    logging.info(f"{https = } vs {http = }")
    logging.info(f"...")


def main():
    import cProfile
    import pstats
    
    with cProfile.Profile() as pf:
        # find()
        asyncio.run(find_fast())
    
    stats = pstats.Stats(pf)
    stats.sort_stats(pstats.SortKey.TIME)
    stats.print_stats(10)
    stats.dump_stats(f"{path}/profiling.prof")

if __name__ == "__main__":
    
    main()