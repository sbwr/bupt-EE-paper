import os
import sys
#import traceback#调试时使用

import re
from bs4 import BeautifulSoup
import requests


class GetMovieInfo():  
   
    """获取每个电影的主题，url链接以及下载链接""" 
    
    def __init__(self,page=''):
        self.headers = {
            'User-Agent':''
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
            'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'
        }
        self.url = 'https://www.dy2018.com/html/gndy/dyzz/index' + page +'.html'

    def get_root_html(self):
    
        """获取主页面的html代码"""
        
        self.response = requests.get(self.url,headers=self.headers)
        self.response.encoding ='gb2312'#电影网页编码为gb2312
        html = self.response.text
        return html

    def analysis_root_html(self):
    
        """分析主页面的html的代码，获取电影主题以及电影url"""
        
        soup = BeautifulSoup(self.get_root_html(),'lxml-xml')#用lxml解析xml网页，该网页直接用lxml解析不全
        html_part1 = soup.select('ul b a')#标准选择器选择
        for part in html_part1:
            root_url = part['href']
            movie_title = part['title']
            yield {
                'title':movie_title,
                'root_url':root_url
            }

    def get_movie_html(self):
    
        """获取每个电影的html代码"""
        
        for item in self.analysis_root_html():
            root_url = 'https://www.dy2018.com' + item['root_url']
            html = requests.get(root_url)
            html.encoding = 'gb2312'
            html = html.text
            yield html

    def analysis_movie_html(self):
    
        """分析电影页面的html并获取下载链接"""
        
        for item in self.get_movie_html():
            soup = BeautifulSoup(item,'lxml')
            html_part2 = soup.select('td a')
            march = re.compile('',re.S)
            download_url_list = re.findall(march,str(html_part2[0]))
            download_url = download_url_list[0]
            yield {
                'download_url':download_url
            }

    def integration(self):
    
        """将主题，电影url以及下载链接合并为一个字典，并用生成器返回"""
        
        for x,y in zip(self.analysis_root_html(),self.analysis_movie_html()):
            x.update(y)#字典合并
            yield x


class Operation(GetMovieInfo):
    
    """操作、显示以及下载"""
    
    def manu(self):
    
        """下载器菜单显示"""
        
        print('=' * 50)
        print(' ' * 7 + '最新电影下载器v1.0')
        print(' ' * 10 + '1、首页最新电影查询')
        print(' ' * 10 + '2、迅雷下载（推荐大文件下载）')
        print(' ' * 10 + '3、普通下载（推荐小文件下载）')
        print(' ' * 10 + '4、电影详情查询')
        print(' ' * 10 + '5、下一页最新电影列表操作')
        print(' ' * 10 + '6、上一页最新电影列表操作')
        print(' ' * 10 + '7、退出下载器')
        print('=' * 50)

    def search_movie(self):
    
        """获取电影标题，用于电影查询"""
        
        i = 1
        for item in self.integration():
            item['num'] = i
            i += 1
            yield item

    def thunder_download(self,details=None,url=None):
    
        """迅雷下载"""
        
        if details == None:
            download_url = url
        else:
            download_url = details[0].get('download_url')
        os.system(r"D:\软件安装\Program\Thunder.exe -StartType:DesktopIcon %s"%download_url )#################
        return None

    def common_download(self,url):
    
        """普通下载，并显示下载进度条"""
        
        response = requests.get(url)
        file = '{}\{}'.format('C:\\Users\\CUI-sir\\Desktop',url[url.rfind('/')+1:])
        print(file)
        total_size = int(response.headers['Content-Length'])
        temp_size = 0
        with open(file,'wb') as f:
            for chunk in response.iter_content(chunk_size=1024):
                if chunk:
                    temp_size += len(chunk)
                    f.write(chunk)
                    f.flush()
                    q = (temp_size/total_size)*100
                    p = int((temp_size/total_size)*50)
                    sys.stdout.write('█'*p + '%.2f'%q + ' %')
                print('')
            print('下载完成')
    def write_2_file(self):
        pass

    def search_movie_detail(self,num=None):
    
        """电影详情搜索"""
        
        for item in self.search_movie():
            items = []
            if num == item.get('num'):
                movie_url = 'https://www.dy2018.com' + item.get('root_url')
                movie_html = requests.get(movie_url)
                movie_html.encoding = 'gb2312'
                movie_html = movie_html.text
                soup = BeautifulSoup(movie_html,'lxml')
                html_part1 = soup.select('#Zoom p')
                for text in html_part1:
                    detail_infor = text.get_text()
                    items.append(detail_infor)
                return item,items

    def show(self,num=1,details=None):
    
        """各类操作显示"""
        
        if num == 1:
            print('最近更新电影如下：')
            for item in self.search_movie():
                title = item.get('title')
                num = item.get('num')
                print('< ' + str(num) + ' >' + '-----' + title)

        if num == 2:
            print('已转至迅雷下载')

        if num == 3:
            pass

        elif num == 4:
            for item in details[1]:
                print(item)

    def main(self):
    
        """入口方法，用与用户输入操作及控制"""
        
        global i#定义全局变量用于控制页数，避免被初始化
        try:
            self.change_num = int(input('请输入操作序号：'))
            if self.change_num == 1:
                self.search_movie()
                self.show(self.change_num)
                order = input('是否进行电影详情操作[YES/NO]:')
                if order.upper() == 'YES':
                    num = int(input('请输入想要查询的电影序号：'))
                    details = self.search_movie_detail(num)
                    self.show(4,details)
                    order2 = input('是否进行迅雷下载电影[YES/NO]:')
                    if order2.upper() == 'YES':
                        self.thunder_download(details)
                        self.show(2)
                        self.main()
                    else:
                        self.main()
                else:
                    order2 = input('是否直接进行迅雷下载电影[YES/NO]:')
                    if order2.upper() == 'YES':
                        num = int(input('请输入想要直接下载的电影序号：'))
                        details = self.search_movie_detail(num)
                        self.thunder_download(details)
                        self.show(2)
                        self.main()
                    else:
                        self.main()

            elif self.change_num == 2:
                dowload_url = input('请复制下载地址（支持所有格式下载）：')
                self.thunder_download(url=dowload_url)
                self.show(self.change_num)
                self.main()

            elif self.change_num == 3:
                url = input('请输入下载地址（不支持第三方下载链接）：')
                self.common_download(url)
                self.show(self.change_num)
                self.main()

            elif self.change_num == 4:
                self.show(1)
                num = int(input('请输入想要查询的电影序号：'))
                details = self.search_movie_detail(num)
                self.show(self.change_num,details)
                order2 = input('是否进行迅雷下在电影[YES/NO]:')
                if order2.upper() == 'YES':
                    self.thunder_download(details)
                    self.main()
                else:
                    self.main()

            elif self.change_num == 5:
                i +=1
                print('当前页数为第%d'%i)
                page = '_' + str(i)
                a = Operation(page)
                a.main()

            elif self.change_num == 6:
                i -= 1
                print('当前页数为第%d' % i)
                if i == 1:
                    b = Operation()
                    b.main()
                elif i >= 2:
                    page = '_' + str(i)
                    c = Operation(page)
                    c.main()
                elif i<= 0:
                    print('此页是首页无法进行上一页操作!')
                    self.main()
                    i = 1

            elif self.change_num == 7:
                sys.exit()

        except Exception:
            #print(traceback.format_exc())#调试程序时使用，可以显示调试错误信息且不中断程序
            print('请输入正确的操作号！')
            self.main()


if __name__ == '__main__':#执行
    i = 1
    movie = Operation()#实例化
    movie.manu()
    movie.main()