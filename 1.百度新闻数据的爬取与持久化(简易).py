# =============================================================================
# 4.4 把数据挖掘到数据存入数据库 by wyt
# =============================================================================

from selenium import webdriver
import time
import re
import pymysql

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
    'DNT': '1',  # Do Not Track
    'Connection': 'keep-alive'
}


def baidu(company):

    options = webdriver.ChromeOptions()
    options.binary_location = 'D:/Software/InternetAPP/chrome-win64/chrome.exe'
    driver = webdriver.Chrome(options=options)
    driver.get('https://www.baidu.com/s?rtt=4&bsst=1&cl=2&tn=news&word=' + company)
    time.sleep(1)
    # 滚动到页面底部以加载更多结果
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(1)  # 等待额外内容加载
    # 现在获取页面的HTML
    res = driver.page_source

    p_info = '<p class="c-author">(.*?)</p>'
    info = re.findall(p_info, res, re.S)
    # p_href = '<h3 class="c-title">.*?<a href="(.*?)"'
    p_href = '<h3 class="news-title_1YtI1 .*?"><a href="(.*?)"'
    href = re.findall(p_href, res, re.S)
    # p_title = '<h3 class="c-title">.*?>(.*?)</a>'
    p_title = '<h3 class="news-title_1YtI1 .*?">.*?>(.*?)</a></h3>'
    title = re.findall(p_title, res, re.S)
    p_source = '<span class="c-color-gray" aria-label="新闻来源：(.*?)">'
    source = re.findall(p_source, res, re.S)
    p_date = '<span class="c-color-gray2 c-font-normal c-gap-right-xsmall" aria-label=".*?">(.*?)</span>'
    date_matches = re.findall(p_date, res, re.S)

    # 确保date列表和title列表长度相同
    while len(date_matches) < len(title):
        date_matches.append("无日期")

    # 为每个标题分配日期
    date = []
    for i in range(len(title)):
        date.append(date_matches[i].strip() if i < len(date_matches) else "无日期")

    for i in range(len(title)):
        title[i] = title[i].strip()
        title[i] = re.sub('<.*?>', '', title[i])
    for i in range(len(title)):
        try:
            driver.get(href[i])
            time.sleep(0.5)
            # 滚动到页面底部以加载更多结果
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            # 现在获取页面的HTML
            article = driver.page_source
            time.sleep(0.5)
            # 在这里获取文章的日期
            article_date = format_date(article)  # 直接在页面源代码中查找并格式化日期
            date[i] = article_date  # 更新日期列表
        except:
            article = '爬取失败'
            date[i] = "无日期"  # 如果爬取失败，则设为“无日期”
        try:
            article = article.encode('ISO-8859-1').decode('utf-8')
        except:
            try:
                article = article.encode('ISO-8859-1').decode('gbk')
            except:
                article = article
        p_article = '<p>(.*?)</p>'
        article_main = re.findall(p_article, article)  # 获取<p>标签里的正文信息
        article = ''.join(article_main)  # 将列表转换成为字符串
        # 数据深度清洗（参考5.1节）
        company_re = company[0] + '.{0,5}' + company[-1]
        if len(re.findall(company_re, article)) < 1:
            title[i] = ''
            source[i] = ''
            href[i] = ''
            date[i] = ''
    while '' in title:
        title.remove('')
    while '' in href:
        href.remove('')
    while '' in date:
        date.remove('')
    while '' in source:
        source.remove('')

    # 打印列表长度，用于调试
    print("本次获取结果如下所示：")
    print("标题数量:", len(title))
    print("链接数量:", len(href))
    print("日期数量:", len(date))
    print("来源数量:", len(source))
    driver.quit()

    # 将数据存入数据库 没有去重
    for i in range(len(title)):
        db = pymysql.connect(host='localhost', port=3306, user='root', password='123456', database='pachong', charset='utf8mb4')
        cur = db.cursor()
        sql = 'INSERT INTO article(company,title,href,source,date) VALUES (%s,%s,%s,%s,%s)'
        cur.execute(sql, (company, title[i], href[i], source[i], date[i]))
        db.commit()
        cur.close()
        db.close()

print('数据爬取并存入数据库成功')

def format_date(date_str):
    # 尝试匹配格式 yyyy-MM-dd HH:mm 或 yyyy年MM月dd日 HH:mm
    match = re.search(r'(\d{4})(-|年)(\d{2})(-|月)(\d{2})日? (\d{2}:\d{2})', date_str)
    if match:
        # 格式化日期为 yyyy-MM-dd HH:mm
        year, month, day, hour_min = match.group(1), match.group(3), match.group(5), match.group(6)
        return f"{year}-{month}-{day} {hour_min}"
    return "无日期"  # 如果没有匹配到日期，返回“无日期”


# 如果想批量爬取并存入数据库，可以采用如下代码：
companys = ['华能信托', '阿里巴巴', '百度集团', '腾讯', '京东']
for company in companys:
    try:
        baidu(company)
        print(company + '爬取并存入数据库成功')
    except:
        print(company + '爬取并存入数据库失败')

