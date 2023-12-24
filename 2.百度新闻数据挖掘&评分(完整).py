# =============================================================================
# 4.4 把数据挖掘到数据存入数据库 by wyt edit by sgteam
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

    # 打印列表长度，用于调试
    print("本次获取结果如下所示：")
    print("标题数量:", len(title))
    print("链接数量:", len(href))
    print("日期数量:", len(date))
    print("来源数量:", len(source))

    # 4.舆情评分版本4及数据深度清洗（参考5.1和5.2和5.3节）
    score = []
    # keywords = ['违约', '诉讼', '兑付', '阿里', '百度', '京东', '互联网']
    keywords = {
        '违约', '诉讼', '兑付', '破产', '财务危机', '裁员', '盈利下滑', '市场萎缩', '产品召回',
        '泄露', '漏洞', '消费者投诉', '处罚', '合规问题',
        '下跌', '评级下降', '债务违约', '经营困难', '市场竞争激烈',
        '故障', '品牌危机', '高管变动', '损失', '市场份额下降',
        '合作关系破裂', '法律纠纷', '经济制裁', '业绩不佳', '顾客满意度下降',
        '延迟交付', '产品缺陷', '股东不满', '内部管理混乱', '员工罢工',
        '环境污染', '不道德行为', '质量问题', '经济衰退', '监管加强',
        '政治风险', '贸易冲突', '竞争对手压力', '消费需求减少', '投资损失',
        '创新失败', '市场预测失误', '供应链中断', '广告争议', '品牌形象受损',
        '负面媒体报道', '社会责任忽视', '员工离职', '客户投诉', '市场策略失败',
        '网络安全威胁', '资金链断裂', '信息泄露', '投资风险增加'
    }
    for i in range(len(title)):
        # 默认分数
        num = 100
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
        for k in keywords:
            if (k in article) or (k in title[i]):
                num -= 5
        score.append(num)
        # 数据深度清洗（参考5.1节）
        company_re = company[0] + '.{0,5}' + company[-1]
        if len(re.findall(company_re, article)) < 1:
            title[i] = ''
            source[i] = ''
            href[i] = ''
            date[i] = ''
            score[i] = ''
    while '' in title:
        title.remove('')
    while '' in href:
        href.remove('')
    while '' in date:
        date.remove('')
    while '' in source:
        source.remove('')
    while '' in score:
        score.remove('')

    # 5.打印清洗后的数据（参考3.1节）
    for i in range(len(title)):
        print(str(i + 1) + '.' + title[i] + '(' + date[i] + ' ' + source[i] + ')')
        print(href[i])
        print(company + '该条新闻的舆情评分为' + str(score[i]))

    driver.quit()
    # 6.将数据存入数据库及数据去重（参考4.4节和5.1节）
    for i in range(len(title)):
        db = pymysql.connect(host='localhost', port=3306, user='root', password='123456', database='pachong', charset='utf8mb4')
        cur = db.cursor()  # 获取会话指针，用来调用SQL语句

        # 6.1 查询数据，为之后的数据去重做准备
        sql_1 = 'SELECT * FROM article WHERE company =%s'
        cur.execute(sql_1, company)
        data_all = cur.fetchall()
        title_all = []
        for j in range(len(data_all)):
            title_all.append(data_all[j][1])

        # 6.2 判断数据是否在原数据库中，不在的话才进行数据存储
        if title[i] not in title_all:
            sql_2 = 'INSERT INTO article(company,title,href,source,date,score) VALUES (%s,%s,%s,%s,%s,%s)'  # 编写SQL语句
            cur.execute(sql_2, (company, title[i], href[i], source[i], date[i], score[i]))  # 执行SQL语句
            db.commit()  # 当改变表结构后，更新数据表的操作
        cur.close()  # 关闭会话指针
        db.close()  # 关闭数据库链接
    print('------------------------------------')  # 分割符

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
# companys = ['华能信托', '阿里巴巴', '百度集团', '腾讯', '京东']
companys = ['哈空调']
for company in companys:
    try:
        baidu(company)
        print(company + '爬取并存入数据库成功')
    except:
        print(company + '爬取并存入数据库失败')

