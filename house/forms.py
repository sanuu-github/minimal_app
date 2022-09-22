from django import forms
from.models import Sampleroom,Sampleitem


#モノ追加フォーム
class CreateitemForm(forms.ModelForm):
    class Meta:
        model=Sampleitem
        fields=['itemname','sampleroom','originalsize','qty','get_date','comment',]
        labels={
            "itemname":"品名","sampleroom":"追加先の部屋","originalsize":"モノサイズ","qty":"数量","get_date":"追加日","comment":"備考",
        }


#部屋追加フォーム
class CreateroomForm(forms.ModelForm):
    class Meta:
        model=Sampleroom
        fields=['name']
        labels={
            'name':"部屋の名前",
            }


#部屋切り替えフォーム
class SelectroomForm(forms.Form):
    def __init__(self,user,*args,**kwargs):                                             #ユーザー毎に表示を変える場合   
        super(SelectroomForm,self).__init__(*args,**kwargs)                             #ユーザー毎に表示を変える場合

        self.fields['部屋別表示']=forms.ChoiceField(                                     #プルダウンリストを作ります。
            choices=                                                                    #プルダウンリストの中身は変数choicesです。
            [('0','-')]+                                                                #変数choicesの中身は、デォルトの（-：-）と
            [(item.id,item.name) for item in Sampleroom.objects.filter(owner=user)],     #ルームモデルに登録されているレコードを変数itemに取出し、name（部屋名）だけにする。
            widget=forms.Select(attrs={'size:':1}),
            )    


#部屋のフォーム
class RoomForm(forms.ModelForm):
    class Meta:
        model=Sampleroom
        fields=['name','id']


#部屋の編集
class CreateForm(forms.Form):
    name:forms.CharField(label='name')
    getdate:forms.DateField(label='getdate')
