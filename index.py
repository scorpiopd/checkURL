import requests
import threading
import os

resultDir = 'result'
sourceDir = 'source'
if not os.path.exists(resultDir):
    os.makedirs(resultDir)
if not os.path.exists(sourceDir):
    os.makedirs(sourceDir)

check_file = open("source/url.txt", 'r')
ok = open('result/okUrls.txt', 'w', encoding='utf-8')
fail = open('result/failUrls.txt', 'w', encoding='utf-8')

not_check_urls = check_file.readlines()
not_check_urls_len = len(not_check_urls)
print('总检测url数：' + str(not_check_urls_len))

is_append_http_prefix = True


def check(wait_check_urls):
    for url_line in wait_check_urls:
        try:
            url = 'http://' + url_line.strip()
            print('url>>>' + url)
            r = requests.get(url, allow_redirects=True, timeout=3)  # 去除ssl验证
            # r = requests.get(url, verify=False, allow_redirects=True, timeout=3)
            print('status_code>>>' + str(r.status_code))
            if r.status_code != 200:
                fail.write(('http://' if is_append_http_prefix else '') + url_line)
            else:
                ok.write(('http://' if is_append_http_prefix else '') + url_line)
        except:
            fail.write(('http://' if is_append_http_prefix else '') + url_line)


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
    check(not_check_urls[int(thread_start):int(thread_end)])


threads_count = 20
thread_urls_count = 0
yu = 0
if not_check_urls_len > 10:
    yu = not_check_urls_len % threads_count
    thread_urls_count = (not_check_urls_len - yu) / threads_count
    print('每个线程要检测的url数量：' + str(thread_urls_count))
    print('余：' + str(yu))
else:
    check(not_check_urls)

for i in range(threads_count):
    # 注意这,开始咯,指明具体的方法和方法需要的参数
    my_thread = threading.Thread(target=run, args=(i,))
    # 一定不要忘记
    my_thread.start()
