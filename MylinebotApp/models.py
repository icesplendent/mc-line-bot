from django.db import models

# Create your models here.
class User_Info(models.Model):
    uid = models.CharField(max_length=50,null=False,default='')         #user_id
    name = models.CharField(max_length=255,blank=True,null=False)       #LINE名字
    pic_url = models.CharField(max_length=255,null=False)               #大頭貼網址
    mtext = models.CharField(max_length=255,blank=True,null=False)      #文字訊息紀錄
    mdt = models.DateTimeField(auto_now=True)                           #物件儲存的日期時間
    points = models.IntegerField(default=0)                             #點數
    STM = models.IntegerField(default=0)                                #意法
    Yahoo = models.IntegerField(default=0)
    ASML = models.IntegerField(default=0)
    NXP = models.IntegerField(default=0)
    Chunghwa = models.IntegerField(default=0)                           #中華電信
    Kronos = models.IntegerField(default=0)
    Cathay = models.IntegerField(default=0)                             #國泰
    CTBC = models.IntegerField(default=0)                               #中信金控
    Line = models.IntegerField(default=0)
    tsmc = models.IntegerField(default=0)
    a104 = models.IntegerField(default=0)
    Pixart = models.IntegerField(default=0)

    def __str__(self):
        return self.uid
