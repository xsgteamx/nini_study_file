# =============================================================================
# 教学文件1.百度新闻的爬取
# =============================================================================

import requests
import re
import time

def baidu(page):
    num = (page - 1) * 10
    url = f'https://www.baidu.com/s?rtt=4&bsst=1&cl=2&tn=news&word=广州商学院&pn={num}'

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:87.0) Gecko/20100101 Firefox/87.0'
    }

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # 检查请求是否成功
        content = response.text
        # 解析数据
        p_href = '<h3 class="news-title_1YtI1"><a href="(.*?)"'
        href = re.findall(p_href, content, re.S)
        print(href)

        p_title = '<h3 class="news-title_1YtI1">.*?>(.*?)<!--/s-text--></a></h3>'
        title = re.findall(p_title, content, re.S)
        print(title)

        p_source = '<span class="c-color-gray c-font-normal c-gap-right">(.*?)</span>'
        source = re.findall(p_source, content, re.S)
        print(source)

        p_date = '<span class="c-color-gray2 c-font-normal">(.*?)</span>'
        date = re.findall(p_date, content, re.S)
        print(date)

        for i in range(len(title)):
            title[i] = title[i].strip()
            title[i] = re.sub('<.*?>', '', title[i])
            print(str(i + 1) + '.' + title[i] + '(' + date[i] + '-' + source[i] + ')')
            print(href[i])
    except requests.RequestException as e:
        print(f"请求错误: {e}")
    file1 = open('B:\\Desktop\\1.txt', 'a', encoding='utf-8')  # 如果把a改成w的话，则每次生成txt的时候都会把原来的txt清空
    file1.write('sgteam' + '数据挖掘completed！' + '\n' + '\n')
    for i in range(len(title)):
        file1.write(str(i + 1) + '.' + title[i] + '(' + date[i] + '-' + source[i] + ')' + '\n')
        file1.write(href[i] + '\n')  # '\n'表示换行
    file1.write('——————————————————————————————' + '\n' + '\n')
    file1.close()
    time.sleep(1)  # 每次请求后暂停1秒

for i in range(14):  # i是从0开始的序号，所以下面要写i+1，这里一共爬取了14页
    baidu(i+1)
    print('第' + str(i+1) + '页爬取成功')
