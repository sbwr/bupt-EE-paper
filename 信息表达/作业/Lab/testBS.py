import requests
from bs4 import BeautifulSoup
import re               # 正则表达式库
import csv
import codecs

def getAllUrl(end):     # 获取第1~end页的url
    url = []
    end = end+1
    for i in range(1, end):
        url.append("https://www.dytt8.net.cn/index.php/vod/show/id/6/page/"+str(i)+".html")
    return url

def getHTMLText(url):   # 通过requests请求获得目标网页的HTML页面内容
    try:
        r = requests.get(url, timeout=100)
        r.raise_for_status() # 若状态码不是200，引发HTTPError异常
        r.encoding = r.apparent_encoding
        return r.text
    except:
        return "网络请求异常"

def analyze(text):      # 解析html页面，初始化BS对象
    soup = BeautifulSoup(text, "html.parser") # 解析对象，解析器
    return soup

def getDetails(bs):     # 在bs对象内检索电影详情内容，并使用正则表达式去除html标签
    # 1. 创建文件对象
    # f = open('data.csv','a',encoding='utf-8',newline='')
    f = codecs.open('data.csv','w','gbk')
    # 2. 基于文件对象构建 csv写入对象
    # fieldnames = ['name','cast']
    csv_writer = csv.writer(f)
    i = 0
    # for item in bs.select('.stui-vodlist__detail'):
        # print("第"+str(i)+"页演员表")
        # print(item)
    # 取得电影名
    for item in bs.select('h4.text-overflow'):  # 组合查找 标签名.class名 ，之间不能加空格
        # print("第"+str(i)+"页演员表")
        # print(str(item))
        regl = re.compile("<[^>]*>")
        item1 = regl.sub('', str(item))
        # print(item1)
    # print(name)
    # 4. 写入csv文件内容
        # print(item1.splitlines())
        csv_writer.writerow(item1.splitlines())
    # 5. 关闭文件
    f.close()


if __name__ == "__main__":
    end = 3
    url = getAllUrl(end)      # 获取需要页的url，保存在列表里
    
    # 1. 创建文件对象
    f = open('data.csv','a',encoding='utf-8',newline='')
    # 2. 基于文件对象构建 csv写入对象
    csv_writer = csv.writer(f)
    # 3. 构建表头
    csv_writer.writerow(["name","cast"])
    for i in range(0, end):
        text = getHTMLText(url[i])
        bs = analyze(text)
        getDetails(bs)
