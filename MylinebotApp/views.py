from django.shortcuts import render
from MylinebotApp.models import *

#我自己加的
import random

# Create your views here.
from django.conf import settings
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt

from linebot import LineBotApi, WebhookParser
from linebot.exceptions import InvalidSignatureError, LineBotApiError
#from linebot.models import MessageEvent, TextSendMessage #原本的
from linebot.models import *

line_bot_api = LineBotApi(settings.LINE_CHANNEL_ACCESS_TOKEN)
parser = WebhookParser(settings.LINE_CHANNEL_SECRET)


#解密碼函式
def anyToDecimal(num,n):
    baseStr = {"0":0,"1":1,"2":2,"3":3,"4":4,"5":5,"6":6,"7":7,"8":8,"9":9,
               "A":10,"B":11,"C":12,"D":13,"E":14,"F":15,"G":16,"H":17,"I":18,"J":19,
               "K":20,"L":21,"M":22,"N":23,"O":24,"P":25,"Q":26,"R":27,"S":28,"T":29,
               "U":30,"V":31,"W":32,"X":33,"Y":34,"Z":35}
    new_num = 0
    nNum = len(num) - 1
    for i in num:         
        new_num = new_num  + baseStr[i]*pow(n,nNum)
        nNum = nNum -1 
    return new_num
def secretnum(a):
    anyToDecimal(a,36)
    return (anyToDecimal(a,36) % 2022) #這裡可以拿到最後要的mod出來的值 2022要記得改掉

@csrf_exempt
def callback(request):
    if request.method == 'POST':
        signature = request.META['HTTP_X_LINE_SIGNATURE']
        body = request.body.decode('utf-8')

        try:
            events = parser.parse(body, signature)
        except InvalidSignatureError:
            return HttpResponseForbidden()
        except LineBotApiError:
            return HttpResponseBadRequest()

        for event in events:
            if isinstance(event, MessageEvent):
                mtext=event.message.text
                uid=event.source.user_id
                profile=line_bot_api.get_profile(uid)
                name=profile.display_name
                pic_url=profile.picture_url
                points=0

                message=[]
                if event.message.text=='開始遊戲':
                    if User_Info.objects.filter(uid=uid).exists()==False:
                        User_Info.objects.create(uid=uid,name=name,pic_url=pic_url,mtext=mtext,points=points)
                        message.append(TextSendMessage(text='註冊成功'))
                    else:
                        message.append(TextSendMessage(text='已註冊'))
                elif event.message.text=='查看黑客松幣總額':
                    user_info = User_Info.objects.filter(uid=uid,name=name,pic_url=pic_url)
                    for user in user_info:
                        info = 'points=%s'%(user.points)
                        message.append(TextSendMessage(text=info))

                elif event.message.text=='確定兌換 Level 1 抽獎卷':
                    user_info = User_Info.objects.filter(uid=uid,name=name,pic_url=pic_url) 
                    new_points=0
                    less_point=1200
                    for user in user_info:
                        new_points = user.points - less_point
                    User_Info.objects.filter(uid=uid,name=name,pic_url=pic_url).update(points=new_points) #修改
                    for user in user_info:
                        info = 'points=%s'%(new_points)
                        message.append(TextSendMessage(text=info)) #輸出
                    if new_points < 0 :
                        message.append(TextSendMessage(text='喔不你的錢錢不夠，不能兌換抽獎卷喔'))
                        for user in user_info:
                            new_points = user.points 
                        User_Info.objects.filter(uid=uid,name=name,pic_url=pic_url).update(points=new_points) #修改回原本的
                        for user in user_info:
                            info = 'points=%s'%(new_points)
                            message.append(TextSendMessage(text=info)) #輸出
                    else :
                        message.append(TextSendMessage(text='請到抽獎區抽獎，並出示抽獎卷'))
                        image_message = ImageSendMessage(
                            original_content_url='https://scontent-tpe1-1.xx.fbcdn.net/v/t39.30808-6/309748365_100109239563436_8451180494723915841_n.jpg?_nc_cat=105&ccb=1-7&_nc_sid=730e14&_nc_ohc=Qavv28yRbyMAX_BPpN1&tn=FKUeTQCsg2KYCGQ3&_nc_ht=scontent-tpe1-1.xx&oh=00_AT8kyuCPH5igOe4uM7QHKr12SjUqTmoITiuXdZSbb46sVQ&oe=63488F97',
                            preview_image_url='https://scontent-tpe1-1.xx.fbcdn.net/v/t39.30808-6/309748365_100109239563436_8451180494723915841_n.jpg?_nc_cat=105&ccb=1-7&_nc_sid=730e14&_nc_ohc=Qavv28yRbyMAX_BPpN1&tn=FKUeTQCsg2KYCGQ3&_nc_ht=scontent-tpe1-1.xx&oh=00_AT8kyuCPH5igOe4uM7QHKr12SjUqTmoITiuXdZSbb46sVQ&oe=63488F97'
                        )
                        message.append(image_message) #輸出抽獎卷 
                elif event.message.text=='確定兌換 Level 2 抽獎卷':
                    user_info = User_Info.objects.filter(uid=uid,name=name,pic_url=pic_url) 
                    new_points=0
                    less_point=1900
                    for user in user_info:
                        new_points = user.points - less_point
                    User_Info.objects.filter(uid=uid,name=name,pic_url=pic_url).update(points=new_points) #修改
                    for user in user_info:
                        info = 'points=%s'%(new_points)
                        message.append(TextSendMessage(text=info)) #輸出
                    if new_points < 0 :
                        message.append(TextSendMessage(text='喔不你的錢錢不夠，不能兌換抽獎卷喔'))
                        for user in user_info:
                            new_points = user.points 
                        User_Info.objects.filter(uid=uid,name=name,pic_url=pic_url).update(points=new_points) #修改回原本的
                        for user in user_info:
                            info = 'points=%s'%(new_points)
                            message.append(TextSendMessage(text=info)) #輸出
                    else :
                        message.append(TextSendMessage(text='請到抽獎區抽獎，並出示抽獎卷'))
                        image_message = ImageSendMessage(
                            original_content_url='https://scontent-tpe1-1.xx.fbcdn.net/v/t39.30808-6/310650538_100111356229891_866083673074835272_n.jpg?_nc_cat=103&ccb=1-7&_nc_sid=730e14&_nc_ohc=sBh92GOoEZEAX9jLhXA&_nc_ht=scontent-tpe1-1.xx&oh=00_AT9W8J2WayEdXWy9TAFDuhGBSLhUV5aApHOxtTgBRzP--w&oe=6348C5DC',
                            preview_image_url='https://scontent-tpe1-1.xx.fbcdn.net/v/t39.30808-6/310650538_100111356229891_866083673074835272_n.jpg?_nc_cat=103&ccb=1-7&_nc_sid=730e14&_nc_ohc=sBh92GOoEZEAX9jLhXA&_nc_ht=scontent-tpe1-1.xx&oh=00_AT9W8J2WayEdXWy9TAFDuhGBSLhUV5aApHOxtTgBRzP--w&oe=6348C5DC'
                        )
                        message.append(image_message) #輸出抽獎卷
                elif event.message.text=='確定兌換 Level 3 抽獎卷':
                    user_info = User_Info.objects.filter(uid=uid,name=name,pic_url=pic_url) 
                    new_points=0
                    less_point=2500
                    for user in user_info:
                        new_points = user.points - less_point
                    User_Info.objects.filter(uid=uid,name=name,pic_url=pic_url).update(points=new_points) #修改
                    for user in user_info:
                        info = 'points=%s'%(new_points)
                        message.append(TextSendMessage(text=info)) #輸出
                    if new_points < 0 :
                        message.append(TextSendMessage(text='喔不你的錢錢不夠，不能兌換抽獎卷喔'))
                        for user in user_info:
                            new_points = user.points 
                        User_Info.objects.filter(uid=uid,name=name,pic_url=pic_url).update(points=new_points) #修改回原本的
                        for user in user_info:
                            info = 'points=%s'%(new_points)
                            message.append(TextSendMessage(text=info)) #輸出
                    else :
                        message.append(TextSendMessage(text='請到抽獎區抽獎，並出示抽獎卷'))
                        image_message = ImageSendMessage(
                            original_content_url='https://scontent-tpe1-1.xx.fbcdn.net/v/t39.30808-6/310107356_100111389563221_7983913375440295230_n.jpg?_nc_cat=103&ccb=1-7&_nc_sid=730e14&_nc_ohc=HlbIuzWPm2cAX-OFoNS&_nc_ht=scontent-tpe1-1.xx&oh=00_AT8ONPkzekx0MG9BmPzkEXOGewMLbAKF7ErsPBIPnLS6Tw&oe=634961A8',
                            preview_image_url='https://scontent-tpe1-1.xx.fbcdn.net/v/t39.30808-6/310107356_100111389563221_7983913375440295230_n.jpg?_nc_cat=103&ccb=1-7&_nc_sid=730e14&_nc_ohc=HlbIuzWPm2cAX-OFoNS&_nc_ht=scontent-tpe1-1.xx&oh=00_AT8ONPkzekx0MG9BmPzkEXOGewMLbAKF7ErsPBIPnLS6Tw&oe=634961A8'
                        )
                        message.append(image_message) #輸出抽獎卷
                elif event.message.text=='輸出會員資料':
                    user_info = User_Info.objects.filter(uid=uid,name=name,pic_url=pic_url)
                    for user in user_info:
                        info = 'UID=%s\nNAME=%s\n大頭貼=%s\npoints=%s\n'%(user.uid,user.name,user.pic_url,user.points)
                        message.append(TextSendMessage(text=info))
                elif event.message.text=='增加點數':
                    user_info = User_Info.objects.filter(uid=uid,name=name,pic_url=pic_url) 
                    new_points=0
                    add_point=random.randrange(100,301,100)
                    for user in user_info:
                        new_points = user.points + add_point
                    User_Info.objects.filter(uid=uid,name=name,pic_url=pic_url).update(points=new_points) #修改
                    for user in user_info:
                        info = 'points=%s'%(new_points)
                        message.append(TextSendMessage(text=info))
                elif event.message.text=='刪除會員資料':
                    User_Info.objects.filter(uid=uid,name=name,pic_url=pic_url).delete() #刪除
                elif ('LINE:'in event.message.text):
                    message.append(TextSendMessage(text='輸入了LINE的密碼'))
                    x = event.message.text.split(":")
                    seaftermod = secretnum(x[1])
                    if (seaftermod==36):
                        user_info = User_Info.objects.filter(uid=uid,name=name,pic_url=pic_url) 
                        line_info = LINE.objects.all()
                        for user in user_info:
                            flag = 0
                            for line in line_info:
                                if(x[1]==line.password):
                                    flag=1
                                    break
                            if(flag == 1):
                                info = '這個企業密碼已被使用過'
                                message.append(TextSendMessage(text=info))
                            elif(user.Line==1):
                                info = '你已經拿過這個企業的點數了喔'
                                message.append(TextSendMessage(text=info))
                            else:
                                message.append(TextSendMessage(text='密碼正確，增加點數'))
                                new_points=0
                                add_point=random.randrange(100,301,100)
                                info = '恭喜增加...\n%s點'%(add_point)
                                message.append(TextSendMessage(text=info))
                                for user in user_info:
                                    new_points = user.points + add_point
                                LINE.objects.create(password=x[1])
                                User_Info.objects.filter(uid=uid,name=name,pic_url=pic_url).update(points=new_points) #修改
                                User_Info.objects.filter(uid=uid,name=name,pic_url=pic_url).update(Line=1) #修改
                                for user in user_info:
                                    info = '現在點數points=%s'%(new_points)
                                    message.append(TextSendMessage(text=info))
                    else:
                        message.append(TextSendMessage(text='密碼錯誤，再試試看'))
                elif ('TSMC:'in event.message.text):
                    message.append(TextSendMessage(text='輸入了TSMC台積電的密碼'))
                    x = event.message.text.split(":")
                    seaftermod = secretnum(x[1])
                    if (seaftermod==25):
                        user_info = User_Info.objects.filter(uid=uid,name=name,pic_url=pic_url) 
                        for user in user_info:
                            if(user.tsmc==1):
                                info = '你已經拿過這個企業的點數了喔'
                                message.append(TextSendMessage(text=info))
                            else:
                                message.append(TextSendMessage(text='密碼正確，增加點數'))
                                new_points=0
                                add_point=random.randrange(100,301,100)
                                info = '恭喜增加...\n%s點'%(add_point)
                                message.append(TextSendMessage(text=info))
                                for user in user_info:
                                    new_points = user.points + add_point
                                User_Info.objects.filter(uid=uid,name=name,pic_url=pic_url).update(points=new_points) #修改
                                User_Info.objects.filter(uid=uid,name=name,pic_url=pic_url).update(tsmc=1) #修改
                                for user in user_info:
                                    info = '現在點數points=%s'%(new_points)
                                    message.append(TextSendMessage(text=info))
                    else:
                        message.append(TextSendMessage(text='密碼錯誤，再試試看'))
                elif ('STM:'in event.message.text):
                    message.append(TextSendMessage(text='輸入了意法半導體的密碼'))
                    x = event.message.text.split(":")
                    seaftermod = secretnum(x[1])
                    if (seaftermod==34):
                        user_info = User_Info.objects.filter(uid=uid,name=name,pic_url=pic_url) 
                        for user in user_info:
                            if(user.STM==1):
                                info = '你已經拿過這個企業的點數了喔'
                                message.append(TextSendMessage(text=info))
                            else:
                                message.append(TextSendMessage(text='密碼正確，增加點數'))
                                new_points=0
                                add_point=random.randrange(100,301,100)
                                info = '恭喜增加...\n%s點'%(add_point)
                                message.append(TextSendMessage(text=info))
                                for user in user_info:
                                    new_points = user.points + add_point
                                User_Info.objects.filter(uid=uid,name=name,pic_url=pic_url).update(points=new_points) #修改
                                User_Info.objects.filter(uid=uid,name=name,pic_url=pic_url).update(STM=1) #修改
                                for user in user_info:
                                    info = '現在點數points=%s'%(new_points)
                                    message.append(TextSendMessage(text=info))                    
                    else:
                        message.append(TextSendMessage(text='密碼錯誤，再試試看'))
                elif ('Yahoo:'in event.message.text):
                    message.append(TextSendMessage(text='輸入了Yahoo的密碼'))
                    x = event.message.text.split(":")
                    seaftermod = secretnum(x[1])
                    if (seaftermod==32):
                        user_info = User_Info.objects.filter(uid=uid,name=name,pic_url=pic_url) 
                        for user in user_info:
                            if(user.Yahoo==1):
                                info = '你已經拿過這個企業的點數了喔'
                                message.append(TextSendMessage(text=info))
                            else:
                                message.append(TextSendMessage(text='密碼正確，增加點數'))
                                new_points=0
                                add_point=random.randrange(100,301,100)
                                info = '恭喜增加...\n%s點'%(add_point)
                                message.append(TextSendMessage(text=info))
                                for user in user_info:
                                    new_points = user.points + add_point
                                User_Info.objects.filter(uid=uid,name=name,pic_url=pic_url).update(points=new_points) #修改
                                User_Info.objects.filter(uid=uid,name=name,pic_url=pic_url).update(Yahoo=1) #修改
                                for user in user_info:
                                    info = '現在點數points=%s'%(new_points)
                                    message.append(TextSendMessage(text=info))
                    else:
                        message.append(TextSendMessage(text='密碼錯誤，再試試看'))
                elif ('ASML:'in event.message.text):
                    message.append(TextSendMessage(text='輸入了ASML艾司摩爾的密碼'))
                    x = event.message.text.split(":")
                    seaftermod = secretnum(x[1])
                    if (seaftermod==30):
                        user_info = User_Info.objects.filter(uid=uid,name=name,pic_url=pic_url) 
                        for user in user_info:
                            if(user.ASML==1):
                                info = '你已經拿過這個企業的點數了喔'
                                message.append(TextSendMessage(text=info))
                            else:
                                message.append(TextSendMessage(text='密碼正確，增加點數'))
                                new_points=0
                                add_point=random.randrange(100,301,100)
                                info = '恭喜增加...\n%s點'%(add_point)
                                message.append(TextSendMessage(text=info))
                                for user in user_info:
                                    new_points = user.points + add_point
                                User_Info.objects.filter(uid=uid,name=name,pic_url=pic_url).update(points=new_points) #修改
                                User_Info.objects.filter(uid=uid,name=name,pic_url=pic_url).update(ASML=1) #修改
                                for user in user_info:
                                    info = '現在點數points=%s'%(new_points)
                                    message.append(TextSendMessage(text=info))
                    else:
                        message.append(TextSendMessage(text='密碼錯誤，再試試看'))
                elif ('NXP:'in event.message.text):
                    message.append(TextSendMessage(text='輸入了恩智浦半導體的密碼'))
                    x = event.message.text.split(":")
                    seaftermod = secretnum(x[1])
                    if (seaftermod==28):
                        user_info = User_Info.objects.filter(uid=uid,name=name,pic_url=pic_url) 
                        for user in user_info:
                            if(user.NXP==1):
                                info = '你已經拿過這個企業的點數了喔'
                                message.append(TextSendMessage(text=info))
                            else:
                                message.append(TextSendMessage(text='密碼正確，增加點數'))
                                new_points=0
                                add_point=random.randrange(100,301,100)
                                info = '恭喜增加...\n%s點'%(add_point)
                                message.append(TextSendMessage(text=info))
                                for user in user_info:
                                    new_points = user.points + add_point
                                User_Info.objects.filter(uid=uid,name=name,pic_url=pic_url).update(points=new_points) #修改
                                User_Info.objects.filter(uid=uid,name=name,pic_url=pic_url).update(NXP=1) #修改
                                for user in user_info:
                                    info = '現在點數points=%s'%(new_points)
                                    message.append(TextSendMessage(text=info))
                    else:
                        message.append(TextSendMessage(text='密碼錯誤，再試試看'))
                elif ('Hsinchu:'in event.message.text):
                    message.append(TextSendMessage(text='輸入了新竹市政府的密碼'))
                    x = event.message.text.split(":")
                    seaftermod = secretnum(x[1])
                    if (seaftermod==26):
                        user_info = User_Info.objects.filter(uid=uid,name=name,pic_url=pic_url) 
                        for user in user_info:
                            if(user.Hsinchu==1):
                                info = '你已經拿過這個企業的點數了喔'
                                message.append(TextSendMessage(text=info))
                            else:
                                message.append(TextSendMessage(text='密碼正確，增加點數'))
                                new_points=0
                                add_point=random.randrange(100,301,100)
                                info = '恭喜增加...\n%s點'%(add_point)
                                message.append(TextSendMessage(text=info))
                                for user in user_info:
                                    new_points = user.points + add_point
                                User_Info.objects.filter(uid=uid,name=name,pic_url=pic_url).update(points=new_points) #修改
                                User_Info.objects.filter(uid=uid,name=name,pic_url=pic_url).update(Hsinchu=1) #修改
                                for user in user_info:
                                    info = '現在點數points=%s'%(new_points)
                                    message.append(TextSendMessage(text=info))
                    else:
                        message.append(TextSendMessage(text='密碼錯誤，再試試看'))
                elif ('Kronos:'in event.message.text):
                    message.append(TextSendMessage(text='輸入了Kronos Research麒點科技的密碼'))
                    x = event.message.text.split(":")
                    seaftermod = secretnum(x[1])
                    if (seaftermod==24):
                        user_info = User_Info.objects.filter(uid=uid,name=name,pic_url=pic_url) 
                        for user in user_info:
                            if(user.Kronos==1):
                                info = '你已經拿過這個企業的點數了喔'
                                message.append(TextSendMessage(text=info))
                            else:
                                message.append(TextSendMessage(text='密碼正確，增加點數'))
                                new_points=0
                                add_point=random.randrange(100,301,100)
                                info = '恭喜增加...\n%s點'%(add_point)
                                message.append(TextSendMessage(text=info))
                                for user in user_info:
                                    new_points = user.points + add_point
                                User_Info.objects.filter(uid=uid,name=name,pic_url=pic_url).update(points=new_points) #修改
                                User_Info.objects.filter(uid=uid,name=name,pic_url=pic_url).update(Kronos=1) #修改
                                for user in user_info:
                                    info = '現在點數points=%s'%(new_points)
                                    message.append(TextSendMessage(text=info))
                    else:
                        message.append(TextSendMessage(text='密碼錯誤，再試試看'))
                elif ('Cathay:'in event.message.text):
                    message.append(TextSendMessage(text='輸入了國泰金控的密碼'))
                    x = event.message.text.split(":")
                    seaftermod = secretnum(x[1])
                    if (seaftermod==22):
                        user_info = User_Info.objects.filter(uid=uid,name=name,pic_url=pic_url) 
                        for user in user_info:
                            if(user.Cathay==1):
                                info = '你已經拿過這個企業的點數了喔'
                                message.append(TextSendMessage(text=info))
                            else:
                                message.append(TextSendMessage(text='密碼正確，增加點數'))
                                new_points=0
                                add_point=random.randrange(100,301,100)
                                info = '恭喜增加...\n%s點'%(add_point)
                                message.append(TextSendMessage(text=info))
                                for user in user_info:
                                    new_points = user.points + add_point
                                User_Info.objects.filter(uid=uid,name=name,pic_url=pic_url).update(points=new_points) #修改
                                User_Info.objects.filter(uid=uid,name=name,pic_url=pic_url).update(Cathay=1) #修改
                                for user in user_info:
                                    info = '現在點數points=%s'%(new_points)
                                    message.append(TextSendMessage(text=info))
                    else:
                        message.append(TextSendMessage(text='密碼錯誤，再試試看'))
                elif ('CTBC:'in event.message.text):
                    message.append(TextSendMessage(text='輸入了中國信託的密碼'))
                    x = event.message.text.split(":")
                    seaftermod = secretnum(x[1])
                    if (seaftermod==20):
                        user_info = User_Info.objects.filter(uid=uid,name=name,pic_url=pic_url) 
                        for user in user_info:
                            if(user.CTBC==1):
                                info = '你已經拿過這個企業的點數了喔'
                                message.append(TextSendMessage(text=info))
                            else:
                                message.append(TextSendMessage(text='密碼正確，增加點數'))
                                new_points=0
                                add_point=random.randrange(100,301,100)
                                info = '恭喜增加...\n%s點'%(add_point)
                                message.append(TextSendMessage(text=info))
                                for user in user_info:
                                    new_points = user.points + add_point
                                User_Info.objects.filter(uid=uid,name=name,pic_url=pic_url).update(points=new_points) #修改
                                User_Info.objects.filter(uid=uid,name=name,pic_url=pic_url).update(CTBC=1) #修改
                                for user in user_info:
                                    info = '現在點數points=%s'%(new_points)
                                    message.append(TextSendMessage(text=info))
                    else:
                        message.append(TextSendMessage(text='密碼錯誤，再試試看'))
                elif ('104:'in event.message.text):
                    message.append(TextSendMessage(text='輸入了一零四資訊科技的密碼'))
                    x = event.message.text.split(":")
                    seaftermod = secretnum(x[1])
                    if (seaftermod==16):
                        user_info = User_Info.objects.filter(uid=uid,name=name,pic_url=pic_url) 
                        for user in user_info:
                            if(user.a104==1):
                                info = '你已經拿過這個企業的點數了喔'
                                message.append(TextSendMessage(text=info))
                            else:
                                message.append(TextSendMessage(text='密碼正確，增加點數'))
                                new_points=0
                                add_point=random.randrange(100,301,100)
                                info = '恭喜增加...\n%s點'%(add_point)
                                message.append(TextSendMessage(text=info))
                                for user in user_info:
                                    new_points = user.points + add_point
                                User_Info.objects.filter(uid=uid,name=name,pic_url=pic_url).update(points=new_points) #修改
                                User_Info.objects.filter(uid=uid,name=name,pic_url=pic_url).update(a104=1) #修改
                                for user in user_info:
                                    info = '現在點數points=%s'%(new_points)
                                    message.append(TextSendMessage(text=info))
                    else:
                        message.append(TextSendMessage(text='密碼錯誤，再試試看'))
                elif ('PixArt:'in event.message.text):
                    message.append(TextSendMessage(text='輸入了原相科技的密碼'))
                    x = event.message.text.split(":")
                    seaftermod = secretnum(x[1])
                    if (seaftermod==19):
                        user_info = User_Info.objects.filter(uid=uid,name=name,pic_url=pic_url) 
                        for user in user_info:
                            if(user.Pixart==1):
                                info = '你已經拿過這個企業的點數了喔'
                                message.append(TextSendMessage(text=info))
                            else:
                                message.append(TextSendMessage(text='密碼正確，增加點數'))
                                new_points=0
                                add_point=random.randrange(100,301,100)
                                info = '恭喜增加...\n%s點'%(add_point)
                                message.append(TextSendMessage(text=info))
                                for user in user_info:
                                    new_points = user.points + add_point
                                User_Info.objects.filter(uid=uid,name=name,pic_url=pic_url).update(points=new_points) #修改
                                User_Info.objects.filter(uid=uid,name=name,pic_url=pic_url).update(Pixart=1) #修改
                                for user in user_info:
                                    info = '現在點數points=%s'%(new_points)
                                    message.append(TextSendMessage(text=info))
                    else:
                        message.append(TextSendMessage(text='密碼錯誤，再試試看'))




                #else:
                    #message.append(TextSendMessage(text='再想想'))
                line_bot_api.reply_message(event.reply_token,message)

                return HttpResponse()
            else:
                return HttpResponseBadRequest()
