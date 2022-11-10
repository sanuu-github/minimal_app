from django import forms
from.models import Room,Item,Cate_a,Cate_b


#アイテム追加フォーム
class CreateitemForm(forms.ModelForm):
    class Meta:
        model=Item
        fields=['name','room','size','qty','get_date','comment',\
            'cate_a','cate_b','delete_flag','delete_date',]
        labels={
            "name":"品名",\
            "room":"追加先の部屋",\
            "size":"モノサイズ",\
            "qty":"数量",\
            "get_date":"追加日",\
            "comment":"備考",\
            "cate_a":"カテゴリーA",\
            "cate_b":"カテゴリーB",\
            "delete_flag":"お別れする",\
            "delete_date":"お別れした日",
        }


#部屋追加フォーム
class CreateroomForm(forms.ModelForm):
    class Meta:
        model=Room
        fields=['name']
        labels={
            'name':"部屋の名前",
            }


#カテゴリーA追加フォーム
class Createcate_aForm(forms.ModelForm):
    class Meta:
        model=Cate_a
        fields=['namea',]
        labels={
            "namea":"カテゴリーAの項目名",
            }


#カテゴリーB追加フォーム
class Createcate_bForm(forms.ModelForm):
    class Meta:
        model=Cate_b
        fields=['nameb']
        labels={
            'nameb':"カテゴリーBの項目名",
            }


#部屋切り替えフォーム
class SelectroomForm(forms.Form):
    def __init__(self,user,*args,**kwargs):                                             #ユーザー毎に表示を変える場合   
        super(SelectroomForm,self).__init__(*args,**kwargs)                             #ユーザー毎に表示を変える場合

        self.fields['部屋別表示']=forms.ChoiceField(                                #プルダウンリストを作ります。
            choices=                                                               #プルダウンリストの中身は変数choicesです。
            [('0','-')]+                                                           #変数choicesの中身は、デォルトの（-：-）と
            [(item.id,item.name) for item in Room.objects.filter(owner=user)],     #ルームモデルに登録されているレコードを変数itemに取出し、name（部屋名）だけにする。
            widget=forms.Select(attrs={'size:':1}),
            )    


#部屋の編集
class CreateForm(forms.Form):
    name:forms.CharField(label='name')
    getdate:forms.DateField(label='getdate')
