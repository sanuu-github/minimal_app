from django.urls import path
from.import views

urlpatterns=[
    path('',views.index,name='index'),
    path('<int:num>',views.index,name='index'),

    path('index_room_qty',views.index_room_qty,name='index_room_qty'),
    path('index_room_size',views.index_room_size,name='index_room_size'),
    path('index_catea_qty',views.index_catea_qty,name='index_catea_qty'),
    path('index_catea_size',views.index_catea_size,name='index_catea_size'),
    path('index_cateb_qty',views.index_cateb_qty,name='index_cateb_qty'),
    path('index_cateb_size',views.index_cateb_size,name='index_cateb_size'),

    path('create',views.create,name='create'),
    path('edit_room/<int:num>',views.edit_room,name='edit_room'),
    path('delete_room/<int:num>',views.delete_room,name='delete_room'),

    path('create_item',views.create_item,name='create_item'),
    path('edit_item/<int:num>',views.edit_item,name='edit_item'),
    path('delete_item/<int:num>',views.delete_item,name='delete_item'),

    path('create_catea',views.create_catea,name='create_catea'),
    path('edit_catea/<int:num>',views.edit_catea,name='edit_catea'),
    path('delete_catea/<int:num>',views.delete_catea,name='delete_catea'),

    path('create_cateb',views.create_cateb,name='create_cateb'),
    path('edit_cateb/<int:num>',views.edit_cateb,name='edit_cateb'),
    path('delete_cateb/<int:num>',views.delete_cateb,name='delete_cateb'),


]