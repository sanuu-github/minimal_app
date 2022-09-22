from django.urls import path
from.import views

urlpatterns=[
    path('',views.index,name='index'),
    path('<int:num>',views.index,name='index'),
    
    path('createroom',views.createroom,name='createroom'),
    path('editroom/<int:num>',views.editroom,name='editroom'),
    path('deleteroom/<int:num>',views.deleteroom,name='deleteroom'),

    path('createitem',views.createitem,name='createitem'),   
    path('edititem/<int:num>',views.edititem,name='edititem'),
    path('deleteitem/<int:num>',views.deleteitem,name='deleteitem'),

]