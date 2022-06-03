# av_category.py 的爬蟲模組
# 作者：scbmark
# 日期：2021/06/01
# 版本：2.0(python 3.10.4)
# 更動：新增 msin 和 msin_fc2

from bs4 import BeautifulSoup
from requests import get,post
import json

class avfile():
    def __init__(self, num, address, title, imglink):
        self.num = num
        self.address = address
        self.title = title
        self.imglink = imglink
    def dump_in_json(self):
        with open('avinfo.json',mode='r',encoding='utf-8') as file:
            temp=json.load(file)
        temp[f'{self.num}']={'num':self.num, 'address':self.address, 'title':self.title, 'imglink':self.imglink}
        with open('avinfo.json',mode='w',encoding='utf-8') as file:
            json.dump(temp, file)
    def print_contents(self):
        print(self.num, self.address, self.title, self.imglink)
    
    def save_img(self, download_path):
        headers={
        "User-Agent":"Mozilla/5.0 (X11; Linux x86_64; rv:91.0) Gecko/20100101 Firefox/91.0"
        }
        img=get(self.imglink,headers=headers)
        imgnam=download_path+self.num+".jpg"
        with open(imgnam,"wb") as file:
            file.write(img.content)
            print('---下載完成！')

def get_htmlfile_avwiki(data):
    url='https://av-wiki.net/'+str(data)+'/'
    headers={
        "User-Agent":"Mozilla/5.0 (X11; Linux x86_64; rv:100.0) Gecko/20100101 Firefox/100.0"
    }
    # 取得html檔
    try:
        root=get(url,headers=headers)
        htmlfile=BeautifulSoup(root.text,'html.parser')
    except:
        print("無法取得資料")
        htmlfile=[]
    return htmlfile

def get_info_avwiki(htmlfile):
    try:
        imglink=htmlfile.find("img", {"loading":"lazy"})['src']
        num=str(htmlfile.find("span", {'class':'entry-subtitle'}).string.split(' ')[-1])
        address=htmlfile.find("ul",{'class':"post-meta clearfix"}).find_all('a',{'rel':'tag'})
        for i in range(0,len(address)):
            address[i]=address[i].text
        separator=' '
        address=separator.join(address)
        title=htmlfile.find("img", {"loading":"lazy"})['alt']
        avinfo = avfile(num, address, title, imglink)
    except:
        avinfo = None
    return avinfo

def get_htmlfile_airav(data):
    url='https://jp.airav.wiki/video/'+str(data)+'?lng=jp'
    headers={
        "User-Agent":"Mozilla/5.0 (X11; Linux x86_64; rv:100.0) Gecko/20100101 Firefox/100.0"
    }
    # 取得html檔
    try:
        root=get(url,headers=headers)
        htmlfile=BeautifulSoup(root.text,'html.parser')
    except:
        print("無法取得資料")
        htmlfile=[]
    return htmlfile

def get_info_airav(htmlfile):
    try:
        imglink=htmlfile.find("meta", {"property":"og:image"})['content']
        num=htmlfile.find("h5", {'class':'d-none d-md-block text-primary mb-3'}).string
        address=htmlfile.find_all("li", {'class':"videoAvstarListItem"})
        for i in range(0,len(address)):
            address[i]=address[i].text
        separator=' '
        address=separator.join(address)
        title=htmlfile.find("h5", {"class":"d-none d-md-block"}).string
        avinfo = avfile(num, address, title, imglink)
    except:
        avinfo = None
    return avinfo

def get_htmlfile_av01(data):
    data={"sn":f'{data}'}
    url="https://www.jav321.com/search"
    headers={
        "User-Agent":"Mozilla/5.0 (X11; Linux x86_64; rv:100.0) Gecko/20100101 Firefox/100.0"
    }
    # 取得html檔
    try:
        root=post(url,headers=headers,data=data)
        htmlfile=BeautifulSoup(root.text,'html.parser')
    except:
        print("無法取得資料")
        htmlfile=[]  
    return htmlfile

def get_info_av01(htmlfile):
    try:
        imglink=htmlfile.find("div", {"class":"col-xs-12 col-md-12"}).find("img",{"class":"img-responsive"})['src']
        num=htmlfile.find("h3").small.string.split(' ')[0].upper()
        address=htmlfile.find("h3").small.string.split(' ')[1:]
        separator=' '
        address=separator.join(address)
        title=htmlfile.find("h3").getText().strip(htmlfile.find("h3").small.string)
        avinfo = avfile(num, address, title, imglink)
    except:
        avinfo = None
    return avinfo

def get_htmlfile_msin(data):
    url='https://db.msin.jp/jp.search/movie?str='+str(data)
    headers={
        "Cookie":"age=off",
        "User-Agent":"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.61 Safari/537.36" 
    }
    # 取得html檔
    try:
        url=get(url, headers = headers).url
        root=get(url, headers = headers)
        htmlfile=BeautifulSoup(root.text,'html.parser')
    except:
        print("無法取得資料")
        htmlfile=[]
    return htmlfile

def get_info_msin(htmlfile):
    try:
        imglink=htmlfile.find("img", {"class":"movie_img"})['src']
        num=htmlfile.find("div", {'class':'mv_fileName'}).string
        address=htmlfile.find("div", {'class':"mv_artist"}).find_all("a")
        for i in range(0,len(address)):
            address[i]=address[i].text
        separator=' '
        address=separator.join(address)
        title=htmlfile.find("div", {"class":"mv_title"}).string
        avinfo = avfile(num, address, title, imglink)
    except:
        avinfo = None
    return avinfo

def get_htmlfile_msin_fc2(data):
    url='https://db.msin.jp/search/movie?str='+str(data)
    headers={
        "Cookie":"age=off",
        "User-Agent":"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.61 Safari/537.36" 
    }
    # 取得html檔
    try:
        url=get(url, headers = headers).url
        root=get(url, headers = headers)
        # print(root.cookies)
        # for key, value in root.cookies.items():
        #     print(key + '=' + value)
        htmlfile=BeautifulSoup(root.text,'html.parser')
    except:
        print("無法取得資料")
        htmlfile=[]
    return htmlfile

def get_info_msin_fc2(htmlfile):
    try:
        imglink='https://db.msin.jp'+htmlfile.find("img", {"class":"movie_img"})['src'][2:]
        num=htmlfile.find("div", {'class':'mv_fileName'}).string
        address=htmlfile.find("div", {'class':"mv_artist"}).find("a").string
        # for i in range(0,len(address)):
        #     address[i]=address[i].text
        # separator=' '
        # address=separator.join(address)
        title=htmlfile.find("div", {"class":"mv_title"}).find("span").string
        avinfo = avfile(num, address, title, imglink)
    except:
        avinfo = None
    return avinfo

def save_img(avinfo, download_path):
    headers={
        "User-Agent":"Mozilla/5.0 (X11; Linux x86_64; rv:91.0) Gecko/20100101 Firefox/91.0"
    }
    img=get(avinfo['imglink'],headers=headers)
    imgnam=download_path+avinfo['num']+".jpg"
    with open(imgnam,"wb") as file:
        file.write(img.content)
        print('---下載完成！')
    file.close()

def crawler_switcher(data):
    for method in range(1,7):
        match method:
            case 1:
                print('avwiki')
                try:
                    htmlfile=get_htmlfile_avwiki(data)
                    avinfo=get_info_avwiki(htmlfile)

                    if avinfo!={}:
                        return avinfo
                except:
                    continue   
            case 2:
                print('airav')
                try:
                    htmlfile=get_htmlfile_airav(data)
                    avinfo=get_info_airav(htmlfile)

                    if avinfo!={}:
                        return avinfo
                except:
                    continue   
            case 3:
                print('av01')
                try:
                    htmlfile=get_htmlfile_av01(data)
                    avinfo=get_info_av01(htmlfile)

                    if avinfo!={}:
                        return avinfo
                except:
                    continue
            case 4:
                print('msin')
                try:
                    htmlfile=get_htmlfile_msin(data)
                    avinfo=get_info_msin(htmlfile)

                    if avinfo!={}:
                        return avinfo
                except:
                    continue
            case 5:
                print('msin-fc2')
                try:
                    htmlfile=get_htmlfile_msin_fc2(data)
                    avinfo=get_info_msin_fc2(htmlfile)

                    if avinfo!={}:
                        return avinfo
                except:
                    continue
            case _:
                avinfo={}
                return avinfo
