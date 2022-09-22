from unicodedata import category
from django.db import models
from datetime import date
from django.contrib.auth.models import User


class Sampleroom(models.Model):
    name=models.CharField(max_length=30)
    owner=models.ForeignKey(User,on_delete=models.CASCADE,related_name='room_owner')

    def __str__(self):
        return \
        self.name

class Room(models.Model):
    name=models.CharField(max_length=30)
    owner=models.ForeignKey(User,on_delete=models.CASCADE,related_name='r_owner')

    def __str__(self):
        return \
        self.name



class Sampleitem(models.Model):
    itemname=models.CharField(max_length=35)
    sampleroom=models.ForeignKey('Sampleroom',on_delete=models.CASCADE)
    originalsize=models.IntegerField(default=10)
    pub_date=models.DateTimeField(auto_now_add=True)
    qty=models.IntegerField(default=1)
    get_date=models.DateField(default=date.today)
    comment=models.TextField(max_length=100, blank=True, null=True)
    owner=models.ForeignKey(User,on_delete=models.CASCADE,related_name='item_owner') 

    class Meta:
        ordering = ('-id',)


class Item(models.Model):
    name=models.CharField(max_length=35)
    room=models.ForeignKey('Room',on_delete=models.CASCADE)
    size=models.IntegerField(default=10)
    pub_date=models.DateTimeField(auto_now_add=True)
    qty=models.IntegerField(default=1)
    get_date=models.DateField(default=date.today)
    comment=models.TextField(max_length=100, blank=True, null=True)
    owner=models.ForeignKey(User,on_delete=models.CASCADE,related_name='i_owner')
    cate_a=
    cate_b=
    delete_flag=
    delete_date=

    class Meta:
        ordering = ('-id',)

#    spea_c02=models.CharField(max_length=35)
#    spea_c03=models.CharField(max_length=35)
#    spea_i01=models.IntegerField(default=-1)
#    spea_i02=models.IntegerField(default=-1)
#    spea_i03=models.IntegerField(default=-1)

    def __str__(self):
        return\
        'アイテムID'+str(self.id)+\
        'アイテム名'+str(self.itemname)+\
        'モノサイズ'+str(self.originalsize)



#棒グラフ練習用モデル　ProductAというモデルクラスを作成
class ProductA(models.Model):
    Date = models.DateField()        #日付
    Revenue = models.IntegerField()  #収益



