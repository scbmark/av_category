#!/home/scbmark/anaconda3/envs/web/bin/python3.10
# 爬取AV的資訊/下載封面/分類資料夾中的AV檔案
# 作者：scbmark
# 日期：2021/06/03
# 版本：1.0(python 3.10.4)
# 更動：使用 OOP 
# TODO 更新 get_num 的演算法
import sys
import os
import glob
import json
from pathlib import Path
from shutil import move
import web_crawler_oop

class working_path():
    def __init__(self, path):
        self.path_name = str(path) + '/'
    def get_jpg_file(self):
        self.jpg_file=glob.glob('*.jpg')
    def get_mp4_file(self):
        self.mp4_file=glob.glob('*.mp4')
    def get_jpg_num(self):
        self.jpg_num=[]
        for jpg in self.jpg_file:
            num=Path(jpg).stem.upper()
            if num.endswith('C' or 'c')==True:
                num=num[0:-2]
        self.jpg_num.append(num)
    def get_mp4_num(self):
        self.mp4_num=[]
        for mp4 in self.mp4_file:
            num=Path(mp4).stem.upper()
            if num.endswith('C' or 'c')==True:
                num=num[0:-2]
            self.mp4_num.append(num)
    def compare_num(self):
        self.need_to_fix=[]
        for mp4 in self.mp4_num:
            if self.jpg_num.count(mp4)==0:
                self.need_to_fix.append(mp4)

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
    
    def save_img(self):
        headers={
        "User-Agent":"Mozilla/5.0 (X11; Linux x86_64; rv:91.0) Gecko/20100101 Firefox/91.0"
        }
        img=get(avinfo.imglink,headers=headers)
        imgnam=download_path+avinfo.num+".jpg"
        with open(imgnam,"wb") as file:
            file.write(img.content)
            print('---下載完成！')

def file_catgory(jpg_list, mp4_list):
    with open('avinfo.json',mode='r',encoding='utf-8') as json_file:
        movfile=json.load(json_file)
    filetype=('*.jpg', '*.mp4')
    total_lists=jpg_list + mp4_list
    unknown=[]

    for file in total_lists:
        oldName = Path(file).name
        newName = Path(file).stem.upper() + Path(file).suffix
        os.rename(oldName,newName)
        file=newName
        num=Path(file).stem
        if num.endswith('C' or 'c')==True:
            num=num[0:-2]

        if num in movfile:
            address_name=movfile[f'{num}']['address']
            if address_name!='':
                if os.path.exists(address_name)==False:
                    os.makedirs(address_name)
                move(fr'{file}', fr'{address_name}/{file}')
                print(f'{file}--移動完成')
            else:
                if os.path.exists('002 undefine')==False:
                    os.makedirs('002 undefine')
                move(fr'{file}', fr'002 undefine/{file}')
                print(f'{file}--移動完成')
        else:
            if num.startswith('FC2' or 'fc2')==True:
                if os.path.exists('001 FC2')==False:
                    os.makedirs('001 FC2')
                move(fr'{file}', fr'001 FC2/{file}')
                print(f'{file}--移動完成')
            else:
                print(f'{file}--查無本地資料')
                unknown.append(num)
    print('--------------------')
    print('分類完成')
    return unknown

def print_info(avinfo):
    print('----影片資訊')
    print('番號：'+avinfo['num'])
    print('女優：'+avinfo['address'])
    print('標題：'+avinfo['title'])
    print('----')

while True:
    mode=input('1.執行程式 q.關閉程式')
    match mode:
        case '1':
            work_path = working_path(Path.cwd())
            work_path.get_mp4_file()
            work_path.get_jpg_file()
            work_path.get_jpg_num()
            work_path.get_mp4_num()
            work_path.compare_num()
            if work_path.need_to_fix!=[]:
                print('-以下圖片將補齊\n', work_path.need_to_fix)
                for ele in work_path.need_to_fix:
                    print(f'--嘗試下載{ele}的圖片...')
                    avinfo=web_crawler_oop.crawler_switcher(ele)
                    if avinfo!=None:
                        avinfo.dump_in_json()
                        avinfo.save_img(work_path.path_name)
                        avinfo.print_contents()
                    else:
                        print('無此番號資料')
            while True:
                is_category=input('是否進行分類\n(y=1 n=2)')
                match is_category:
                    case '1':
                        work_path.get_jpg_file()
                        work_path.get_mp4_file()
                        unknown=file_catgory(work_path.jpg_file, work_path.mp4_file)
                        print('尚有以下未分類\n', unknown)
                        for ele in unknown:
                            print(f'嘗試下載{ele}的資料...')
                            avinfo=web_crawler_oop.crawler_switcher(ele)
                            if avinfo!=None:
                                avinfo.dump_in_json()
                                avinfo.print_contents()
                            else:
                                print('無此番號資料')
                        unknown=file_catgory(work_path.jpg_file, work_path.mp4_file)
                    case '2':
                        os.system('clear')
                        sys.exit("程式結束")
                    case _:
                        print('輸入錯誤')
        
        case 'q':
            os.system('clear')
            sys.exit("程式結束")
        
        case _:
            print('輸入錯誤')
                    
