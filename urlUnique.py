import os
import re

resultDir = 'result/unique/'
sourceDir = 'source/'

if __name__ == '__main__':
    if not os.path.exists(resultDir):
        os.makedirs(resultDir)
    if not os.path.exists(sourceDir):
        os.makedirs(sourceDir)

    check_file = open("source/url.txt", 'r')
    ok = open(resultDir + '/okUrls.txt', 'w', encoding='utf-8')

    not_check_urls = check_file.readlines()
    temp = []
    for i in range(len(not_check_urls)):
        item = not_check_urls[i]
        ip = re.findall(r'\d+.\d+.\d+.\d+', item)
        if len(ip) != 0:
            item = item.replace(ip[0], '')
        item = item.strip()
        if item.strip() != '---':
            temp.append(item)

    print('原url数：' + str(len(not_check_urls)))
    print(not_check_urls)

    not_check_urls = list(set(temp))
    print('去重后url数：' + str(len(not_check_urls)))
    print(not_check_urls)

    for item in not_check_urls:
        ok.write(item + '\n')
