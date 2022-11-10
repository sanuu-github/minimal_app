#論理削除参考サイト：https://toruuetani.hatenablog.com/entry/20071209/p1


#インポート文
from django.db import models
from datetime import date
from django.contrib.auth.models import User


class Sampleroom(models.Model):
    name=models.CharField(max_length=30)
    owner=models.ForeignKey(User,on_delete=models.CASCADE,related_name='room_owner')
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
    def __str__(self):
        return\
        'アイテムID'+str(self.id)+\
        'アイテム名'+str(self.itemname)+\
        'モノサイズ'+str(self.originalsize)


class Room(models.Model):
    name=models.CharField(max_length=25)
    owner=models.ForeignKey(User,on_delete=models.CASCADE,related_name='r_owner')
    def __str__(self):
        return \
        self.name


class Item(models.Model):
    owner=models.ForeignKey(User,on_delete=models.CASCADE,related_name='i_owner')
    room=models.ForeignKey('Room',on_delete=models.CASCADE)
    name=models.CharField(max_length=35)
    qty=models.IntegerField(default=1)
    size=models.IntegerField(default=10)
    get_date=models.DateField(default=date.today)
    cate_a=models.ForeignKey('Cate_a',on_delete=models.SET_NULL,null=True,blank=True,)
    cate_b=models.ForeignKey('Cate_b',on_delete=models.SET_NULL,null=True,blank=True,)
    comment=models.TextField(max_length=100,blank=True,null=True)
    delete_flag=models.BooleanField(default=False)
    delete_date=models.DateField(default=None,blank=True,null=True)
    pub_date=models.DateTimeField(auto_now_add=True)
    class Meta:
        ordering = ('-id',)
    def __str__(self):
        return\
        'アイテムID'+str(self.id)+\
        'アイテム名'+str(self.name)+\
        'モノサイズ'+str(self.size)


class Cate_a(models.Model):
    namea=models.CharField(max_length=20,blank=True,null=True)
    owner=models.ForeignKey(User,on_delete=models.CASCADE,related_name='cate_a_owner')
    def __str__(self):
        return \
        self.namea

class Cate_b(models.Model):
    nameb=models.CharField(max_length=20,blank=True,null=True)
    owner=models.ForeignKey(User,on_delete=models.CASCADE,related_name='cate_b_owner')
    def __str__(self):
        return \
        self.nameb

#棒グラフ練習用モデル　ProductAというモデルクラスを作成
class ProductA(models.Model):
    Date = models.DateField()        #日付
    Revenue = models.IntegerField()  #収益

