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
                elif event.message.text=='各企業任務總覽':
                    message.append(TextSendMessage(text='以下是各企業任務總覽\n台積電\nASML\nKronos\nNXP\n意法'))
                elif event.message.text=='活動規則':
                    message.append(TextSendMessage(text='以下是活動規則\n現在輸入「增加點數」就可以增加100~300點\n試試看'))
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
                            original_content_url='https://reurl.cc/V1VndZ',
                            preview_image_url='https://reurl.cc/V1VndZ'
                        )
                        message.append(image_message) #輸出抽獎卷 還沒試過可不可
                elif event.message.text=='確定兌換 Level 2 抽獎卷':
                    user_info = User_Info.objects.filter(uid=uid,name=name,pic_url=pic_url) 
                    new_points=0
                    less_point=2000
                    for user in user_info:
                        new_points = user.points - less_point
                    User_Info.objects.filter(uid=uid,name=name,pic_url=pic_url).update(points=new_points) #修改
                    for user in user_info:
                        info = 'points=%s'%(new_points)
                        message.append(TextSendMessage(text=info)) #輸出
                    if new_points < 0 :
                        message.append(TextSendMessage(text='喔不你的錢錢不夠，到了抽獎區也不能抽獎喔'))
                    else :
                        message.append(TextSendMessage(text='請到抽獎區抽獎，並出示黑客松幣餘額'))
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
                elif ('Line:'in event.message.text):
                    message.append(TextSendMessage(text='輸入line的密碼'))
                    x = event.message.text.split(":")
                    seaftermod = secretnum(x[1])
                    if (seaftermod==186):
                        message.append(TextSendMessage(text='密碼正確，增加點數'))
                    else:
                        message.append(TextSendMessage(text='密碼錯誤'))

                else:
                    message.append(TextSendMessage(text='再想想'))
                line_bot_api.reply_message(event.reply_token,message)

                return HttpResponse()
            else:
                return HttpResponseBadRequest()
