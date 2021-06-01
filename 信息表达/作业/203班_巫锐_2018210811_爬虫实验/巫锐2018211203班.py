import requests
from bs4 import BeautifulSoup
import re               # 正则表达式库
import pandas as pd

# 获取第1~end页的url
def getAllUrl(end):
    url = []
    end = end+1
    for i in range(1, end):
        url.append("https://www.dytt8.net.cn/index.php/vod/show/id/6/page/"+str(i)+".html")
    return url

# 通过requests库请求获得目标网页的HTML页面内容
def getHTMLText(url):
    try:
        r = requests.get(url, timeout=100)
        r.raise_for_status()                    # 若状态码不是200，引发HTTPError异常
        r.encoding = r.apparent_encoding
        return r.text
    except:
        return "网络请求异常"

# 解析html页面，初始化BS对象
def analyzeHTMLText(text):
    soup = BeautifulSoup(text, "html.parser")   # 解析对象，解析器
    return soup

# 在bs对象内检索电影详情内容，并使用正则表达式去除html标签，最后将获得的电影名、信息存在data.csv中
def getDetail(bs, name, casts, page):
    isdetail = 0                                # 影片标题和演员表交替出现，记录本次的内容是否是演员表
    # bs.select('h4.text-overflow'):            # 组合查找影片标题 标签名.class名 ，之间不能加空格
    for item in bs.select('.text-overflow'):    # 该css类可同时查找出影片标题和演员表
        # print(item)
        regl = re.compile("<[^>]*>")
        item1 = regl.sub('', str(item))         # 用正则表达式删除html标签，提取出有效内容
        # 将电影标题保存至 name
        if isdetail==0:
            name.append(item1)
            isdetail = 1
        # 将电影信息保存至 detail
        else:
            casts.append(item1)
            isdetail = 0
    # css类->属性组合查找获取链接html标签，并使用.get()获取链接纯文本
    for item in bs.select(".stui-vodlist__box > a"):
        link = item.get('href') 
        # 分析获取到的链接和详情页url的对应关系，拼接字符串获得详情页完整url
        detail_url = "https://www.dytt8.net.cn/index.php/vod/" + link[15:]
        # print(detail_url)
        getDescription(detail_url, detail)
        
def getDescription(url, detail):
    text = getHTMLText(url)
    # print(text)
    bs = analyzeHTMLText(text)
    for item in bs.select(".desc"):
        regl = re.compile("<[^>]*>")
        item = regl.sub('', str(item)) 
        # print(item)
        detail.append(item)

# 使用pandas库保存获取的内容到工作目录下的data.csv
def saveContents(name, casts, detail):
    df = pd.DataFrame({'title':name,'casts':casts,'description':detail})
    df.to_csv("data.csv", encoding="gb18030")   # encoding gbk, gb2312均报错，又win10不支持UTF-8，所以只有这个了



if __name__ == "__main__":
    pages_num = 50                             # 设置爬取的页数
    url = getAllUrl(pages_num)                  # 获取需要页的url，保存在列表里
    name = []                                   # 使用列表保存电影名称
    casts = []                                  # 使用列表保存电影详细信息
    detail = []
    
    for i in range(0, pages_num):               # 循环爬取至末页
        text = getHTMLText(url[i])              # 获取一页的全部html文本
        bs = analyzeHTMLText(text)              # 使用beautifulsoup解析文本
        getDetail(bs, name, casts, i+1)         # 获取文本中所需内容（电影标题、演员表）
    saveContents(name, casts, detail)           # 保存获取的内容