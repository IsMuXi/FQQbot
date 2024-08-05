import time,os,keyboard,cv2,pytesseract,win32clipboard,os,random,re,pyperclip,requests
import pyautogui as pag
import numpy as np
from PIL import Image,ImageEnhance
from io import BytesIO
def gain():
    def gain_input_xy():
        for i in range(1,11):
            print('采集输入框坐标中......')
            print('请保持鼠标在输入栏 '+str(round(5-i*0.5,1))+'s之后完成采集')
            time.sleep(0.5)
            screenWidth, screenHeight = pag.size()
            x, y = pag.position()
            print('屏幕尺寸:(%s %s),当前鼠标坐标:(%s, %s)'%(screenWidth,screenHeight,x,y))
            os.system('cls')
        print('最终输入框坐标为:(%s, %s)'%(x,y))
        global input_x,input_y
        input_x,input_y = x,y
        print('按N继续下一项,按R重新采集')
        while True:
            if keyboard.is_pressed('N'):
                break
            if keyboard.is_pressed('R'):
                gain_input_xy()
    def gain_msg_xy():
        screenWidth,screenHeight = pag.size()
        global msg_x1,msg_x2,msg_y1,msg_y2
        for i in range(1,11):
            print('采集消息获取对角线坐标中......')
            print('请保持指针在对角线顶点 '+str(round(5-i*0.5,1))+'s之后完成第一项采集')
            time.sleep(0.5)
            x,y = pag.position()
            print('屏幕尺寸:(%s %s),当前鼠标坐标:(%s, %s)'%(screenWidth,screenHeight,x,y))
            os.system('cls')
            msg_x1,msg_y1 = x,y
        for i in range(1,11):
            print('请保持指针在对角线另一顶点 '+str(round(5-i*0.5,1))+'s之后完成第二项采集')
            time.sleep(0.5)
            x,y = pag.position()
            print('屏幕尺寸:(%s %s),当前鼠标坐标:(%s, %s)'%(screenWidth,screenHeight,x,y))
            os.system('cls')            
            msg_x2,msg_y2 = x,y
        print('第一顶点坐标为:(%s, %s)'%(msg_x1,msg_y1))
        print('第二顶点坐标为:(%s, %s)'%(msg_x2,msg_y2))
        print('按N继续下一项,按R重新采集')
        while True:
            if keyboard.is_pressed('N'):
                break
            if keyboard.is_pressed('R'):
                gain_msg_xy()
    gain_input_xy()
    gain_msg_xy()
gain()
def repeat():
    img = pag.screenshot(region=[min(msg_x1,msg_x2),min(msg_y1,msg_y2),abs(msg_x2-msg_x1),abs(msg_y2-msg_y1)])
    img_bgr = cv2.cvtColor(np.asarray(img), cv2.COLOR_RGB2BGR)    
    cv2.imwrite("screenshot.png", img_bgr) 
    img = Image.open("screenshot.png")
    enhancer = ImageEnhance.Contrast(img)
    img_contrast = enhancer.enhance(5)
    time.sleep(0.5)
    text = pytesseract.image_to_string(img_contrast,lang='chi_sim')
    print("识别结果：", text)
    time.sleep(0.2)
    if ('菜单' in text) == True:
        img2 = Image.open('菜单.jpg')        
        output = BytesIO()
        img2.save(output, 'BMP')
        data = output.getvalue()[14:]
        output.close()
        win32clipboard.OpenClipboard()
        win32clipboard.EmptyClipboard()
        win32clipboard.SetClipboardData(win32clipboard.CF_DIB, data)
        win32clipboard.CloseClipboard()
        pag.click(input_x,input_y,button='left')
        pag.hotkey('ctrl','v')
        time.sleep(0.2)
        pag.hotkey('enter')
    if (('来' in text) == True) and (('张' in text) == True) and (('图' in text) == True):
        m = random.choice(range(1,11))
        pyperclip.copy('正在为您寻找图片中......')
        pag.click(input_x,input_y,button='left')
        pag.hotkey('ctrl','v')
        pag.hotkey('enter')
        time.sleep(0.1)
        pyperclip.copy('找到'+str(m)+'张')
        pag.click(input_x,input_y,button='left')
        pag.hotkey('ctrl','v')
        pag.hotkey('enter')
        if not os.path.exists('./缓存'):
            os.mkdir('./缓存')
        url = 'https://api.lolicon.app/setu/v2?size=original&tag=jk|白丝|黑丝|裸足|水手服|女仆装|萝莉|肉丝|御姐|白裤袜|黑裤袜|&r18=0&num='+str(m)
        headers = {
            'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36 Edg/127.0.0.0'
        }
        res = requests.get(url,headers=headers).json()
        os.system('cls')
        global total
        total = len(res['data'])
        print(total)
        global titles,urls
        titles = []
        tags = []
        urls = []
        for i in range(len(res['data'])):
            titles.append(str(res['data'][i]['title']).replace("\\",'').replace('/','').replace('*','').replace('?','').replace('"','').replace('<','').replace('>','').replace('|',''))
            tags.append(res['data'][i]['tags'])
            urls.append(res['data'][i]['urls']['original'])
        urls_and_names = dict(zip(urls,titles))
        a = 1
        with open('./logs.txt','w',encoding='utf-8') as f:
            f.write(str(titles)+str(urls))
        for pic_url,title in urls_and_names.items():
            pictures = requests.get(pic_url,headers=headers).content
            with open('./缓存/'+title+'.jpg','wb') as f:
                f.write(pictures)
            pyperclip.copy('拿到'+str(a)+'张图片了！')
            pag.click(input_x,input_y,button='left')
            pag.hotkey('ctrl','v')
            time.sleep(0.1)
            pag.hotkey('enter')
            a += 1
        def new_picture():
            url = 'https://api.lolicon.app/setu/v2?size=original&tag=jk|白丝|黑丝|裸足|水手服|女仆装|萝莉|肉丝|御姐|少女&r18=0&num='+str(m)
            headers = {
                'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36 Edg/127.0.0.0'
            }
            res = requests.get(url,headers=headers).json()
            os.system('cls')
            global title_new,tags_new,url_new
            title_new = (str(res['data'][0]['title']).replace("\\",'').replace('/','').replace('*','').replace('?','').replace('"','').replace('<','').replace('>','').replace('|',''))
            tags_new = str(res['data'][0]['tags'])
            url_new = str(res['data'][0]['urls']['original'])
            pictures = requests.get(url_new,headers=headers).content
            with open('./缓存/'+title_new+'.jpg','wb') as f:
                f.write(pictures)
            stats = os.stat('./缓存/'+title_new+'.jpg')
            print(stats.st_size)
            if stats.st_size >= 1000:
                img3 = Image.open('./缓存/'+title_new+'.jpg')
                print(stats.st_size/(1000**2),'Plan B')
                if ((stats.st_size/(1000**2)) <=10):
                    output = BytesIO()
                    img3.save(output, 'BMP')
                    data = output.getvalue()[14:]
                    output.close()
                    win32clipboard.OpenClipboard()
                    win32clipboard.EmptyClipboard()
                    win32clipboard.SetClipboardData(win32clipboard.CF_DIB, data)
                    win32clipboard.CloseClipboard()
                    pag.click(input_x,input_y,button='left')
                    pag.hotkey('ctrl','v')
                    time.sleep(0.1)
                    pag.hotkey('ctrl','enter')
                    pyperclip.copy('title:'+title_new)
                    pag.hotkey('ctrl','v')
                    time.sleep(0.5)         
                    pag.hotkey('enter')
                    titles.append(title_new)
                    urls.append(url_new)
            else:
                new_picture()
        b = 0
        for picture in titles:
            stats = os.stat('./缓存/'+picture+'.jpg')
            print(stats.st_size)
            if stats.st_size >= 1000:
                print('第一关过关')
                img3 = Image.open('./缓存/'+picture+'.jpg')
                print(stats.st_size/(1000**2))
                if ((stats.st_size/(1000**2)) <=10000):
                    output = BytesIO()
                    img3.save(output, 'BMP')
                    data = output.getvalue()[14:]
                    output.close()
                    win32clipboard.OpenClipboard()
                    win32clipboard.EmptyClipboard()
                    win32clipboard.SetClipboardData(win32clipboard.CF_DIB, data)
                    win32clipboard.CloseClipboard()
                    pag.click(input_x,input_y,button='left')
                    pag.hotkey('ctrl','v')
                    time.sleep(0.1)
                    pag.hotkey('ctrl','enter')
                    pyperclip.copy('title:'+picture)
                    pag.hotkey('ctrl','v')
                    time.sleep(0.5)         
                    pag.hotkey('enter')
                    b +=1
        for i in range(total - b ):
            print('plan B')
            new_picture()
        pyperclip.copy('图片来辣')
        pag.click(input_x,input_y,button='left')
        pag.hotkey('ctrl','v')
        pag.hotkey('enter')
        print(titles,'\n',tags,'\n',urls)
        pyperclip.copy('注:图片来自网络爬取 随机到什么图与本程序作者无关')
        pag.click(input_x,input_y,button='left')
        pag.hotkey('ctrl','v')
        pag.hotkey('enter')
    repeat()
repeat()