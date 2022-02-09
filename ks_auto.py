import re
import random
import requests
import time
#发送邮件模块
#***************************************************************
import smtplib
from email.mime.text import MIMEText
mail_host = 'smtp.163.com'  #邮件
mail_user = '13513236276'  #账号用户名
mail_pass = 'CQHHBSJIFGDDMUKP'   #账号密码 网易邮箱是smtp绑定码
sender = '13513236276@163.com'  #发送邮箱
receivers = ['2871599908@qq.com']  #接收邮箱


def send_mail(title='',content=''):
    #登录并发送邮件
    message = MIMEText(content,'plain','utf-8')#发送格式
    message['Subject'] = title #发送标题
    message['From'] = sender #发送方邮件
    message['To'] = receivers[0]  #接收方邮件
    try:
        smtpObj = smtplib.SMTP()  #连接到服务器
        smtpObj.connect(mail_host,25)#登录到服务器
        smtpObj.login(mail_user,mail_pass) #发送
        smtpObj.sendmail(#退出
            sender,receivers,message.as_string()) 
        smtpObj.quit() 
        print('失败信息邮件已发送')
    except smtplib.SMTPException as e:
        print('失败信息邮件已发送',e) #打印错误
#***************************************************************
#发送邮件模块
header = {
'Connection': 'keep-alive',
'Host': 'ksxskj.hevttc.edu.cn',
'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.80 Safari/537.36 Edg/98.0.1108.43',
'Origin': 'https://ksxskj.hevttc.edu.cn',
'Referer': 'https://ksxskj.hevttc.edu.cn/NCIR/user_data/16543719/change/',
'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
'Accept-Encoding': 'gzip, deflate, br',
'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
'Cookie': ''
}

#/**********************模拟登录
murl ='https://ksxskj.hevttc.edu.cn/'

userdata=                    {
'csrfmiddlewaretoken':'',
'username':'',
'password':'',
'check_code':'',
'next':'/'
}


json = {
    'csrfmiddlewaretoken':'',
    'tw':'36.4',
    'fl':'False',
    'gk':'False',
    'hx':'False',
    'qt':'False',
    'jc':'False',
    'fx':'False',
    'jqjc':'',
    'lc':'河北省张家口市怀来县',
    'actionName':'actionValue'  

}

def Simulate_login():
    s = requests.Session()
    html= s.get(murl).text
    userdata['csrfmiddlewaretoken']=re.findall('"csrfmiddlewaretoken" value="(.*?)"',html)[0]
    header['Cookie'] = re.findall('(csrftoken.*?) f',str(s.cookies))[0]
    srequests =requests.session()
    srequests.post(murl+'/login/?next=/',headers=header,data=userdata).text
    cook_test=str(srequests.cookies)
    x=re.findall('(csrftoken=.*?) ',cook_test)[0]
    y=re.findall('(sessionid=.*?) ',cook_test)[0]
    Cookie=x+';'+y
    header['Cookie'] = Cookie
    json['csrfmiddlewaretoken'] = re.findall('csrftoken=(.*?);',Cookie)[0]

def mlogin(user,passwd):
    userdata['username']=user
    userdata['password']=passwd
    Simulate_login()


def get_time():#获取当前时间
    hour=time.strftime("%H", time.localtime())
    return int(hour)


def get_rand_tw():
    r = random.randint(2,6)
    X = 36+r/10
    return str(X)


def post_tw(user,passwd,address='',url='',time=''):#填写体温的总程序
    try:
        json['tw'] =get_rand_tw() #此行为随机生成体温注释掉为默认体温
        json['lc'] = address
        mlogin(user,passwd)
        r = requests.post(url,headers=header,data=json)
        r.encoding = r.apparent_encoding
        save_s=re.findall('alert\("(.*?)"\);',r.text)
        try:
            if(save_s !=[]):
                print(save_s[0])
            else:
                print('填写失败!')
                #send_mail(time+'自动填写体温失败!')#如果不需要发送邮件可以删除此行
        except:
            print('填写失败!')
            #send_mail(time+'自动填写体温失败!')#如果不需要发送邮件可以删除此行
    except:
        #send_mail(time+'自动填写体温失败!')#如果不需要发送邮件可以删除此行
        return "产生异常"
        
add_url=murl+'NCIR/user_data/add/'

    
def auto_post(user,passwd,address):#自动填写上下午体温
    if(get_time()<12):
        post_tw(user,passwd,address=address,url=add_url,time='上午体温')#上午体温网址
    else:
        post_tw(user,passwd,address=address,url=add_url,time='下午体温')#下午体温网址

if __name__=="__main__":#主程序执行
    auto_post(user='0215190104',passwd='13513236276.',address='河北省张家口市怀来县')
    auto_post(user='0414190127',passwd='011027zm',address='河北省衡水市枣强县')









