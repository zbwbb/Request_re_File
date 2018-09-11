import json
import time
import requests
from requests.exceptions import RequestException
import UserAgent
import re
from multiprocessing import Pool


def get_one_page(url):
    try:
        response = requests.get(url, headers=UserAgent.get_user_agent())
        if response.status_code == 200:
            return response.text
        return None
    except RequestException as e:
        print(e.response)
        return None


def parse_one_page(html):
    pattern = re.compile('<dd>.*?board-index.*?">(\d+)</i>.*?title="(.*?)".*?'
                         'data-src="(.*?)".*?class="star">(.*?)</p>.*?class="releasetime">(.*?)</p>.*?'
                         'class="integer">(.*?)</i>.*?class="fraction">(.*?)</i></p', re.S)
    list_info = re.findall(pattern, html)
    for item in list_info:
        yield {
            'index': item[0],
            'title': item[1],
            'image': item[2],
            'actor': item[3].strip()[3:] if len(item[3]) > 3 else "",
            'time': item[4].strip()[5:] if len(item[4]) > 5 else "",
            'score': item[5].strip() + item[6].strip()
        }
    return list_info


def write_to_file(content):
    with open('result.txt', 'a') as f:
        f.write(json.dumps(content, ensure_ascii=False) + "\n")


def main(offset):
    url = 'http://maoyan.com/board/4?offset=' + str(offset)
    html = get_one_page(url)
    list_info = parse_one_page(html)
    for item in list_info:
        write_to_file(item)


if __name__ == '__main__':
    # 方式一
    # start = time.time()
    # for i in range(0, 11):
    #     main(i * 10)
    #     time.sleep(1)
    # end = time.time()
    # print("Running time %s Seconds" % (end-start))
    # 耗时 12秒
    # # 方式二
    start = time.time()
    pool = Pool(processes=100)
    for i in range(0, 11):
        pool.apply_async(main(i))
    print("mark++++++++++++++++++++++++++++")
    pool.close()
    pool.join()
    end = time.time()
    print("End+++++++++++++++++++++++++++")
    # 耗时1.6秒
    print("Running time %s Seconds" % (end - start))