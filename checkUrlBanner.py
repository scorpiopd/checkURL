import time

import requests
import threading
import os

from bs4 import BeautifulSoup

now = time.strftime("%Y-%m-%d==%H-%M-%S", time.localtime())
resultDir = 'result/banner/' + now
sourceDir = 'source/'
# is_append_http_prefix = False
timeout = 7
threads_count = 20
thread_urls_count = 0
yu = 0


def send(url_line):
    url = check_url_is_valid(url_line)

    try:
        print('url>>>' + url)
        headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Cache-Control': 'max-age=0',
            'DNT': '1',
            'Proxy-Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36'
        }
        # r = requests.get(url, allow_redirects=True, timeout=timeout, headers=headers)  # 去除ssl验证
        r = requests.get(url, allow_redirects=True)  # 去除ssl验证
        print(r.url)
        # r.encoding = 'utf8'
        # r = requests.get(url, verify=False, allow_redirects=True, timeout=3)
        print('status_code>>>' + str(r.status_code))

        if r.status_code != 200:
            # print('fail1')
            fail.write(url + '\n')
        else:
            # print(r.text)
            bs = BeautifulSoup(r.text, 'html.parser')
            # print(bs.contents)
            content_type = bs.find(attrs={"http-equiv": "Content-Type"})
            if content_type is not None:
                content_type = content_type['content']
                charset = content_type[content_type.find('charset') + 8:]
                if charset != 'utf8':
                    r.encoding = charset
                    bs = BeautifulSoup(r.text, 'html.parser')
            title = bs.title
            if title is not None:
                title = title.text
                if title == '':
                    title = '无名或解析失败'
                    error.write(url + '                ' + title + '\n')
                else:
                    ok.write(url + '                ' + title + '\n')
            else:
                title = '无名或解析失败'
                error.write(url + '                ' + title + '\n')
            print(title)
    except Exception as e:
        print(e)
        print('fail2')
        fail.write(url + '\n')


# 具体做啥事,写在函数中
def run(number):
    print('线程：' + str(number))
    thread_start = number * thread_urls_count
    if number + 1 == threads_count:
        thread_end = thread_start + thread_urls_count + yu
    else:
        thread_end = thread_start + thread_urls_count

    print('线程开始：' + str(thread_start))
    print('线程结束：' + str(thread_end))
    # print(not_check_urls[int(thread_start):int(thread_end)])
    wait_check_urls = not_check_urls[int(thread_start):int(thread_end)]
    for url_line in wait_check_urls:
        send(url_line)


# 处理url
def check_url_is_valid(url):
    url = url.strip()
    if url.endswith('\''):
        url = url[:-1]
    if url.startswith('\''):
        url = url[1:]
    if url.endswith('"'):
        url = url[:-1]
    if url.startswith('"'):
        url = url[1:]
    if url.find('http') != -1:
        return url
    else:
        return 'http://' + url


if __name__ == '__main__':
    if not os.path.exists(resultDir):
        os.makedirs(resultDir)
    if not os.path.exists(sourceDir):
        os.makedirs(sourceDir)

    check_file = open("source/url.txt", 'r')
    ok = open(resultDir + '/okUrls.txt', 'w', encoding='utf-8')
    fail = open(resultDir + '/failUrls.txt', 'w', encoding='utf-8')
    error = open(resultDir + '/errorUrls.txt', 'w', encoding='utf-8')

    not_check_urls = check_file.readlines()
    not_check_urls_len = len(not_check_urls)
    print('总检测url数：' + str(not_check_urls_len))

    if not_check_urls_len > 30:
        yu = not_check_urls_len % threads_count
        thread_urls_count = (not_check_urls_len - yu) / threads_count
        print('每个线程要检测的url数量：' + str(thread_urls_count))
        print('余：' + str(yu))

        for i in range(threads_count):
            # 注意这,开始咯,指明具体的方法和方法需要的参数
            my_thread = threading.Thread(target=run, args=(i,))
            # 一定不要忘记
            my_thread.start()
    else:
        for url_line in not_check_urls:
            send(url_line)
