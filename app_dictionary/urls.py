from django.urls import path
from app_dictionary import views
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('',views.home,name='home',),
    path('dictionary',views.dictionary,name='dictionary'),
    path('dictionary_add',views.dictionary_add,name='dictionary_add'),
    path('add_words',views.add_words,name='add_words'),
    path('upload_file',views.upload_file,name='upload_file'),
    path('delete_all',views.delete_all,name='delete_all'),
    path('test_words/<int:pk>',views.test_words,name='test_words'),
    path('next_word/<int:pk>',views.next_word,name='next_word'),
    path('prev_word/<int:pk>',views.prev_word,name='prev_word'),
    path('edit_word/<int:pk>',views.edit_word,name='edit_word'),
    path('save_word/<int:pk>',views.save_word,name='save_word'),
    # currey shop
    path('index',auth_views.LoginView.as_view(template_name='curry_shop_login.html'),name='index'),
    path('register',views.register,name='register'),
    path('profile',views.profile,name='profile'),
    path('add_item',views.add_item,name='add_item'),
    path('itemlist',views.itemlist,name='itemlist'),
    path('billitem',views.billitem,name='billitem'),
    path('item_details/<int:pk>',views.item_details,name='item_details'),
    path('delete_item/<int:pk>',views.delete_item,name='delete_item'),
    path('login',auth_views.LoginView.as_view(template_name='curry_shop_login.html'),name='login'),
    path('logout',auth_views.LogoutView.as_view(template_name='curry_shop_logout.html'),name='logout'),
    path('addbill',views.addbill,name='addbill'),
    path('bill_list',views.bill_list,name='bill_list'),
    path('new_bill_list',views.new_bill_list,name='new_bill_list'),
    path('reject_order',views.reject_order,name='reject_order'),
    path('accept_order',views.accept_order,name='accept_order'),
    path('all_items',views.all_items,name='all_items'),
    path('create_order',views.create_order,name='create_order'),
    path('order_ready',views.order_ready,name='order_ready'),
    path('order_call',views.order_call,name='order_call'),
    path('my_order',views.my_order,name='my_order'),
    path('send_otp',views.send_otp,name='send_otp'),
    path('verify_otp',views.verify_otp,name='verify_otp'),
    path('dispatch_order',views.dispatch_order,name='dispatch_order'),
    path('dispatched_list',views.dispatched_list,name='dispatched_list'),
    path('delevered_order',views.delevered_order,name='delevered_order'),
    path('order_history',views.order_history,name='order_history'),
    path('change_filter',views.change_filter,name='change_filter'),
    path('change_sort',views.change_sort,name='change_sort'),
    path('get_the_reason',views.get_the_reason,name='get_the_reason'),
    path('my_order_track/<int:pk>',views.my_order_track,name='my_order_track'),
    path('update_userdata/<int:pk>',views.update_userdata,name='update_userdata'),
]+ static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)