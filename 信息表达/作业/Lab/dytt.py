from bs4 import BeautifulSoup 
import  urllib
import  re
url= 'http://www.ygdy8.net/html/gndy/dyzz/index.html'
moive_url_list = []
moive_name_list = []
request = urllib.urlopen(url)
response = request.read()
response = re.UNICODE(response,'GBK').encode('utf-8')
soup = BeautifulSoup(response,'html.parser')
a = soup.find_all('a',class_="ulink")
for  i  in  a:
    moive_open_url = 'http://www.ygdy8.net' + i['href']
    req =  urllib.urlopen(moive_open_url)
    res = req.read()
    try:
        res = re.UNICODE(res,'GBK').encode('utf-8')
    except UnicodeDecodeError:
        continue
so = BeautifulSoup(res,'html.parser')
a_tag = so.find_all('a')
for j in a_tag:
    pattern = re.compile("^ftp://ygdy\d{1}:ygdy\d{1}@y\d{3}.dydytt.net")
string= j['href']
match = pattern.match(string)
if match:
    moive_url_list.append(string)
for m in moive_url_list:
    print (m)