#!/home/scbmark/anaconda3/envs/web/bin/python3.10
# 爬取AV的資訊/下載封面/分類資料夾中的AV檔案
# 作者：scbmark
# 日期：2021/06/01
# 版本：4.0(python 3.10.4)
# 更動：使用 json 作為新的資料庫、把 web 相關的函式分離成模組

import sys
import os
import glob
import json
from pathlib import Path
from shutil import move
import web_crawler

def set_path():
    set_path_ctr=0

    while set_path_ctr==0:
        current_dir=str(Path.cwd())+'/'
        print(f"當前路徑：\n{current_dir}")
        chgdir_ctrl=input('是否更改路徑：\n(y=1,n=2)')
        if int(chgdir_ctrl)==1:
            from tkinter import Tk
            from tkinter import filedialog as fd
            root = Tk()
            root.withdraw()
            root.directory = fd.askdirectory(initialdir = Path.home())
            download_path=root.directory+'/'
            os.chdir(download_path)
            print (f"新的路徑：\n{download_path}")
            set_path_ctr=1

        elif int(chgdir_ctrl)==2:
            download_path=current_dir
            os.chdir(download_path)
            set_path_ctr=1
        else:
            print('輸入錯誤')
    return download_path

def get_filelists():
    type_jpg=('*.jpg')
    j_lists=[]
    j_lists.extend(glob.glob(type_jpg))

    type_mp4=('*.mp4')
    m_lists=[]
    m_lists.extend(glob.glob(type_mp4))

    file_lists=[j_lists,m_lists]
    return file_lists

def get_num(file_lists):
    j_lists=file_lists[0]
    m_lists=file_lists[1]
    jpg_num_lists=[]
    mp4_num_lists=[]

    for jpg in j_lists:
        num=str(Path(jpg).stem.upper())
        if num.endswith('C' or 'c')==True:
            num=num[0:-2]
        jpg_num_lists.append(num)

    for mp4 in m_lists:
        num=str(Path(mp4).stem.upper())
        if num.endswith('C' or 'c')==True:
            num=num[0:-2]
        mp4_num_lists.append(num)

    num_lists=[jpg_num_lists,mp4_num_lists]
    return num_lists

def compare_jpg_mp4(num_lists):
    need_to_fix=[]
    jpg_num_lists=num_lists[0]
    mp4_num_lists=num_lists[1]

    for mp4 in mp4_num_lists:
        if jpg_num_lists.count(mp4)==0:
            need_to_fix.append(mp4)

    return need_to_fix

def file_catgory(file_lists):
    with open('/home/scbmark/av_data_capture/avinfo.json',mode='r',encoding='utf-8') as file:
        movfile=json.load(file)
    filetype=('*.jpg', '*.mp4')
    total_lists=file_lists[0]+file_lists[1]
    unknown=[]
    #print(total_lists)
    print('-'*20)

    for list in total_lists:
        oldName = Path(list).name
        newName = Path(list).stem.upper() + Path(list).suffix
        os.rename(oldName,newName)
        list=newName
        num=Path(list).stem
        if num.endswith('C' or 'c')==True:
            num=num[0:-2]

        if num in movfile:
            address_name=movfile[f'{num}']['address']
            if address_name!='':
                if os.path.exists(address_name)==False:
                    os.makedirs(address_name)
                move(fr'{list}', fr'{address_name}/{list}')
                print(f'{list}--移動完成')
            else:
                if os.path.exists('002 undefine')==False:
                    os.makedirs('002 undefine')
                move(fr'{list}', fr'002 undefine/{list}')
                print(f'{list}--移動完成')
        else:
            if num.startswith('FC2' or 'fc2')==True:
                if os.path.exists('001 FC2')==False:
                    os.makedirs('001 FC2')
                move(fr'{list}', fr'001 FC2/{list}')
                print(f'{list}--移動完成')
            else:
                print(f'{list}--查無本地資料')
                unknown.append(num)
    print('--------------------')
    print('分類完成')
    return unknown

def save_info(avinfo):
    with open('/home/scbmark/av_data_capture/avinfo.json',mode='r',encoding='utf-8') as file:
        movfile=json.load(file)
    movfile[f'{avinfo["num"]}']=avinfo
    with open('/home/scbmark/av_data_capture/avinfo.json',mode='w',encoding='utf-8') as file:
        json.dump(movfile,file)

def print_info(avinfo):
    print('----影片資訊')
    print('番號：'+avinfo['num'])
    print('女優：'+avinfo['address'])
    print('標題：'+avinfo['title'])
    print('----')

while True:
    mode=input('主選單：\n(1.執行程式 q.關閉程式)')
    if mode=='1':
        download_path=set_path()
        file_lists=get_filelists()
        num_lists=get_num(file_lists)
        need_to_fix=compare_jpg_mp4(num_lists)
        if need_to_fix!=[]:
            print('-以下圖片將補齊\n', need_to_fix)
            for ele in need_to_fix:
                print(f'--嘗試下載{ele}的圖片...')
                avinfo=web_crawler.crawler_switcher(ele)
                if avinfo!={}:
                    save_info(avinfo)
                    web_crawler.save_img(avinfo, download_path)
                    print_info(avinfo)
                else:
                    print('無此番號資料')
        is_catgory=input('是否進行分類\n(y=1 n=2)')
        if is_catgory=='1':
            file_lists=get_filelists()
            unknown=file_catgory(file_lists)
            while unknown!=[]:
                print('尚有以下未分類\n', unknown)
                is_try=input('是否嘗試下載資料？\n(y=1 n=2)')
                if is_try=='1':
                    for ele in unknown:
                        print(f'嘗試下載{ele}的資料...')
                        avinfo=web_crawler.crawler_switcher(ele)
                        if avinfo!={}:
                            save_info(avinfo)
                            print_info(avinfo)
                        else:
                            print('無此番號資料')
                    file_lists=get_filelists()
                    unknown=file_catgory(file_lists)
                elif is_try=='2':
                    os.system('clear')
                    sys.exit("程式結束")
                else:
                    print('輸入錯誤')
                    continue
        elif is_catgory=='2':
            os.system('clear')
            sys.exit("程式結束")
        else:
            print('輸入錯誤')
            continue
    elif mode=='q':
        os.system('clear')
        sys.exit("程式結束")
    else:
        print('輸入錯誤')
