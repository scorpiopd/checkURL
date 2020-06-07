import time

import requests
import threading
import os

from bs4 import BeautifulSoup

now = time.strftime("%Y-%m-%d==%H-%M-%S", time.localtime())
resultDir = 'result/' + now
sourceDir = 'source/'
is_append_http_prefix = False
timeout = 5
threads_count = 20
thread_urls_count = 0
yu = 0


def send(url_line):
    url = check_url_is_valid(url_line)

    try:
        print('url>>>' + url)
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:77.0) Gecko/20100101 Firefox/77.0',
        }
        r = requests.get(url, allow_redirects=True, timeout=timeout, headers=headers)  # 去除ssl验证
        # r = requests.get(url, verify=False, allow_redirects=True, timeout=3)
        print('status_code>>>' + str(r.status_code))

        if r.status_code != 200:
            # print('fail1')
            fail.write(('http://' if is_append_http_prefix else '') + url + '\n')
        else:
            bs = BeautifulSoup(r.text, 'html.parser')
            http_equiv = bs.find(attrs={"http-equiv": "refresh"})
            if http_equiv is not None:
                content = http_equiv['content']
                url_word_index = 0
                if content.find('url') != -1:
                    url_word_index = content.find('url')
                else:
                    url_word_index = content.find('URL')
                refresh_url = content[url_word_index + 4:]
                print('content:' + content)
                print('refresh_url:' + refresh_url)
                if refresh_url.find('http') != -1:
                    send(refresh_url)
                else:
                    send(url + '/' + refresh_url)
            else:
                # print('ok')
                ok.write(('http://' if is_append_http_prefix else '') + url + '\n')
    except:
        # print('fail2')
        fail.write(('http://' if is_append_http_prefix else '') + url + '\n')


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
