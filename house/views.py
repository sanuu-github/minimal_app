#インポート文 ---------------------------------------------------------------------------------------------------------
from datetime import date
from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import redirect
from django.core.paginator import Paginator
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Sum,Count
from.forms import CreateroomForm,CreateitemForm,SelectroomForm,Createcate_aForm,Createcate_bForm
from.models import Room,Item,Cate_a,Cate_b

#タイトル入力

#以下はグラフ用のインポート文--------------------------------------------------------------------------------------------
from django.views.generic import TemplateView
from . import models
from .graph import Output_Graph,Plot_Graph,Plot_PieChart


#インフォメッセージ装飾デコレーター(未使用2）---------------------------------------------------------------------------------
def normal_deco(func):
    def line(n):
        decon = '***************'+n+'****************'
        return decon
    return line

def important_deco(func):
    def diamond(i):
        decoi = '◇◇◇◇◇◇◇◇◇'+i+'◇◇◇◇◇◇◇◇'
        return decoi
    return diamond


#トップページ----------------------------------------------------------------------------------------------------------
@login_required(login_url='/accounts/login/')                        #ログインしていたら使える。
def index(request,num=1):
    user=request.user                                                #ログインユーザー情報の取得

    #POST送信時（アイテムリストを部屋切り替えした時）
    if(request.method=='POST'):
        #送信内容の取得
        find=request.session['部屋別表示']=request.POST['部屋別表示']  #フォーム側で取得した部屋名を変数findに取り出す。
        itemlist=Item.objects.filter(owner=request.user).filter(room=find)

    #GET送信時
    else:
        #絞り込みをしてページネーションする時
        if '部屋別表示' in request.session:
            find=request.session['部屋別表示']
            itemlist=Item.objects.filter(owner=request.user).filter(room=find)
            #print('GETでセッション有り')

        #初回アクセス時
        else:
            itemlist=Item.objects.filter(owner=request.user)
            #print('GETでセッション無し')

    page=Paginator(itemlist,5)
    form=SelectroomForm(request.user)

    params={
        'itemlist':page.get_page(num),
        'form':form, 
        'user':user,
        "chart":get_pie_sample(request),
        "graphtitle":'Sample',
        "totalling":totalling(request),
    }
    return render(request,'house/index.html',params)



#グラフ切替アクセス「部屋別/数」ver
@login_required(login_url='/accounts/login/')                        #ログインしていたら使える。
def index_room_qty(request,num=1):
    user=request.user                                                #ログインユーザー情報の取得

    itemlist=Item.objects.filter(owner=request.user)
    page=Paginator(itemlist,5)
    form=SelectroomForm(request.user)
    chart=get_pie_data_room_sumqty(request)              #グラフ描画関数の戻り値を変数chartで送る。

    params={
        'itemlist':page.get_page(num),
        'form':form, 
        'user':user,
        "chart":chart,
        "graphtitle":'部屋別アイテム数',
    }
    return render(request,'house/index.html',params)

#グラフ切替アクセス「部屋別/サイズ」ver
@login_required(login_url='/accounts/login/')                        #ログインしていたら使える。
def index_room_size(request,num=1):
    user=request.user                        #ログインユーザー情報の取得

    itemlist=Item.objects.filter(owner=request.user)
    page=Paginator(itemlist,5)
    form=SelectroomForm(request.user)
    chart=get_pie_data_room_sumsize(request)              #グラフ描画関数の戻り値を変数chartで送る。

    params={
        'itemlist':page.get_page(num),
        'form':form, 
        'user':user,
        "chart":chart,
        "graphtitle":'部屋別アイテムサイズ',
    }
    return render(request,'house/index.html',params)

#グラフ切替アクセス「カテゴリーA/数」ver
@login_required(login_url='/accounts/login/')                        #ログインしていたら使える。
def index_catea_qty(request,num=1):
    user=request.user                        #ログインユーザー情報の取得

    itemlist=Item.objects.filter(owner=request.user)
    page=Paginator(itemlist,5)
    form=SelectroomForm(request.user)
    chart=get_pie_data_catea_sumqty(request)              #グラフ描画関数の戻り値を変数chartで送る。

    params={
        'itemlist':page.get_page(num),
        'form':form, 
        'user':user,
        "chart":chart,
        "graphtitle":'カテゴリーA別アイテム数',
    }
    return render(request,'house/index.html',params)

#グラフ切替アクセス「カテゴリーA/サイズ」ver
@login_required(login_url='/accounts/login/')                        #ログインしていたら使える。
def index_catea_size(request,num=1):
    user=request.user                        #ログインユーザー情報の取得

    itemlist=Item.objects.filter(owner=request.user)
    page=Paginator(itemlist,5)
    form=SelectroomForm(request.user)
    chart=get_pie_data_catea_sumsize(request)              #グラフ描画関数の戻り値を変数chartで送る。

    params={
        'itemlist':page.get_page(num),
        'form':form, 
        'user':user,
        "chart":chart,
        "graphtitle":'カテゴリーA別アイテムサイズ',
    }
    return render(request,'house/index.html',params)

#グラフ切替アクセス「カテゴリーB/数」ver
@login_required(login_url='/accounts/login/')                        #ログインしていたら使える。
def index_cateb_qty(request,num=1):
    user=request.user                        #ログインユーザー情報の取得

    itemlist=Item.objects.filter(owner=request.user)
    page=Paginator(itemlist,5)
    form=SelectroomForm(request.user)
    chart=get_pie_data_cateb_sumqty(request)              #グラフ描画関数の戻り値を変数chartで送る。

    params={
        'itemlist':page.get_page(num),
        'form':form, 
        'user':user,
        "chart":chart,
        "graphtitle":'カテゴリーB別アイテム数',
    }
    return render(request,'house/index.html',params)

#グラフ切替アクセス「カテゴリーB/サイズ」ver
@login_required(login_url='/accounts/login/')                        #ログインしていたら使える。
def index_cateb_size(request,num=1):
    user=request.user                        #ログインユーザー情報の取得

    itemlist=Item.objects.filter(owner=request.user)
    page=Paginator(itemlist,5)
    form=SelectroomForm(request.user)
    chart=get_pie_data_cateb_sumsize(request)              #グラフ描画関数の戻り値を変数chartで送る。

    params={
        'itemlist':page.get_page(num),
        'form':form, 
        'user':user,
        "chart":chart,
        "graphtitle":'カテゴリーB別アイテムサイズ',
    }
    return render(request,'house/index.html',params)





#円グラフ（サンプル）描画関数----------------------------------------------------------------------------------------------
@login_required(login_url='/accounts/login/')                       #ログインしていたら使える。  
def get_pie_sample(request):

    values = [90,80,70,60,50,40,30,20,10,]
    lavels = ['キッチン','リビング','ダイニング','洋室','玄関','廊下','脱衣所','お風呂','トイレ']

    pie = [pie for pie in values]
    label = [label for label in lavels]
    return Plot_PieChart(pie, label)

#円グラフ（カテゴリーB/数）描画関数-----------------------------------------------------------------------------------------
@login_required(login_url='/accounts/login/')                       #ログインしていたら使える。  
def get_pie_data_cateb_sumqty(request):

    #ステップ１･･･アイテムが登録されている部屋名のみ取得。
    catebid_qtysum=Item.objects.filter(owner=request.user).select_related('cate_b').values('cate_b')\
        .annotate(Sum('qty'),)

    #ステップ2･･･合計値のみを取り出してリストの形にする。
    valueslist=[]
    for id_sum in catebid_qtysum:
        i_s=list(id_sum.values())
        for slist in i_s:
            valueslist.append(slist)
    values=valueslist[1::2]

    #ステップ3････ラベルIDのみを取り出してリストの形にする。
    catebides=valueslist[0::2]

    #ステップ４･･･「cateaides」を一つづつ取り出し合致するラベル名を取得し、リストにする。
    lavels=[]
    for ids in catebides:
        try:
            cateb_record=Cate_b.objects.get(id=ids)
            lavels.append(cateb_record.nameb)
        except:
            lavels.append('未設定')

    pie = [pie for pie in values]
    label = [label for label in lavels]
    return Plot_PieChart(pie, label)

#円グラフ（カテゴリーA/数）描画関数-----------------------------------------------------------------------------------------
@login_required(login_url='/accounts/login/')                       #ログインしていたら使える。  
def get_pie_data_catea_sumqty(request):

    #ステップ１･･･アイテムが登録されている部屋名のみ取得。
    cateaid_qtysum=Item.objects.filter(owner=request.user).select_related('cate_a').values('cate_a')\
        .annotate(Sum('qty'),)

    #ステップ2･･･合計値のみを取り出してリストの形にする。
    valueslist=[]
    for id_sum in cateaid_qtysum:
        i_s=list(id_sum.values())
        for slist in i_s:
            valueslist.append(slist)
    values=valueslist[1::2]

    #ステップ3････ラベルIDのみを取り出してリストの形にする。
    cateaides=valueslist[0::2]

    #ステップ４･･･「cateaides」を一つづつ取り出し合致するラベル名を取得し、リストにする。
    lavels=[]
    for ids in cateaides:
        try:
            catea_record=Cate_a.objects.get(id=ids)
            lavels.append(catea_record.namea)
        except:
            lavels.append('未設定')

    pie = [pie for pie in values]
    label = [label for label in lavels]
    return Plot_PieChart(pie, label)

#円グラフ（カテゴリーB/サイズ）描画関数-------------------------------------------------------------------------------------
@login_required(login_url='/accounts/login/')                       #ログインしていたら使える。  
def get_pie_data_cateb_sumsize(request):

    #ステップ１･･･アイテムが登録されている部屋名のみ取得。
    catebid_sizesum=Item.objects.filter(owner=request.user).select_related('cate_b').values('cate_b')\
        .annotate(Sum('size'),)

    #ステップ2･･･合計値のみを取り出してリストの形にする。
    valueslist=[]
    for id_sum in catebid_sizesum:
        i_s=list(id_sum.values())
        for slist in i_s:
            valueslist.append(slist)
    values=valueslist[1::2]

    #ステップ3････ラベルIDのみを取り出してリストの形にする。
    catebides=valueslist[0::2]

    #ステップ４･･･「cateaides」を一つづつ取り出し合致するラベル名を取得し、リストにする。
    lavels=[]
    for ids in catebides:
        try:
            cateb_record=Cate_b.objects.get(id=ids)
            lavels.append(cateb_record.nameb)
        except:
            lavels.append('未設定')

    pie = [pie for pie in values]
    label = [label for label in lavels]
    return Plot_PieChart(pie, label)

#円グラフ（カテゴリーA/サイズ）描画関数-------------------------------------------------------------------------------------
@login_required(login_url='/accounts/login/')                       #ログインしていたら使える。  
def get_pie_data_catea_sumsize(request):

    #ステップ１･･･アイテムが登録されている部屋名のみ取得。
    cateaid_sizesum=Item.objects.filter(owner=request.user).select_related('cate_a').values('cate_a')\
        .annotate(Sum('size'),)

    #ステップ2･･･合計値のみを取り出してリストの形にする。
    valueslist=[]
    for id_sum in cateaid_sizesum:                       #この時点のデータ：{'name_a': None, 'size__sum': 76}
        i_s=list(id_sum.values())                       #この時点のデータ：[3, 76][4, 34][5, 19][6, 88][7, 15][8, 6][19, 33]
        for slist in i_s:                               #この時点のデータ：3 76 4 34 5 19 6 88 7 15 8 6 19 33
            valueslist.append(slist)                    #この時点のデータ：[3, 76, 4, 34, 5, 19, 6, 88, 7, 15, 8, 6, 19, 33]
    values=valueslist[1::2]                             #この時点のデータ：[76,34,19,88,15,6,33]

    #ステップ3････ラベルIDのみを取り出してリストの形にする。
    cateaides=valueslist[0::2]                           #この時点のデータ：[None, 4, 5, 6, 7, 8, 19]

    #ステップ４･･･「cateaides」を一つづつ取り出し合致するラベル名を取得し、リストにする。
    lavels=[]
    for ids in cateaides:
        try:
            catea_record=Cate_a.objects.get(id=ids)
            lavels.append(catea_record.namea)
        except:
            lavels.append('未設定')                       #カテゴリーを設定のない、Noneが有った場合

    pie = [pie for pie in values]                        #Plot_Piechart関数の「p」に渡す配列（円グラフの中身）
    label = [label for label in lavels]                  # Plot_Piechart関数の「l」に渡す配列（円グラフのラベル）
    return Plot_PieChart(pie, label)

#円グラフ（部屋/数）描画関数-----------------------------------------------------------------------------------------------
@login_required(login_url='/accounts/login/')                       #ログインしていたら使える。  
def get_pie_data_room_sumqty(request):

    #ItemモデルからRoomカラムで括ったqtyの合計を取出す。
    roomid_qtysum=Item.objects.filter(owner=request.user).select_related('room').values('room')\
        .annotate(Sum('qty'),)
    #クエリーセットで出てきたデータをひたすら分解して、graph.pyへ渡す為のリストの形に書き換える泥臭いコード＾o＾；恥
    valueslist=[]
    for id_sum in roomid_qtysum:
        i_s=list(id_sum.values())
        for slist in i_s:
            valueslist.append(slist)
    values=valueslist[1::2]
    roomides=valueslist[0::2]
    labels=[]
    for ids in roomides:
        room_record=Room.objects.get(id=ids)
        labels.append(room_record.name)
    
    #部屋ごとの合計値と部屋名をそれぞれリストの形にして渡すことができました。
    pie = [pie for pie in values]                        #Plot_Piechart関数の「p」に渡す配列（円グラフの中身）
    label = [label for label in labels]                  # Plot_Piechart関数の「l」に渡す配列（円グラフのラベル）
    return Plot_PieChart(pie, label)

#円グラフ（部屋/サイズ）描画関数-------------------------------------------------------------------------------------------
@login_required(login_url='/accounts/login/')                       #ログインしていたら使える。  
def get_pie_data_room_sumsize(request):

    #ステップ１　アイテムが登録されている部屋名のみ取得。
    roomid_sizesum=Item.objects.filter(owner=request.user).select_related('room').values('room')\
        .annotate(Sum('size'),)

    #ステップ2･･･合計値のみを取り出してリストの形にする。
    valueslist=[]
    for id_sum in roomid_sizesum:                       #この時点のデータ：{'room': 3, 'size__sum': 76}
        i_s=list(id_sum.values())                       #この時点のデータ：[3, 76][4, 34][5, 19][6, 88][7, 15][8, 6][19, 33]
        for slist in i_s:                               #この時点のデータ：3 76 4 34 5 19 6 88 7 15 8 6 19 33
            valueslist.append(slist)                    #この時点のデータ：[3, 76, 4, 34, 5, 19, 6, 88, 7, 15, 8, 6, 19, 33]
    values=valueslist[1::2]                             #この時点のデータ：[76,34,19,88,15,6,33]

    #ステップ3････部屋IDのみを取り出してリストの形にする。
    roomides=valueslist[0::2]                           #この時点のデータ：[3, 4, 5, 6, 7, 8, 19]

    #ステップ４･･･「roomides」を一つづつ取り出し合致する部屋名を取得し、リストにする。
    lavels=[]
    for ids in roomides:
        room_record=Room.objects.get(id=ids)
        lavels.append(room_record.name)

    #◆単純パターン
    #values = [20, 30, 10]
    #lavels = ['Wine', 'Sake', 'Beer']

    pie = [pie for pie in values]                        #Plot_Piechart関数の「p」に渡す配列（円グラフの中身）
    label = [label for label in lavels]                  # Plot_Piechart関数の「l」に渡す配列（円グラフのラベル）
    return Plot_PieChart(pie, label)

#棒グラフ描画関数---------------------------------------------------------------------------------------------------------
@login_required(login_url='/accounts/login/')                       #ログインしていたら使える。
def get_bar_data(request):
    #グラフに必要なデータを抽出
    qs    = models.Item.objects.filter(owner=request.user)    #Sampleitemクラスの読込
    x     = [x.get_date for x in qs]                                #X軸データ
    y     = [y.originalsize for y in qs]                            #Y軸データ
    return Plot_Graph(x,y)                                          #グラフ作成 これを関数の戻り値とする。





#グラフ値集計関数
@login_required(login_url='/accounts/login/')                   #ログインしていたら使える。
def totalling(request):

    itemsum=Item.objects.filter(owner=request.user).aggregate(Count('id'))        #アイテムの合計
    qtysum=Item.objects.filter(owner=request.user).aggregate(Sum('qty'))          #数の合計
    sizesum=Item.objects.filter(owner=request.user).aggregate(Sum('size'))        #サイズの合計


    #辞書形式になっているので、整数値で取り出す。
    totall='登録されているアイテム合計:'+str(itemsum['id__count'])\
    +'････アイテム 数量合計:'+str(qtysum['qty__sum'])\
    +'････アイテム サイズ合計:'+str(sizesum['size__sum'])

    return(totall)                                          #関数呼び出し元にdateで返す。




#部屋追加関数-------------------------------------------------------------------------------------------------------------
@login_required(login_url='/accounts/login/')                   #ログインしていたら使える。
def create(request):

    #POST送信時
    if(request.method=='POST'):                                 #部屋を作り、オーナーと名前を保存する。

        #アイテムを作成し設定して保存
        rmi=Room()                                              #Roomモデルのインスタンス(rmi)を作成する。
        rmi.owner=request.user                                  #オーナーにはログインユーザーをセットする。
        rmi.name=request.POST['name']                           #名前には、クリエイトルームフォームから送られてきた値をセットする。
        rmi.save()

        #完了メッセージの作成
        messages.info(request,'部屋名「'+rmi.name+'」を追加しました。')

        #最新リストを作成
        roomlist=Room.objects.filter(owner=request.user)
        catealist=Cate_a.objects.filter(owner=request.user)
        cateblist=Cate_b.objects.filter(owner=request.user)

        #前の画面に戻る
        return redirect(to='/house/create')

    #GET送信時
    else:
        #最新リストを作成
        roomlist=Room.objects.filter(owner=request.user)
        catealist=Cate_a.objects.filter(owner=request.user)
        cateblist=Cate_b.objects.filter(owner=request.user)

    #共通処理
    params={
        'form':CreateroomForm(),  
        'form_a':Createcate_aForm(),
        'form_b':Createcate_bForm(),       
        'roomlist':roomlist, 
        'catealist':catealist,
        'cateblist':cateblist,
        }
    return render(request,'house/create.html',params)


#カテゴリーA追加関数-------------------------------------------------------------------------------------------------------
@login_required(login_url='/accounts/login/')                   #ログインしていたら使える。
def create_catea(request):

    #POST送信時
    if(request.method=='POST'):                                 #カテゴリーを作り、オーナーと名前を保存する。

        #アイテムを作成し設定して保存
        cai=Cate_a()                                           #Cate_aモデルのインスタンス(cami)を作成する。
        cai.owner=request.user                                 #オーナーにはログインユーザーをセットする。
        cai.namea=request.POST['namea']                         #名前には、クリエイトルームフォームから送られてきた値をセットする。
        cai.save()
        
        #完了メッセージの作成
        messages.info(request,'カテゴリーAに項目名「'+cai.namea+'」を追加しました。')

        #最新リストを作成
        catealist=Cate_a.objects.filter(owner=request.user)

        #前の画面に戻る
        return redirect(to='/house/create')

    #GET送信時
    else:
        #最新リストを作成
        roomlist=Room.objects.filter(owner=request.user)
        catealist=Cate_a.objects.filter(owner=request.user)
        cateblist=Cate_b.objects.filter(owner=request.user)

    #共通処理
    params={
        'form':Createcate_aForm(),
        'roomlist':roomlist, 
        'catealist':catealist,
        'cateblist':cateblist,
        }
    return render(request,'house/create.html',params)


#カテゴリーB追加関数-------------------------------------------------------------------------------------------------------
@login_required(login_url='/accounts/login/')                   #ログインしていたら使える。
def create_cateb(request):

    #POST送信時
    if(request.method=='POST'):                                 #カテゴリーを作り、オーナーと名前を保存する。

        #アイテムを作成し設定して保存
        cbi=Cate_b()                                           #Cate_bモデルのインスタンス(cbmi)を作成する。
        cbi.owner=request.user                                 #オーナーにはログインユーザーをセットする。
        cbi.nameb=request.POST['nameb']                         #名前には、クリエイトルームフォームから送られてきた値をセットする。
        cbi.save()
        
        #完了メッセージの作成
        messages.info(request,'カテゴリーBに項目名「'+cbi.nameb+'」を追加しました。')

        #最新リストを作成
        roomlist=Room.objects.filter(owner=request.user)
        catealist=Cate_a.objects.filter(owner=request.user)
        cateblist=Cate_b.objects.filter(owner=request.user)

        #前の画面に戻る
        return redirect(to='/house/create')

    #GET送信時
    else:
        #最新リストを作成
        cateblist=Cate_b.objects.filter(owner=request.user)

    #共通処理
    params={
        'form':Createcate_bForm(),
        'roomlist':roomlist, 
        'catealist':catealist,
        'cateblist':cateblist,
        }
    return render(request,'house/create.html',params)


#アイテム追加モデル--------------------------------------------------------------------------------------------------------
@login_required(login_url='/accounts/login/')                   #ログインしていたら使える。
def create_item(request):

    #POST送信時
    if(request.method=='POST'):

        #送信内容の取得　部屋名
        n=request.POST['room']
        room=Room.objects.filter(owner=request.user)\
            .filter(id=n).first()

        #送信内容の取得　カテゴリーA
        if request.POST['cate_a']=='':
            catea=None
        else:
            a=request.POST['cate_a']
            catea=Cate_a.objects.filter(owner=request.user)\
                .filter(id=a).first()

        #送信内容の取得　カテゴリーB
        if request.POST['cate_b']=='':
            cateb=None
        else:
            b=request.POST['cate_b']
            cateb=Cate_b.objects.filter(owner=request.user)\
                .filter(id=b).first()

        #送信内容の取得　削除日
        if request.POST['delete_date']=='':
            d=None
        else:
            d=request.POST['delete_date']


        #アイテムを作成し設定して保存
        ii=Item()                                            #itemモデルのインスタンス（ii）を作成する。
        ii.owner=request.user                                #オーナーにはログインユーザーをセットする。
        ii.room=room                                         #送信内容と一致する部屋名をroomモデルの部屋名から取得してここに入れる。
        ii.name=request.POST['name']                         #名前には、クリエイトルームフォームから送られてきた値をセットする。
        ii.size=request.POST['size']
        ii.qty=request.POST['qty']
        ii.get_date=request.POST['get_date']
        ii.comment=request.POST['comment']
        ii.cate_a=catea
        ii.cate_b=cateb
        ii.delete_flag=request.POST.get('delete_flag',False)
        ii.delete_date=d
        ii.save()                                            #入力内容を保存する。
        
        #完了メッセージの作成
        messages.info(request,'モノ名「'+ii.name+'」を追加しました。')
        return redirect(to='/house/create_item')
    
    #GETアクセス時の処理
    else:
        itemlist=Item.objects.filter(owner=request.user)
        title='createitem'

    #共通処理
    params={
        'title':title,
        'form':CreateitemForm(),
        'itemlist':itemlist,
        }
    return render(request,'house/create_item.html',params)


#アイテム変更（編集）関数--------------------------------------------------------------------------------------------------
@login_required(login_url='/accounts/login/')                    #ログインしていたら使える。
def edit_item(request,num):
    obj=Item.objects.get(id=num)
    if(request.method=='POST'):
        item=CreateitemForm(request.POST,instance=obj)
        item.save()
        return redirect(to='/house')
    
    params={
        'title':'アイテム変更フォーム',
        'id':num,
        'form':CreateitemForm(instance=obj),
    }
    return render(request,'house/edit_item.html',params)


#部屋変更（編集）関数------------------------------------------------------------------------------------------------------
@login_required(login_url='/accounts/login/')                   #ログインしていたら使える。
def edit_room(request,num):
    obj=Room.objects.get(id=num)
    if(request.method=='POST'):
        room=CreateroomForm(request.POST,instance=obj)
        room.save()
        return redirect(to='/house/create')
    params={
        'title':'部屋名変更フォーム',
        'id':num,
        'form':CreateroomForm(instance=obj),
    }
    return render(request,'house/edit_room.html',params)

#部屋変更（編集）関数------------------------------------------------------------------------------------------------------
@login_required(login_url='/accounts/login/')                   #ログインしていたら使える。
def edit_catea(request,num):
    obj=Cate_a.objects.get(id=num)
    if(request.method=='POST'):
        recorda=Createcate_aForm(request.POST,instance=obj)
        recorda.save()
        return redirect(to='/house/create')
    params={
        'title':'部屋名変更フォーム',
        'id':num,
        'form':Createcate_aForm(instance=obj),
    }
    return render(request,'house/edit_catea.html',params)

#カテゴリーB変更（編集）関数------------------------------------------------------------------------------------------------------
@login_required(login_url='/accounts/login/')                   #ログインしていたら使える。
def edit_cateb(request,num):
    obj=Cate_b.objects.get(id=num)
    if(request.method=='POST'):
        recordb=Createcate_bForm(request.POST,instance=obj)
        recordb.save()
        return redirect(to='/house/create')
    params={
        'title':'部屋名変更フォーム',
        'id':num,
        'form':Createcate_bForm(instance=obj),
    }
    return render(request,'house/edit_cateb.html',params)


#アイテム削除関数----------------------------------------------------------------------------------------------------------
@login_required(login_url='/accounts/login/')                   #ログインしていたら使える。
def delete_item(request,num):
    item=Item.objects.get(id=num)
    if(request.method=='POST'):
        item.delete()
        return redirect(to='/house')
    params={
        'title':'削除確認',
        'id':num,
        'obj':item,
    }
    return render(request,'house/delete_item.html',params)


#部屋削除関数--------------------------------------------------------------------------------------------------------------
@login_required(login_url='/accounts/login/')  #ログインしていたら使える。
def delete_room(request,num):
    room=Room.objects.get(id=num)
    if(request.method=='POST'):
        room.delete()
        return redirect(to='/house/create')
    params={
        'title':'削除確認',
        'id':num,
        'obj':room,
    }
    return render(request,'house/delete_room.html',params)



#カテゴリーA削除関数--------------------------------------------------------------------------------------------------------------
@login_required(login_url='/accounts/login/')  #ログインしていたら使える。
def delete_catea(request,num):
    recorda=Cate_a.objects.get(id=num)
    if(request.method=='POST'):
        recorda.delete()
        return redirect(to='/house/create')
    params={
        'title':'削除確認',
        'id':num,
        'obj':recorda,
    }
    return render(request,'house/delete_catea.html',params)


#カテゴリーB削除関数--------------------------------------------------------------------------------------------------------------
@login_required(login_url='/accounts/login/')  #ログインしていたら使える。
def delete_cateb(request,num):
    recordb=Cate_b.objects.get(id=num)
    if(request.method=='POST'):
        recordb.delete()
        return redirect(to='/house/create')
    params={
        'title':'削除確認',
        'id':num,
        'obj':recordb,
    }
    return render(request,'house/delete_cateb.html',params)



#Fストリングメモ
# print("私の名前は"+name+"です。")
# print(f’私の’名前は{name}です。年齢は{age}です。)