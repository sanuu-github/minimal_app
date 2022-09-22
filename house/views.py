#インポート文 
from datetime import date
from unicodedata import name
from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import redirect
from django.core.paginator import Paginator
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from.forms import CreateroomForm,CreateitemForm,SelectroomForm,RoomForm
from.models import Sampleroom,Sampleitem


#以下はグラフ用のインポート分
from django.views.generic import TemplateView
from . import models
from .graph import Output_Graph,Plot_Graph,Plot_PieChart


#円グラフ（アイテム個数）描画関数
@login_required(login_url='/accounts/login/')                       #ログインしていたら使える。  
def get_pie_data_sumqty(request):

    roomid_qtysum=Sampleitem.objects.filter(owner=request.user).select_related('sampleroom').values('sampleroom')\
        .annotate(Sum('qty'),)
    valueslist=[]
    for id_sum in roomid_qtysum:
        i_s=list(id_sum.values())
        for slist in i_s:
            valueslist.append(slist)
    values=valueslist[1::2]
    roomides=valueslist[0::2]
    lavels=[]
    for ids in roomides:
        room_record=Sampleroom.objects.get(id=ids)
        lavels.append(room_record.name)

    pie = [pie for pie in values]                        #Plot_Piechart関数の「p」に渡す配列（円グラフの中身）
    label = [label for label in lavels]                  # Plot_Piechart関数の「l」に渡す配列（円グラフのラベル）
    return Plot_PieChart(pie, label)


#棒グラフ描画関数
@login_required(login_url='/accounts/login/')                       #ログインしていたら使える。
def get_bar_data(request):
    #グラフに必要なデータを抽出
    qs    = models.Sampleitem.objects.filter(owner=request.user)    #Sampleitemクラスの読込
    x     = [x.get_date for x in qs]                                #X軸データ
    y     = [y.originalsize for y in qs]                            #Y軸データ
    return Plot_Graph(x,y)                     

#円グラフ（サイズ合計）描画関数
@login_required(login_url='/accounts/login/')                       #ログインしていたら使える。  
def get_pie_data_sumsize(request):

    #ステップ１　アイテムが登録されている部屋名のみ取得。
    roomid_sizesum=Sampleitem.objects.filter(owner=request.user).select_related('sampleroom').values('sampleroom')\
        .annotate(Sum('originalsize'),)

    #ステップ2･･･合計値のみを取り出してリストの形にする。
    valueslist=[]
    for id_sum in roomid_sizesum:                       #この時点のデータ：{'sampleroom': 3, 'originalsize__sum': 76}
        i_s=list(id_sum.values())                       #この時点のデータ：[3, 76][4, 34][5, 19][6, 88][7, 15][8, 6][19, 33]
        for slist in i_s:                               #この時点のデータ：3 76 4 34 5 19 6 88 7 15 8 6 19 33
            valueslist.append(slist)                    #この時点のデータ：[3, 76, 4, 34, 5, 19, 6, 88, 7, 15, 8, 6, 19, 33]
    values=valueslist[1::2]                             #この時点のデータ：[76,34,19,88,15,6,33]

    #ステップ3････部屋IDのみを取り出してリストの形にする。
    roomides=valueslist[0::2]                           #この時点のデータ：[3, 4, 5, 6, 7, 8, 19]

    #ステップ４･･･「roomides」を一つづつ取り出し合致する部屋名を取得し、リストにする。
    lavels=[]
    for ids in roomides:
        room_record=Sampleroom.objects.get(id=ids)
        lavels.append(room_record.name)

    #◆単純パターン
    #values = [20, 30, 10]
    #lavels = ['Wine', 'Sake', 'Beer']

    pie = [pie for pie in values]                        #Plot_Piechart関数の「p」に渡す配列（円グラフの中身）
    label = [label for label in lavels]                  # Plot_Piechart関数の「l」に渡す配列（円グラフのラベル）
    return Plot_PieChart(pie, label)


#棒グラフ描画関数
@login_required(login_url='/accounts/login/')                       #ログインしていたら使える。
def get_bar_data(request):
    #グラフに必要なデータを抽出
    qs    = models.Sampleitem.objects.filter(owner=request.user)    #Sampleitemクラスの読込
    x     = [x.get_date for x in qs]                                #X軸データ
    y     = [y.originalsize for y in qs]                            #Y軸データ
    return Plot_Graph(x,y)                                          #グラフ作成 これを関数の戻り値とする。


#トップページ
@login_required(login_url='/accounts/login/')  #ログインしていたら使える。
def index(request,num=1):
    user=request.user                        #ログインユーザー情報の取得

    #POST送信時（アイテムリストを部屋切り替えした時）
    if(request.method=='POST'):
        #送信内容の取得
        find=request.session['部屋別表示']=request.POST['部屋別表示']  #フォーム側で取得した部屋名を変数findに取り出す。
        itemlist=Sampleitem.objects.filter(owner=request.user).filter(sampleroom=find)
        print('POST送信')
    #GET送信時
    else:
        #絞り込みをしてページネーションする時
        if '部屋別表示' in request.session:
            find=request.session['部屋別表示']
            itemlist=Sampleitem.objects.filter(owner=request.user).filter(sampleroom=find)
            print('GETでセッション有り')

        #初回アクセス時
        else:
            itemlist=Sampleitem.objects.filter(owner=request.user)
            print('GETでセッション無し')
            print(itemlist)

    page=Paginator(itemlist,10)
    form=SelectroomForm(request.user)

    chart=get_pie_data_sumqty(request)              #グラフ描画関数の戻り値を変数chartで送る。
    graphtitle='部屋別モノサイズ'                    #グラフタイトル

    params={
        'title':'whats in my house',   
        'itemlist':page.get_page(num),
        'form':form, 
        'user':user,
        "chart":chart,
        "graphtitle":graphtitle,
    }
    return render(request,'house/index.html',params)




#部屋追加モデル
@login_required(login_url='/accounts/login/')                   #ログインしていたら使える。
def createroom(request):

    #POST送信時
    if(request.method=='POST'):                                 #部屋を作り、オーナーと名前を保存する。

        #アイテムを作成し設定して保存
        sm=Sampleroom()                                         #サンプルルームモデルのインスタンス（sm）を作成する。
        sm.owner=request.user                                   #オーナーにはログインユーザーをセットする。
        sm.name=request.POST['name']                            #名前には、クリエイトルームフォームから送られてきた値をセットする。
        sm.save()
        
        #完了メッセージの作成
        messages.info(request,'部屋名「'+sm.name+'」を追加しました。')

        #最新リストを作成
        roomlist=Sampleroom.objects.filter(owner=request.user)

        #前の画面に戻る
        return redirect(to='/house/createroom')

    #GET送信時
    else:
        #最新リストを作成
        roomlist=Sampleroom.objects.filter(owner=request.user)

    #共通処理
    params={
        'title':'部屋追加フォーム',
        'form':CreateroomForm(),  
        'roomlist':roomlist, 
        }
    return render(request,'house/createroom.html',params)


#アイテム追加モデル
@login_required(login_url='/accounts/login/')                   #ログインしていたら使える。
def createitem(request):

    #POST送信時
    if(request.method=='POST'):

        #送信内容の取得
        n=request.POST['sampleroom']

        #部屋名の取得
        room=Sampleroom.objects.filter(owner=request.user) \
            .filter(id=n).first()

        #アイテムを作成し設定して保存
        si=Sampleitem()                                         #サンプルルームアイテムのインスタンス（si）を作成する。
        si.owner=request.user                                   #オーナーにはログインユーザーをセットする。
        si.sampleroom=room                                      #送信内容と一致する部屋名をサンプルルームモデルの部屋名から取得してここに入れる。
        si.itemname=request.POST['itemname']                    #名前には、クリエイトルームフォームから送られてきた値をセットする。
        si.originalsize=request.POST['originalsize']
        si.qty=request.POST['qty']
        si.get_date=request.POST['get_date']
        si.comment=request.POST['comment']
        si.save()                                               #入力内容を保存する。
        
        #完了メッセージの作成
        messages.info(request,'モノ名「'+si.itemname+'」を追加しました。')
        return redirect(to='/house/createitem')
    
    #GETアクセス時の処理
    else:
        itemlist=Sampleitem.objects.filter(owner=request.user)
        title='createitem'

    #共通処理
    params={
        'title':title,
        'form':CreateitemForm(),  
        'itemlist':'itemlist', 
        }
    return render(request,'house/createitem.html',params)


#アイテム変更（編集）関数
@login_required(login_url='/accounts/login/')                    #ログインしていたら使える。
def edititem(request,num):
    obj=Sampleitem.objects.get(id=num)
    if(request.method=='POST'):
        item=CreateitemForm(request.POST,instance=obj)
        item.save()
        return redirect(to='/house/createitem')
    params={
        'title':'アイテム変更フォーム',
        'id':num,
        'form':CreateitemForm(instance=obj),
    }
    return render(request,'house/edititem.html',params)


#部屋変更（編集）関数
@login_required(login_url='/accounts/login/')  #ログインしていたら使える。
def editroom(request,num):
    obj=Sampleroom.objects.get(id=num)
    if(request.method=='POST'):
        room=CreateroomForm(request.POST,instance=obj)
        room.save()
        return redirect(to='/house/createroom')
    params={
        'title':'部屋名変更フォーム',
        'id':num,
        'form':CreateroomForm(instance=obj),
    }
    return render(request,'house/editroom.html',params)


#アイテム削除関数
@login_required(login_url='/accounts/login/')  #ログインしていたら使える。
def deleteitem(request,num):
    item=Sampleitem.objects.get(id=num)
    if(request.method=='POST'):
        item.delete()
        return redirect(to='/house')
    params={
        'title':'削除確認',
        'id':num,
        'obj':item,
    }
    return render(request,'house/deleteitem.html',params)


#部屋削除関数
@login_required(login_url='/accounts/login/')  #ログインしていたら使える。
def deleteroom(request,num):
    room=Sampleroom.objects.get(id=num)
    if(request.method=='POST'):
        room.delete()
        return redirect(to='/house/createroom')
    params={
        'title':'削除確認',
        'id':num,
        'obj':room,
    }
    return render(request,'house/deleteroom.html',params)


#Fストリングメモ
# print("私の名前は"+name+"です。")
# print(f’私の’名前は{name}です。年齢は{age}です。)